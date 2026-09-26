"""A curated ~300-problem competitive subset for the Library.

Pool: APPS 'interview' + TACO EASY/MEDIUM problems with a Python reference
solution (one row per problem; test cases are never read). A sample is
triaged by Flash for how interview-like it is; the best are kept, capped per
pattern so the set stays balanced."""

import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Literal

import duckdb
from pydantic import BaseModel, Field

from ..config import DATA_DIR
from ..enrich.patterns import TECHNIQUES, PatternName
from .dsa import pattern_slug, strip_fence

PARQUET = str(DATA_DIR / "competitive" / "primeintellect-verifiable" / "data" / "*.parquet")
MIN_SCORE = 4

TRIAGE_SYSTEM = """You screen competitive-programming problems for a software-engineering interview-prep app.
interview_like 1-5: 5 = could be asked in a coding interview as is (clear statement, a standard technique,
solvable in 30-45 minutes); 1 = contest-only (heavy math, obscure tricks, long input formats).
title: a short descriptive title (3-6 words). difficulty: as an interview problem.
pattern: one primary pattern; techniques: 1-4 from the allowed list."""

Technique = Literal[TECHNIQUES]  # type: ignore[valid-type]


class Triage(BaseModel):
    interview_like: int = Field(ge=1, le=5)
    title: str = Field(min_length=3, max_length=80)
    difficulty: Literal["Easy", "Medium", "Hard"]
    pattern: PatternName
    techniques: list[Technique] = Field(min_length=1, max_length=4)


def clean_statement(prompt: str) -> str:
    text = re.sub(r"^Solve the following coding problem using the programming language \w+:\s*", "", prompt.strip())
    return re.sub(r"\n+The input will be (stdin|given via stdin).*$", "", text, flags=re.S).strip()


def slug_for(source: str, source_id: str, title: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50]
    return f"cp-{base}-{hashlib.sha1(f'{source}:{source_id}'.encode()).hexdigest()[:6]}"


def candidates(limit: int = 2000) -> list[dict]:
    con = duckdb.connect()
    rows = con.execute(f"""
        with pool as (
          select source, in_source_id, prompt, gold_standard_solution as solution,
                 regexp_extract(metadata, 'difficulty'': ''([^'']+)', 1) as diff,
                 regexp_extract(metadata, 'problem_url'': ''([^'']+)', 1) as url,
                 row_number() over (partition by in_source_id order by length(prompt)) as rn
          from read_parquet('{PARQUET}')
          where prompt like '%programming language python%'
            and gold_standard_solution <> 'None'
            and ((source = 'apps' and metadata like '%''interview''%')
                 or (source = 'taco' and (metadata like '%''EASY''%' or metadata like '%''MEDIUM''%')))
            and length(prompt) between 500 and 3500
        )
        select source, in_source_id, prompt, solution, diff, url from pool
        where rn = 1 and coalesce(url, '') not like '%leetcode.com%'  -- already in the main catalog
        order by hash(in_source_id) limit {int(limit)}
    """).fetchall()
    return [{"source": s, "id": i, "statement": clean_statement(p), "solution": strip_fence(sol), "url": u or None}
            for s, i, p, sol, _, u in rows]


def triage(llm, pool: list[dict], workers: int = 8) -> list[dict]:
    def one(c):
        user = f"Problem:\n{c['statement'][:3000]}\n\nReference solution:\n{c['solution'][:2000]}\n\nAllowed techniques: {', '.join(TECHNIQUES)}"
        return {**c, "triage": llm.complete_json(TRIAGE_SYSTEM, user, Triage, tier="fast", purpose="competitive-triage")}

    out = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for f in as_completed([ex.submit(one, c) for c in pool]):
            try:
                out.append(f.result())
            except Exception as e:
                print(f"  skip: {e}", flush=True)
            if len(out) % 250 == 0:
                print(f"  triaged {len(out)}/{len(pool)}", flush=True)
    return out


def select(triaged: list[dict], keep: int = 300, per_pattern: int = 25) -> list[dict]:
    ranked = sorted((c for c in triaged if c["triage"].interview_like >= MIN_SCORE),
                    key=lambda c: (-c["triage"].interview_like, c["id"]))
    chosen, counts = [], {}
    for c in ranked:
        p = c["triage"].pattern
        if counts.get(p, 0) < per_pattern:
            chosen.append(c)
            counts[p] = counts.get(p, 0) + 1
        if len(chosen) == keep:
            break
    return chosen


def run(con, llm, pool_size: int = 2000, keep: int = 300) -> int:
    chosen = select(triage(llm, candidates(pool_size)), keep=keep)
    con.execute("delete from problems where kind = 'competitive'")
    con.executemany(
        """insert into problems (slug, kind, title, difficulty, pattern_slug, pattern_source, techniques, topic_slugs, tags,
               importance, companies, statement_md, solutions, url, source_id, premium)
           values (?, 'competitive', ?, ?, ?, 'ai', ?, [], [], ?, '{}', ?, ?, ?, 'primeintellect-verifiable', false)""",
        [[slug_for(c["source"], c["id"], c["triage"].title), c["triage"].title, c["triage"].difficulty,
          pattern_slug(c["triage"].pattern), list(c["triage"].techniques), c["triage"].interview_like / 10,
          c["statement"], json.dumps({"python": c["solution"]}), c["url"]] for c in chosen],
    )
    return len(chosen)
