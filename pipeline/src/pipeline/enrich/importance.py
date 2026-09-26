"""Importance of a problem, 0-1: how likely it is to matter in an interview.

Weights: curated lists (NeetCode 150 / Blind 75) 0.5, company demand 0.4
(peak frequency 0.3 + how many companies ask it 0.1), popularity 0.1."""

import json
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Stats:
    max_accepted: int
    max_companies: int


def score(nc150: bool, blind75: bool, companies: dict, total_accepted: int | None, stats: Stats) -> float:
    curated = (0.35 if nc150 else 0) + (0.15 if blind75 else 0)
    freqs = [f for f in (companies or {}).values() if f is not None]
    peak = (max(freqs) / 100 * 0.3) if freqs else 0
    breadth = (math.log1p(len(freqs)) / math.log1p(stats.max_companies) * 0.1) if freqs and stats.max_companies else 0
    popular = 0.0
    if total_accepted and stats.max_accepted > 1:
        popular = math.log10(max(total_accepted, 1)) / math.log10(stats.max_accepted) * 0.1
    return round(min(1.0, curated + peak + breadth + popular), 4)


def run(con) -> int:
    rows = con.execute("select slug, nc150, blind75, companies, total_accepted from problems").fetchall()
    parsed = [(slug, nc, b75, json.loads(c) if c else {}, acc) for slug, nc, b75, c, acc in rows]
    stats = Stats(
        max_accepted=max((acc or 0) for *_, acc in parsed) or 1,
        max_companies=max((len(c) for _, _, _, c, _ in parsed), default=1) or 1,
    )
    con.executemany(
        "update problems set importance = ? where slug = ?",
        [[score(nc, b75, c, acc, stats), slug] for slug, nc, b75, c, acc in parsed],
    )
    return len(parsed)
