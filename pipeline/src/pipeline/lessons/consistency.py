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

from pydantic import BaseModel, Field

BATCH = 8

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


def run(con, llm, domains: list[str] | None = None, tier: str = "smart") -> list[dict]:
    areas = domains or [r[0] for r in con.execute("select distinct domain from topics order by 1").fetchall()]
    found: list[dict] = []
    for domain in areas:
        group = lessons_in(con, domain)
        if len(group) < 2:
            continue
        # Overlapping windows: a contradiction between neighbours in the sort
        # order is the likely case, and every lesson is seen with others.
        for i in range(0, len(group), BATCH // 2):
            window = group[i : i + BATCH]
            if len(window) < 2:
                break
            for c in check(llm, domain, window, tier=tier):
                found.append({"domain": domain, **c.model_dump()})
        print(f"  {domain}: {len(group)} lessons checked", flush=True)
    # The same pair can surface in two overlapping windows.
    seen, unique = set(), []
    for c in found:
        key = (tuple(sorted(c["topics"])), c["disagreement"][:60])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique
