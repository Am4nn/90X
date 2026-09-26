"""Tag algorithm problems with one primary pattern (places the problem on the
Pattern Map) and 1-4 techniques (what the solution actually uses). NeetCode
problems keep NeetCode's pattern and get techniques added."""

import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Literal

from pydantic import BaseModel, Field

from ..config import DATA_DIR
from ..normalize.dsa import pattern_slug
from .topics import DSA_PATTERNS

PATTERN_NAMES = tuple(name for name, _ in DSA_PATTERNS)
PatternName = Literal[PATTERN_NAMES]  # type: ignore[valid-type]

TECHNIQUES = (
    "hash-map", "hash-set", "counting", "sorting", "two-pointers", "sliding-window", "prefix-sum",
    "difference-array", "binary-search", "binary-search-on-answer", "stack", "monotonic-stack", "queue",
    "monotonic-queue", "linked-list", "recursion", "tree-traversal", "bst", "trie", "heap", "greedy",
    "intervals", "backtracking", "bfs", "dfs", "topological-sort", "union-find", "shortest-path",
    "minimum-spanning-tree", "dp-1d", "dp-2d", "dp-bitmask", "dp-interval", "dp-knapsack", "dp-digit",
    "bit-manipulation", "math", "number-theory", "geometry", "combinatorics", "simulation",
    "string-matching", "string-parsing", "matrix", "segment-tree", "fenwick-tree", "design",
    "divide-and-conquer", "iteration",
)
Technique = Literal[TECHNIQUES]  # type: ignore[valid-type]

SYSTEM = """You classify LeetCode problems the way an interview coach would, based on the intended optimal solution.

pattern: exactly one primary pattern from the allowed list. Rules:
- "Arrays & Hashing" only when a hash map / set / counting is central to the solution.
- A plain single pass over an array or string with no special idea is NOT hashing: use "String" for
  string problems, "Simulation" for step-by-step rule following, otherwise the most specific pattern.
- "Math & Geometry" only when the core is a math formula, number theory or geometry. Never use it as a fallback.
- "Prefix Sum" when cumulative sums/xors or difference arrays are the key idea.
- "Segment Tree & Fenwick" for range queries with updates.
- "Matrix / Grid" when the difficulty is navigating a 2-D grid (unless it is clearly BFS/DFS on a graph).
- "Design" when the task is to implement a class / data structure with several operations.

techniques: 1-4 items from the allowed list, the ones the optimal solution actually uses, most important first."""


class PatternTags(BaseModel):
    pattern: PatternName
    techniques: list[Technique] = Field(min_length=1, max_length=4)


def _prompt(title: str, statement: str, solutions: dict) -> str:
    code = solutions.get("python") or solutions.get("java") or solutions.get("cpp") or ""
    return (
        f"Problem: {title}\n\n{statement[:3500]}\n\n"
        f"Reference solution:\n{code[:2500]}\n\n"
        f"Allowed patterns: {', '.join(PATTERN_NAMES)}\n"
        f"Allowed techniques: {', '.join(TECHNIQUES)}"
    )


def untagged(con, limit: int | None = None, retag: bool = False) -> list[tuple]:
    """Algorithm problems (no sql/concurrency area) with a statement that still need tags."""
    where = "techniques is null" if not retag else "true"
    return con.execute(
        f"""select slug, title, statement_md, solutions, pattern_source from problems
            where kind = 'leetcode' and len(coalesce(topic_slugs, [])) = 0 and statement_md is not null
              and {where}
            order by importance desc""" + (f" limit {int(limit)}" if limit else "")
    ).fetchall()


def _tag(llm, row, tier: str = "fast") -> tuple[str, PatternTags]:
    slug, title, statement, solutions, _ = row
    tags = llm.complete_json(SYSTEM, _prompt(title, statement, json.loads(solutions or "{}")), PatternTags,
                             tier=tier, purpose="pattern")
    return slug, tags


class _NoLock:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def run(con, llm, limit: int | None = None, retag: bool = False, workers: int = 8, progress_every: int = 200) -> int:
    rows = untagged(con, limit, retag)
    neetcode = {r[0] for r in rows if r[4] == "neetcode"}
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_tag, llm, row) for row in rows]
        for future in as_completed(futures):
            try:
                slug, tags = future.result()
            except Exception as e:  # one bad answer shouldn't stop the run
                print(f"  skip: {e}", flush=True)
                continue
            with getattr(llm, "lock", _NoLock()):
                if slug in neetcode:  # keep NeetCode's own pattern, add techniques
                    con.execute("update problems set techniques = ? where slug = ?", [list(tags.techniques), slug])
                else:
                    con.execute("update problems set pattern_slug = ?, pattern_source = 'ai', techniques = ? where slug = ?",
                                [pattern_slug(tags.pattern), list(tags.techniques), slug])
            done += 1
            if done % progress_every == 0:
                print(f"  tagged {done}/{len(rows)}", flush=True)
    return done


def trial(con, llm, csv_path, tier: str = "fast") -> str:
    """Re-tag the problems in a reviewed sample CSV without writing to the
    database; write old vs new next to the reviewer's comments."""
    with open(csv_path, encoding="utf-8") as f:
        reviewed = list(csv.DictReader(f))
    by_title = {r[1]: r for r in con.execute(
        "select slug, title, statement_md, solutions, pattern_source, pattern_slug, topic_slugs, premium from problems"
    ).fetchall()}
    out = []
    for r in reviewed:
        row = by_title.get(r["Title"])
        if not row:
            continue
        slug, title, statement, solutions, source, old, areas, premium = row
        note = "Premium" if premium else ""
        if areas:
            new, techniques = "(not tagged: " + ", ".join(areas) + " area)", ""
        else:
            _, tags = _tag(llm, (slug, title, statement, solutions, source), tier)
            new, techniques = pattern_slug(tags.pattern), ", ".join(tags.techniques)
        comment = next((v for k, v in r.items() if k.lower().startswith("correct")), "")
        out.append({"title": title, "your_comment": comment, "old": old, "new": new, "techniques": techniques, "flag": note})
    path = DATA_DIR / "review" / "pattern_retag_trial.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    return str(path)


def write_sample(con, n: int = 50) -> str:
    """Random AI-tagged problems for a hand check."""
    path = DATA_DIR / "review" / "pattern_sample.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = con.execute(
        """select title, difficulty, pattern_slug, array_to_string(techniques, ', '), url from problems
           where pattern_source = 'ai' order by random() limit ?""", [n]
    ).fetchall()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["title", "difficulty", "ai_pattern", "techniques", "url", "correct (y/n)"])
        w.writerows([[*r, ""] for r in rows])
    return str(path)


def evaluate(con, llm, n: int = 40, tier: str = "fast") -> tuple[float, list[tuple[str, str, str]]]:
    """Trial on NeetCode-tagged problems (known answer), writing nothing."""
    rows = con.execute(
        """select slug, title, statement_md, solutions, pattern_source, pattern_slug from problems
           where pattern_source = 'neetcode' and statement_md is not null
           order by hash(slug) limit ?""", [n]
    ).fetchall()
    results = []
    for row in rows:
        _, tags = _tag(llm, row[:5], tier)
        results.append((row[1], row[5], pattern_slug(tags.pattern)))
    correct = sum(1 for _, e, g in results if e == g)
    return (correct / len(results) if results else 0.0), results
