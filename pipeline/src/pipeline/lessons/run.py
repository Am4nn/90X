"""Generate lessons topic by topic, saving each one as it lands.

Saving per topic is not a detail: the first card run lost 278 sources of work
when it was interrupted, because it only wrote at the end.

Each lesson goes through write -> structural contract -> independent fact
check -> rewrite with corrections. A lesson that still has findings after the
last pass is stored as `failed` with the findings attached, so it can be read
and fixed rather than silently published.
"""

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from ..llm import LLM, BudgetExceeded, LLMError, spend_usd
from ..normalize.interview_questions import parse_all
from . import check as checks
from . import evidence as ev
from . import verify
from .context import for_topic
from .write import render, write

PASSES = 4  # write, a correction pass for soft findings, and rewrites for false ones
WORKERS = 4  # topics in flight; the writer waits on the API, not on us


def topics_to_write(con, only: list[str] | None, limit: int | None, redo: bool) -> list[dict]:
    rows = con.execute(
        """
        select t.slug, t.name, t.domain, t.description, t.importance, p.name as parent_name,
               (select l.problems from lessons l where l.topic_slug = t.slug) as carried_notes
        from topics t left join topics p on p.slug = t.parent_slug
        where (? or t.slug not in (select topic_slug from lessons where status = 'ok'))
        order by t.importance desc, t.slug
        """,
        [redo],
    ).fetchall()
    cols = ["slug", "name", "domain", "description", "importance", "parent_name", "carried_notes"]
    out = [dict(zip(cols, r)) for r in rows]
    if only:
        wanted = set(only)
        out = [t for t in out if t["slug"] in wanted]
    return out[:limit] if limit else out


def documents_for(con, slug: str) -> list[dict]:
    rows = con.execute(
        "select id, title, body_md from documents where topic_slug = ? order by sort, id", [slug]
    ).fetchall()
    return [dict(zip(["id", "title", "body_md"], r)) for r in rows]


def one(llm: LLM, con, topic: dict, documents: list[dict], questions=None, tier: str = "smart",
        lock=None) -> dict:
    """Write, fact-check, and rewrite once with the corrections."""
    context, refs = for_topic(topic, documents)
    # `consistency --fix` leaves its correction on the lesson. Without this the
    # rewrite it asks for runs without the finding that prompted it.
    notes = topic.get("carried_notes") or ""
    if lock:
        with lock:
            evidence_text, linked = ev.for_topic(con, topic, questions)
    else:
        evidence_text, linked = ev.for_topic(con, topic, questions)
    findings = []
    softened = False

    for _ in range(PASSES):
        lesson = write(llm, topic, context, evidence=evidence_text, notes=notes, tier=tier)
        body = render(lesson)
        problems = checks.check(body, [f.question for f in lesson.follow_ups])
        if problems:
            notes = "\n".join(f"- [contract] {p}" for p in problems)
            findings = []
            continue
        review = verify.review(llm, topic, body)
        blocking = verify.blocking(review)
        findings = list(review.findings)
        if not blocking:
            # A soft objection is not a gate, but it does earn one correction
            # pass: the reviewer found something real, and the rewrite usually
            # takes it. Whatever comes back after that is accepted.
            if findings and not softened:
                softened = True
                notes = verify.notes(findings)
                continue
            return {"body": body, "refs": refs, "linked": linked, "problems": "",
                    "findings": [f.model_dump() for f in findings]}
        notes = verify.notes(findings)

    unresolved = [f for f in findings if f.verdict == "wrong"]
    return {
        "body": body,
        "refs": refs,
        "linked": linked,
        "problems": "; ".join(problems) if problems else f"{len(unresolved)} false claims unresolved",
        "findings": [f.model_dump() for f in findings],
    }


def save(con, topic: dict, result: dict) -> None:
    con.execute(
        """insert or replace into lessons
           (topic_slug, title, body_md, source_refs, practice, findings, words, status, problems, generated_at)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            topic["slug"], topic["name"], result["body"], json.dumps(result["refs"]),
            json.dumps(result["linked"]), json.dumps(result["findings"]),
            checks.word_count(result["body"]),
            "failed" if result["problems"] else "ok", result["problems"] or None,
            datetime.now(timezone.utc),
        ],
    )


def run(con, only: list[str] | None = None, limit: int | None = None, redo: bool = False,
        tier: str = "smart", llm: LLM | None = None) -> tuple[int, int]:
    """Returns (written, failed)."""
    llm = llm or LLM(con)
    todo = topics_to_write(con, only, limit, redo)
    questions = parse_all()  # parsed once; every system_design topic searches it
    started, before = time.time(), spend_usd(con)
    written = failed = 0

    print(f"{len(todo)} topics to write, {WORKERS} at a time", flush=True)
    # DuckDB connections are not thread-safe, so every touch of `con` - the
    # document read, the save, the spend total - happens under this lock.
    db = threading.Lock()
    done = 0

    def work(topic: dict):
        with db:
            docs = documents_for(con, topic["slug"])
        return topic, docs, one(llm, con, topic, docs, questions, tier=tier, lock=db)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(work, t): t for t in todo}
        try:
            for future in as_completed(futures):
                topic = futures[future]
                try:
                    topic, docs, result = future.result()
                except BudgetExceeded as e:
                    print(f"  stopping: {e}", flush=True)
                    for f in futures:
                        f.cancel()
                    break
                except LLMError as e:
                    print(f"{topic['slug']}: FAILED {e}", flush=True)
                    failed += 1
                    continue
                except Exception as e:
                    # A provider timeout or a bad tier must not cancel the
                    # topics still in flight: one bad call used to end the run.
                    print(f"{topic['slug']}: FAILED {type(e).__name__}: {e}", flush=True)
                    failed += 1
                    continue
                with db:
                    save(con, topic, result)
                    spent = spend_usd(con) - before
                done += 1
                written += not result["problems"]
                failed += bool(result["problems"])
                rate = spent / done
                linked = result["linked"]
                print(
                    f"[{done}/{len(todo)}] {topic['slug']}  {checks.word_count(result['body'])}w  "
                    f"{len(docs)} docs  {len(linked['problems'])}p/{len(linked['questions'])}q  "
                    f"${spent:.3f} (${rate:.4f}/topic, ~${rate * len(todo):.2f} total)  "
                    f"{int(time.time() - started)}s"
                    + (f"  FAILED: {result['problems']}" if result["problems"] else ""),
                    flush=True,
                )
        finally:
            pool.shutdown(wait=False, cancel_futures=True)

    return written, failed
