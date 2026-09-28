"""Lessons in one area, read together, to find claims that disagree.

The fact checker reads one lesson at a time, so it cannot see that
`java-concurrenthashmap` says a tree bin untreeifies "when chains shrink"
while `java-hashmap-internals` correctly says removal-time untreeification is
structural and not size-based. Both look fine alone. A reader who studies
both gets two different models of the same mechanism and no way to tell which
is right.

Pairwise comparison is quadratic and most pairs share nothing, so each area is
read in batches of its definitions and key points - the checkable claims -
rather than whole lessons.
"""

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from ..llm import lock_for

BATCH = 8
WORKERS = 4  # each window waits on the API, not on us

SYSTEM = """You are checking a set of interview-prep lessons from one subject area for claims that contradict each other.

Each lesson is given as its title, its opening definition, and its key points. They were written independently, so the same mechanism may be described two different ways.

Report only genuine contradictions: two lessons stating things that cannot both be true of the same thing. For each, say which one is correct and which lesson should change.

Do NOT report:
- Different levels of detail. A short summary and a precise account of the same mechanism agree; they are not in conflict.
- Different topics that merely sound similar, or the same word used for genuinely different things in different contexts.
- Style, wording, emphasis, or one lesson omitting what another covers.

If nothing genuinely contradicts, return an empty list. That is the normal outcome; do not invent conflicts to look useful."""


class Contradiction(BaseModel):
    topics: list[str] = Field(min_length=2, description="the topic slugs whose claims disagree")
    disagreement: str = Field(min_length=20, description="one sentence on what they say differently")
    correct: str = Field(min_length=20, description="what is actually true")
    fix: str = Field(description="the topic slug that should change")


class Contradictions(BaseModel):
    contradictions: list[Contradiction] = Field(default_factory=list, max_length=10)


def claims_of(body_md: str) -> str:
    """A lesson's checkable core: its opening definition and its key points."""
    definition = body_md.strip().split("\n\n", 1)[0]
    points = re.search(r"## Key points\s*\n(.+?)(?=\n## |\Z)", body_md, re.DOTALL)
    return f"{definition}\n{points.group(1).strip() if points else ''}".strip()


def lessons_in(con, domain: str) -> list[dict]:
    rows = con.execute(
        """select l.topic_slug, l.title, l.body_md
           from lessons l join topics t on t.slug = l.topic_slug
           where l.status = 'ok' and t.domain = ? order by t.sort, l.topic_slug""",
        [domain],
    ).fetchall()
    return [{"slug": s, "title": t, "claims": claims_of(b)} for s, t, b in rows]


def check(llm, domain: str, group: list[dict], tier: str = "smart") -> list[Contradiction]:
    body = "\n\n".join(f"### {x['title']}  [{x['slug']}]\n{x['claims']}" for x in group)
    return llm.complete_json(SYSTEM, f"Area: {domain}\n\n{body}", Contradictions,
                             tier=tier, purpose="consistency").contradictions


def save(con, rows: list[dict], lock=None) -> None:
    """Keep each window's findings as they land.

    A run killed 61 windows of 69 in lost every one of them, because they were
    collected in memory and returned at the end - about $2 of model calls for
    nothing. The same mistake the lesson run was built to avoid.
    """
    if not rows:
        return
    now = datetime.now(timezone.utc)
    args = [[r["domain"], r["topics"], r["disagreement"], r["correct"], r["fix"], now] for r in rows]
    statement = """insert or replace into lesson_contradictions
                   (domain, topics, disagreement, correct, fix, found_at) values (?, ?, ?, ?, ?, ?)"""
    if lock:
        with lock:
            con.executemany(statement, args)
    else:
        con.executemany(statement, args)


def retire(con, applied: list[dict]) -> None:
    """Forget findings whose correction has been handed to the rewrite.

    A finding kept after its lesson was fixed comes back on the next `--fix`
    and marks the corrected lesson for rewrite again, carrying the note it has
    already taken. The record of what was wrong lives in the report file and in
    git; what this table is for is work still to do.
    """
    if not applied:
        return
    con.executemany(
        "delete from lesson_contradictions where domain = ? and disagreement = ?",
        [[x["domain"], x["disagreement"]] for x in applied],
    )


def stored(con) -> list[dict]:
    rows = con.execute(
        """select domain, topics, disagreement, correct, fix from lesson_contradictions
           order by domain, disagreement"""
    ).fetchall()
    return [dict(zip(["domain", "topics", "disagreement", "correct", "fix"], r)) for r in rows]


def run(con, llm, domains: list[str] | None = None, tier: str = "smart") -> list[dict]:
    areas = domains or [r[0] for r in con.execute("select distinct domain from topics order by 1").fetchall()]
    # Overlapping windows: a contradiction between neighbours in the sort order
    # is the likely case, and every lesson is seen alongside others.
    windows = []
    for domain in areas:
        group = lessons_in(con, domain)
        if len(group) < 2:
            continue
        for i in range(0, len(group), BATCH // 2):
            window = group[i : i + BATCH]
            if len(window) < 2:
                break
            windows.append((domain, window))

    found: list[dict] = stored(con)
    done = 0
    db = lock_for(con)
    print(f"{len(windows)} windows across {len(areas)} areas, {WORKERS} at a time", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(check, llm, domain, window, tier): domain for domain, window in windows}
        for future in as_completed(futures):
            domain = futures[future]
            done += 1
            try:
                landed = [{"domain": domain, **c.model_dump()} for c in future.result()]
                found += landed
                save(con, landed, db)
            except Exception as e:  # one window failing must not lose the rest
                print(f"  {domain}: window failed, {type(e).__name__}: {e}", flush=True)
            print(f"  [{done}/{len(windows)}] {domain}", flush=True)
    # The same pair can surface in two overlapping windows.
    seen, unique = set(), []
    for c in found:
        key = (tuple(sorted(c["topics"])), c["disagreement"][:60])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique
