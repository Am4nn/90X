"""Trick catalog per pattern for pattern lessons (spec 6.11). DeepSeek Pro
reads the pattern's most important problems and their reference solutions
and names the reusable tricks; each trick links only to problems we have."""

import hashlib
import json

from pydantic import BaseModel, Field

SYSTEM = """You write the trick catalog for one algorithmic pattern in an interview-prep app.
From the problems and reference solutions given, list the reusable tricks an interviewer expects someone
to know for this pattern: 3-8 tricks, most important first.
For each: a short name, the idea in 1-3 sentences (why it works), a minimal Python snippet (a few lines, not a
full solution), and 1-3 problem slugs from the list that use it. Only use slugs from the list."""


class Trick(BaseModel):
    name: str
    idea: str
    snippet: str
    problems: list[str] = Field(min_length=1, max_length=3)


class Catalog(BaseModel):
    tricks: list[Trick] = Field(min_length=1, max_length=8)


def build(con, llm, patterns: list[tuple[str, str]] | None = None, per_pattern_problems: int = 12) -> int:
    patterns = patterns or con.execute("select slug, name from topics where domain = 'dsa' order by sort").fetchall()
    total = 0
    for slug, name in patterns:
        problems = con.execute(
            """select slug, title, solutions from problems
               where pattern_slug = ? and kind = 'leetcode' and statement_md is not null
               order by importance desc limit ?""", [slug, per_pattern_problems]
        ).fetchall()
        if not problems:
            continue
        listing = "\n\n".join(
            f"slug: {s}\ntitle: {t}\nsolution:\n{(json.loads(sol or '{}').get('python') or '')[:1200]}" for s, t, sol in problems
        )
        catalog = llm.complete_json(SYSTEM, f"Pattern: {name}\n\n{listing}", Catalog, tier="smart", purpose="tricks")
        known = {s for s, _, _ in problems}
        con.execute("delete from pattern_tricks where pattern_slug = ?", [slug])
        for i, t in enumerate(catalog.tricks):
            links = [p for p in t.problems if p in known]
            if not links:
                continue
            con.execute(
                "insert into pattern_tricks (id, pattern_slug, name, idea_md, snippets, problem_slugs, sort) values (?, ?, ?, ?, ?, ?, ?)",
                [f"{slug}:{hashlib.sha1(t.name.encode()).hexdigest()[:8]}", slug, t.name, t.idea,
                 json.dumps({"python": t.snippet}), links, i],
            )
            total += 1
    return total
