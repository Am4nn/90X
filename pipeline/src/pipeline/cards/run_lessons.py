"""Generate cards from lessons, gate them, and save per topic.

Per-topic saving, again because the first card run lost 278 sources of work
to one interruption. Rejected cards are kept with their reason rather than
deleted: a rejection rate that climbs is the signal that the generator or the
lessons have drifted, and that is invisible if failures are thrown away.
"""

import json
import threading
import uuid
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from ..llm import LLM, BudgetExceeded, LLMError, spend_usd
from . import gate
from .from_lessons import for_lesson

WORKERS = 4
# Fixed namespace so a card id is stable across runs.
CARD_NAMESPACE = uuid.UUID("90c0de00-0000-4000-8000-000000000001")


def topics_with_lessons(con, only: list[str] | None, limit: int | None, redo: bool) -> list[dict]:
    rows = con.execute(
        """
        select t.slug, t.name, t.domain, t.importance, l.body_md
        from lessons l join topics t on t.slug = l.topic_slug
        where l.status = 'ok'
          and (? or t.slug not in (select topic_slug from cards where topic_slug is not null and source = 'lesson'))
        order by t.importance desc, t.slug
        """,
        [redo],
    ).fetchall()
    out = [dict(zip(["slug", "name", "domain", "importance", "lesson"], r)) for r in rows]
    if only:
        out = [t for t in out if t["slug"] in set(only)]
    return out[:limit] if limit else out


def one(llm: LLM, topic: dict, tier: str = "smart") -> tuple[list, list[tuple[object, str]], dict]:
    cards = for_lesson(llm, topic, topic["lesson"], tier=tier)
    result = gate.review(llm, topic, cards)
    rejected = gate.judge(cards, result)
    bad = {id(c) for c, _ in rejected}
    confidence = {id(c): gate.confidence_of(result).get(i, 0.5) for i, c in enumerate(cards)}
    return [c for c in cards if id(c) not in bad], rejected, confidence


def save(con, topic: dict, kept: list, rejected: list[tuple[object, str]], confidence: dict) -> None:
    now = datetime.now(timezone.utc)
    con.execute("delete from cards where topic_slug = ? and source = 'lesson'", [topic["slug"]])
    rows = [(c, None) for c in kept] + [(c, reason) for c, reason in rejected]
    # kept, quality and source_refs are what /admin/cards reads: without them a
    # lesson card never reaches the review screen, which is where Aman looks.
    refs = json.dumps([{"kind": "lesson", "id": topic["slug"], "title": topic["name"]}])
    # public.cards.id is a uuid, so a readable "slug:l0" id would never publish.
    # uuid5 keeps it deterministic: regenerating a topic reuses the same ids.
    for i, (card, reason) in enumerate(rows):
        con.execute(
            """insert or replace into cards
               (id, topic_slug, format, difficulty, prompt_md, options, answer_md, key_points,
                source_refs, quality, kept, status, source, reject_reason, created_at)
               values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'lesson', ?, ?)""",
            [
                str(uuid.uuid5(CARD_NAMESPACE, f"{topic['slug']}:{i}")), topic["slug"], card.format, card.difficulty, card.prompt,
                json.dumps(card.options) if card.options else None, card.answer,
                json.dumps(card.key_points), refs,
                json.dumps({"gate_confidence": confidence.get(id(card), 0.5)}),
                reason is None, "rejected" if reason else "draft", reason, now,
            ],
        )


def run(con, only: list[str] | None = None, limit: int | None = None, redo: bool = False,
        tier: str = "smart", llm: LLM | None = None) -> tuple[int, int]:
    llm = llm or LLM(con)
    todo = topics_with_lessons(con, only, limit, redo)
    started, before = time.time(), spend_usd(con)
    db = threading.Lock()
    kept_total = rejected_total = done = 0

    print(f"{len(todo)} topics with lessons, {WORKERS} at a time", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(one, llm, t, tier): t for t in todo}
        try:
            for future in as_completed(futures):
                topic = futures[future]
                try:
                    kept, rejected, confidence = future.result()
                except BudgetExceeded as e:
                    print(f"  stopping: {e}", flush=True)
                    break
                except LLMError as e:
                    print(f"{topic['slug']}: FAILED {e}", flush=True)
                    continue
                except Exception as e:
                    # One provider error must not cancel the topics in flight.
                    print(f"{topic['slug']}: FAILED {type(e).__name__}: {e}", flush=True)
                    continue
                with db:
                    save(con, topic, kept, rejected, confidence)
                    spent = spend_usd(con) - before
                done += 1
                kept_total += len(kept)
                rejected_total += len(rejected)
                share = rejected_total / max(1, kept_total + rejected_total)
                print(
                    f"[{done}/{len(todo)}] {topic['slug']}  kept {len(kept)}  rejected {len(rejected)}  "
                    f"(rejected {share:.0%} so far)  ${spent:.3f}  {int(time.time() - started)}s",
                    flush=True,
                )
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
    return kept_total, rejected_total
