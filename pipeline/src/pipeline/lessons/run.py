"""Generate lessons topic by topic, saving each one as it lands.

Saving per topic is not a detail: the first card run lost 278 sources of work
when it was interrupted, because it only wrote at the end.
"""

import json
import time
from datetime import datetime, timezone

from ..llm import LLM, BudgetExceeded, LLMError, spend_usd
from . import check as checks
from .context import for_topic
from .write import render, write

RETRIES = 2  # a failed contract is regenerated rather than published


def topics_to_write(con, only: list[str] | None, limit: int | None, redo: bool) -> list[dict]:
    rows = con.execute(
        """
        select t.slug, t.name, t.domain, t.description, t.importance, p.name as parent_name
        from topics t left join topics p on p.slug = t.parent_slug
        where (? or t.slug not in (select topic_slug from lessons where status = 'ok'))
        order by t.importance desc, t.slug
        """,
        [redo],
    ).fetchall()
    cols = ["slug", "name", "domain", "description", "importance", "parent_name"]
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


def one(llm: LLM, topic: dict, documents: list[dict], tier: str = "smart") -> tuple[str, list[str], str]:
    """Write one lesson, regenerating while it fails the contract.
    Returns (body_md, refs, problems_text). Empty problems means publishable."""
    context, refs = for_topic(topic, documents)
    problems: list[str] = []
    for _ in range(RETRIES):
        lesson = write(llm, topic, context, tier=tier)
        body = render(lesson)
        problems = checks.check(body, lesson.should_answer)
        if not problems:
            return body, refs, ""
    return body, refs, "; ".join(problems)


def save(con, topic: dict, body: str, refs: list[str], problems: str) -> None:
    con.execute(
        """insert or replace into lessons
           (topic_slug, title, body_md, source_refs, words, status, problems, generated_at)
           values (?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            topic["slug"], topic["name"], body, json.dumps(refs), checks.word_count(body),
            "failed" if problems else "ok", problems or None,
            datetime.now(timezone.utc),
        ],
    )


def run(con, only: list[str] | None = None, limit: int | None = None, redo: bool = False,
        tier: str = "smart", llm: LLM | None = None) -> tuple[int, int]:
    """Returns (written, failed)."""
    llm = llm or LLM(con)
    todo = topics_to_write(con, only, limit, redo)
    started, before = time.time(), spend_usd(con)
    written = failed = 0

    print(f"{len(todo)} topics to write", flush=True)
    for i, topic in enumerate(todo, 1):
        docs = documents_for(con, topic["slug"])
        try:
            body, refs, problems = one(llm, topic, docs, tier=tier)
        except BudgetExceeded as e:
            print(f"  stopping: {e}", flush=True)
            break
        except LLMError as e:
            print(f"[{i}/{len(todo)}] {topic['slug']}: FAILED {e}", flush=True)
            failed += 1
            continue
        save(con, topic, body, refs, problems)
        written += not problems
        failed += bool(problems)
        spent = spend_usd(con) - before
        rate = spent / i
        print(
            f"[{i}/{len(todo)}] {topic['slug']}  {checks.word_count(body)}w  "
            f"{len(docs)} docs  ${spent:.3f} (${rate:.4f}/topic, ~${rate * len(todo):.2f} total)  "
            f"{int(time.time() - started)}s"
            + (f"  FAILED CONTRACT: {problems}" if problems else ""),
            flush=True,
        )
    return written, failed
