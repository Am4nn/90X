"""Judge the cards we already have, again.

When the gate changes, the cards do not need rewriting - they need re-judging.
Regenerating them instead would be both dearer and worse: it throws away the
cards a human reviewer has already read and approved, and replaces them with
questions nobody has seen.

It also runs in the other direction, which is the point. A card the old gate
rejected is still here with its reason, so a gate that was wrong to reject it
can take it back. The old gate turned down a valid `output` card for a format
rule it invented; nothing else would have recovered that card.
"""

import json
from datetime import datetime, timezone

from ..llm import LLM, BudgetExceeded, LLMError, lock_for, spend_usd
from . import gate
from .run_lessons import WORKERS, card_id

from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class Draft:
    """A stored card in the shape the gate expects."""

    def __init__(self, row) -> None:
        (self.id, self.topic_slug, self.format, self.difficulty, self.prompt,
         options, self.answer, key_points, self.status) = row
        self.options = json.loads(options) if options else []
        self.key_points = json.loads(key_points or "[]")


def topics_with_cards(con, only: list[str] | None = None) -> list[dict]:
    rows = con.execute(
        """select t.slug, t.name, t.domain from topics t
           where exists (select 1 from cards c where c.topic_slug = t.slug and c.source = 'lesson'
                         and c.status in ('draft', 'rejected'))
           order by t.importance desc, t.slug"""
    ).fetchall()
    out = [{"slug": s, "name": n, "domain": d} for s, n, d in rows]
    return [t for t in out if t["slug"] in set(only)] if only else out


def cards_of(con, slug: str) -> list[Draft]:
    """Drafts and rejects together: both are up for re-judgement.

    A `repaired` row is left out - it is the record of a wording that was
    already replaced, not a candidate.
    """
    rows = con.execute(
        """select id, topic_slug, format, difficulty, prompt_md, options, answer_md, key_points, status
           from cards where source = 'lesson' and topic_slug = ? and status in ('draft', 'rejected')
           order by status, id""",
        [slug],
    ).fetchall()
    return [Draft(r) for r in rows]


def apply(con, cards: list[Draft], rejected: list[tuple[object, str]], confidence: dict) -> tuple[int, int]:
    """Write the new verdicts. Returns (recovered, newly_rejected)."""
    now = datetime.now(timezone.utc)
    reasons = {id(c): r for c, r in rejected}
    recovered = newly_rejected = 0
    for card in cards:
        reason = reasons.get(id(card))
        status = "rejected" if reason else "draft"
        if status == "draft" and card.status == "rejected":
            recovered += 1
        elif status == "rejected" and card.status == "draft":
            newly_rejected += 1
        con.execute(
            """update cards set status = ?, kept = ?, reject_reason = ?,
                   quality = json_merge_patch(coalesce(quality, '{}'), ?), created_at = ?
               where id = ?""",
            [status, reason is None, reason,
             json.dumps({"gate_confidence": confidence.get(id(card), 0.5), "regated": True}),
             now, card.id],
        )
    return recovered, newly_rejected


def run(con, only: list[str] | None = None, tier: str = "review", llm: LLM | None = None) -> dict:
    llm = llm or LLM(con)
    todo = topics_with_cards(con, only)
    db = lock_for(con)
    started, before = time.time(), spend_usd(con)
    totals = {"topics": 0, "judged": 0, "recovered": 0, "newly_rejected": 0, "rejected": 0}

    def work(topic: dict):
        with db:
            cards = cards_of(con, topic["slug"])
        if not cards:
            return topic, [], [], {}
        result = gate.review(llm, topic, cards, tier=tier)
        return topic, cards, gate.judge(cards, result), gate.confidence_of(result)

    print(f"{len(todo)} topics to re-judge, {WORKERS} at a time", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(work, t): t for t in todo}
        try:
            for future in as_completed(futures):
                topic = futures[future]
                try:
                    topic, cards, rejected, confidence = future.result()
                except BudgetExceeded as e:
                    print(f"  stopping: {e}", flush=True)
                    break
                except (LLMError, Exception) as e:
                    print(f"{topic['slug']}: FAILED {type(e).__name__}: {e}", flush=True)
                    continue
                if not cards:
                    continue
                with db:
                    recovered, newly = apply(con, cards, rejected, confidence)
                    spent = spend_usd(con) - before
                totals["topics"] += 1
                totals["judged"] += len(cards)
                totals["recovered"] += recovered
                totals["newly_rejected"] += newly
                totals["rejected"] += len(rejected)
                if recovered or newly:
                    print(f"  {topic['slug']}: +{recovered} recovered, -{newly} newly rejected", flush=True)
                if totals["topics"] % 25 == 0:
                    print(f"[{totals['topics']}/{len(todo)}] {totals['judged']} judged, "
                          f"+{totals['recovered']} / -{totals['newly_rejected']}  ${spent:.3f}  "
                          f"{int(time.time() - started)}s", flush=True)
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
    return totals
