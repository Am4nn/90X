"""Tag problems that NeetCode doesn't cover with one of its 18 patterns,
reading the statement and a reference solution (DeepSeek Flash)."""

import csv
import json
from typing import Literal

from pydantic import BaseModel

from ..config import DATA_DIR
from ..normalize.dsa import pattern_slug
from .topics import DSA_PATTERNS

PatternName = Literal[tuple(name for name, _ in DSA_PATTERNS)]  # type: ignore[valid-type]

SYSTEM = (
    "You classify LeetCode problems by the algorithmic pattern an interviewer expects. "
    "Pick exactly one pattern from the allowed list, based on the intended optimal solution."
)


class PatternChoice(BaseModel):
    pattern: PatternName


def _prompt(title: str, statement: str, solutions: dict) -> str:
    code = solutions.get("python") or solutions.get("java") or solutions.get("cpp") or ""
    return (
        f"Problem: {title}\n\n{statement[:3500]}\n\n"
        f"Reference solution:\n{code[:2500]}\n\n"
        f"Allowed patterns: {', '.join(name for name, _ in DSA_PATTERNS)}"
    )


def run(con, llm, limit: int | None = None, workers: int = 8, progress_every: int = 200) -> int:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    rows = con.execute(
        """select slug, title, statement_md, solutions from problems
           where pattern_slug is null and statement_md is not null and kind = 'leetcode'
           order by importance desc""" + (f" limit {int(limit)}" if limit else "")
    ).fetchall()

    def tag(row):
        slug, title, statement, solutions = row
        choice = llm.complete_json(SYSTEM, _prompt(title, statement, json.loads(solutions or "{}")), PatternChoice,
                                   tier="fast", purpose="pattern")
        return slug, pattern_slug(choice.pattern)

    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(tag, row) for row in rows]
        for future in as_completed(futures):
            try:
                slug, pattern = future.result()
            except Exception as e:  # one bad answer shouldn't stop the run
                print(f"  skip: {e}", flush=True)
                continue
            with getattr(llm, "lock", _NoLock()):
                con.execute("update problems set pattern_slug = ?, pattern_source = 'ai' where slug = ?", [pattern, slug])
            done += 1
            if done % progress_every == 0:
                print(f"  tagged {done}/{len(rows)}", flush=True)
    return done


class _NoLock:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def write_sample(con, n: int = 50) -> str:
    """Random AI-tagged problems for a hand check."""
    path = DATA_DIR / "review" / "pattern_sample.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = con.execute(
        "select title, difficulty, pattern_slug, url from problems where pattern_source = 'ai' order by random() limit ?", [n]
    ).fetchall()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["title", "difficulty", "ai_pattern", "url", "correct (y/n)"])
        w.writerows([[*r, ""] for r in rows])
    return str(path)


def evaluate(con, llm, n: int = 40, tier: str = "fast") -> tuple[float, list[tuple[str, str, str]]]:
    """Trial on NeetCode-tagged problems (known answer), writing nothing.
    Returns accuracy and (title, expected, got) for each problem."""
    rows = con.execute(
        """select title, statement_md, solutions, pattern_slug from problems
           where pattern_source = 'neetcode' and statement_md is not null
           order by hash(slug) limit ?""", [n]
    ).fetchall()
    results = []
    for title, statement, solutions, expected in rows:
        choice = llm.complete_json(SYSTEM, _prompt(title, statement, json.loads(solutions or "{}")), PatternChoice,
                                   tier=tier, purpose=f"pattern-trial-{tier}")
        results.append((title, expected, pattern_slug(choice.pattern)))
    correct = sum(1 for _, e, g in results if e == g)
    return (correct / len(results) if results else 0.0), results
