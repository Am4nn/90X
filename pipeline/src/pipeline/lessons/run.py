"""Generate lessons topic by topic, saving each one as it lands.

Saving per topic is not a detail: the first card run lost 278 sources of work
when it was interrupted, because it only wrote at the end.

Each lesson goes through write -> structural contract -> independent fact
check -> rewrite with corrections. A lesson that still has findings after the
last pass is stored as `failed` with the findings attached, so it can be read
and fixed rather than silently published.
"""

import json
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from ..llm import LLM, BudgetExceeded, LLMError, lock_for, spend_usd
from ..normalize.interview_questions import parse_all
from . import check as checks
from . import evidence as ev
from . import verify
from .context import for_topic
from .write import render, write

MIN_CONTEXT = 400  # characters; below this there is nothing to write from
MAX_PROBLEM_SOURCES = 8  # candidates; context.for_topic takes what fits
PASSES = 4  # write, a correction pass for soft findings, and rewrites for false ones
WORKERS = 14  # topics in flight
# Not a CPU number. A worker spends almost all its time waiting on an HTTP
# response - the whole run uses about half a second of CPU per 45 seconds - so
# cores are irrelevant and the ceiling is the provider's rate limit.


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


def spare_documents(con) -> list[dict]:
    """Documents mapped to no topic: 2,346 of 5,290, so nearly half the corpus.

    Read once per run and offered to every topic, where `context.for_topic` takes
    only the ones whose title overlaps the topic's name. Titles and bodies of
    every one of them is far too much to hold, so this is capped at the longest -
    length is a rough proxy for a real article rather than a stub heading.
    """
    rows = con.execute(
        """select id, title, body_md from documents
           where topic_slug is null and length(coalesce(body_md, '')) > 400
           order by length(body_md) desc limit 1200"""
    ).fetchall()
    return [dict(zip(["id", "title", "body_md"], r)) for r in rows]


def problems_for(con, topic: dict) -> list[dict]:
    """The statements of the problems in a DSA pattern, hardest-earned first.

    A pattern's problems are the best material we hold for it, and no lesson read
    one until now: `sliding-window` was written from a roadmap paragraph while 150
    real statements sat in the same database. Interview problems only, and the
    NeetCode 150 and Blind 75 first, for the same reason `evidence.problems_for`
    does it - contest problems are a different sport.
    """
    if topic["domain"] != "dsa":
        return []
    rows = con.execute(
        """select slug, title, difficulty, statement_md, source_id
           from problems
           where pattern_slug = ? and kind = 'leetcode' and length(coalesce(statement_md, '')) > 200
           order by (nc150 or blind75) desc, importance desc limit ?""",
        [topic["slug"], MAX_PROBLEM_SOURCES],
    ).fetchall()
    return [dict(zip(["slug", "title", "difficulty", "statement_md", "source_id"], r)) for r in rows]


class NoSource(LLMError):
    """Raised rather than let a model write a lesson out of its own memory.

    Every lesson must come from material we downloaded: a document, or a
    roadmap.sh node's own text. Two of the first 274 slipped through with
    neither - `beh-teamwork` and `simulation`, both topics we hold no documents
    for - and a lesson written from memory is exactly the thing the gates
    downstream cannot catch, because it reads perfectly well and cites nothing.
    """


def one(llm: LLM, con, topic: dict, documents: list[dict], questions=None, tier: str = "smart",
        lock=None, spare: list[dict] | None = None, problems: list[dict] | None = None) -> dict:
    """Write, fact-check, and rewrite once with the corrections."""
    context, refs = for_topic(topic, documents, spare, problems)
    if not refs or len(context) < MIN_CONTEXT:
        raise NoSource(
            f"no source material for {topic['slug']}: {len(refs)} refs, {len(context)} characters. "
            "Download something for it first."
        )
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
            return {"body": body, "summary": lesson.summary, "refs": refs, "linked": linked,
                    "problems": "", "findings": [f.model_dump() for f in findings]}
        notes = verify.notes(findings)

    unresolved = [f for f in findings if f.verdict == "wrong"]
    return {
        "body": body,
        "summary": lesson.summary,
        "refs": refs,
        "linked": linked,
        "problems": "; ".join(problems) if problems else f"{len(unresolved)} false claims unresolved",
        "findings": [f.model_dump() for f in findings],
    }


def save(con, topic: dict, result: dict) -> None:
    con.execute(
        """insert or replace into lessons
           (topic_slug, title, summary, body_md, source_refs, practice, findings, words, status, problems, generated_at)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            topic["slug"], topic["name"], result.get("summary"), result["body"], json.dumps(result["refs"]),
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
    # Also once: 1,200 documents belonging to no topic, offered to every one of
    # them. `for_topic` keeps only what overlaps the topic's name.
    spare = spare_documents(con)
    started, before = time.time(), spend_usd(con)
    written = failed = 0

    print(f"{len(todo)} topics to write, {WORKERS} at a time", flush=True)
    # DuckDB connections are not thread-safe, so every touch of `con` - the
    # document read, the save, the spend total, and the LLM's own cost log -
    # happens under the connection's one lock.
    db = lock_for(con)
    done = 0

    def work(topic: dict):
        with db:
            docs = documents_for(con, topic["slug"])
            problems = problems_for(con, topic)
        return topic, docs, one(llm, con, topic, docs, questions, tier=tier, lock=db,
                                spare=spare, problems=problems)

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
                    # The traceback goes with it: a bare "KeyError: 'title'" from
                    # a 40-minute run tells you nothing about which of the six
                    # places that touch a title raised it.
                    print(f"{topic['slug']}: FAILED {type(e).__name__}: {e}\n"
                          + "".join(traceback.format_exception(e)).rstrip(), flush=True)
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
