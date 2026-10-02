"""Bring an already-written topic in line with the budget it should have had.

The first full run wrote every topic's slots from a round-robin that never
rotated, so the corpus came out at 173 cards for one archetype and 1 for another.
`archetypes.budget` is fixed, but 2,401 cards were written under the old
rotation and regenerating all of them would pay twice for work that is mostly
fine. So this reconciles instead: for each topic, compare the archetypes it has
against the archetypes it should have, drop the surplus and write only the
shortfall.

Dropping is by gate confidence, lowest first: when a topic holds six `concept`
cards and the budget calls for two, the two the gate was most sure of are the
ones worth keeping. Within the same confidence the harder card wins, because the
corpus was rebuilt to answer a reviewer who said it was too easy.

A topic the catalogue did not cover before and does now (`ai`, `lld`,
`behavioral`) has no cards at all, so for those every slot is a shortfall and
this is simply the generation run.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone

from . import archetypes
from .archetypes import CardSlot

# Keep the hardest card when confidence ties: the rebuild exists because the old
# corpus was 0.9% Hard.
_DIFFICULTY_RANK = {"Hard": 0, "Medium": 1, "Easy": 2}


def _held(con, slug: str) -> list[tuple[str, str, float, str]]:
    """`(id, archetype, gate_confidence, difficulty)` for a topic's live drafts,
    worst first, so a trim can take from the front."""
    rows = con.execute(
        """select id, archetype, quality, difficulty from cards
           where source = 'lesson' and topic_slug = ? and status = 'draft'
             and archetype is not null and kept""",
        [slug],
    ).fetchall()
    out = []
    for card_id, archetype, quality, difficulty in rows:
        confidence = 0.0
        if quality:
            try:
                confidence = float(json.loads(quality).get("gate_confidence") or 0.0)
            except (ValueError, TypeError):
                confidence = 0.0
        out.append((card_id, archetype, confidence, difficulty or ""))
    out.sort(key=lambda r: (r[2], -_DIFFICULTY_RANK.get(r[3], 1)))
    return out


def plan_topic(con, topic: dict, start: int) -> tuple[list[CardSlot], list[str]]:
    """`(slots to write, card ids to drop)` for one topic.

    The comparison is per archetype rather than per slot: a slot names an
    archetype, a primitive and a difficulty target, but a card already written
    for the right archetype is not worth rewriting because the budget would now
    have asked for it at a different difficulty.
    """
    slots = archetypes.budget(topic, start)
    if not slots:
        return [], []
    want = Counter(slot.archetype for slot in slots)
    held = _held(con, topic["slug"])
    have = Counter(archetype for _, archetype, _, _ in held)

    drop: list[str] = []
    for archetype, n in have.items():
        excess = n - want.get(archetype, 0)
        if excess > 0:
            drop += [card_id for card_id, a, _, _ in held if a == archetype][:excess]

    by_archetype: defaultdict[str, list[CardSlot]] = defaultdict(list)
    for slot in slots:
        by_archetype[slot.archetype].append(slot)
    write: list[CardSlot] = []
    for archetype, wanted in by_archetype.items():
        shortfall = len(wanted) - have.get(archetype, 0)
        if shortfall > 0:
            write += wanted[-shortfall:]
    return write, drop


def plan(con, only: list[str] | None = None) -> dict[str, tuple[dict, list[CardSlot], list[str]]]:
    """Every topic's `(topic, slots to write, ids to drop)`, skipping the settled."""
    from .run_lessons import slot_starts, topics_with_lessons

    starts = slot_starts(con)
    out: dict[str, tuple[dict, list[CardSlot], list[str]]] = {}
    for topic in topics_with_lessons(con, only, None, redo=True):
        write, drop = plan_topic(con, topic, starts.get(topic["slug"], 0))
        if write or drop:
            out[topic["slug"]] = (topic, write, drop)
    return out


def summarise(plan_rows: dict[str, tuple[dict, list[CardSlot], list[str]]]) -> str:
    by_area: defaultdict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for topic, write, drop in plan_rows.values():
        row = by_area[topic.get("domain", "?")]
        row[0] += 1
        row[1] += len(write)
        row[2] += len(drop)
    lines = [f"{'area':16} {'topics':>7} {'to write':>9} {'to drop':>8}"]
    for area in sorted(by_area, key=lambda a: -by_area[a][1]):
        topics, write, drop = by_area[area]
        lines.append(f"{area:16} {topics:7} {write:9} {drop:8}")
    total = [sum(r[i] for r in by_area.values()) for i in range(3)]
    lines.append(f"{'TOTAL':16} {total[0]:7} {total[1]:9} {total[2]:8}")
    return "\n".join(lines)


def drop_cards(con, ids: list[str]) -> int:
    """Retire a surplus card rather than deleting it, so a trim stays auditable
    and a card dropped for being surplus is not confused with one the gate
    rejected."""
    if not ids:
        return 0
    con.executemany(
        """update cards set status = 'rejected', kept = false,
                  reject_reason = 'surplus: the budget asks for fewer of this archetype'
           where id = ?""",
        [[card_id] for card_id in ids],
    )
    return len(ids)


def save_additional(con, topic: dict, cards: list, hard: dict) -> int:
    """Insert newly written cards without touching the topic's existing ones.

    `run_lessons.save` deletes a topic's lesson cards before inserting, which is
    right for a full rewrite and catastrophic here: it would delete the cards
    this reconciliation decided to keep.
    """
    from .run_lessons import _refs, card_id

    now = datetime.now(timezone.utc)
    for card in cards:
        # A card's id is a hash of its topic and its question, so two cards whose
        # questions came out the same collide. `insert or replace` then silently
        # overwrote one with the other: a topic's shortfall could never be filled,
        # every retry re-paid for cards that replaced each other, and the three
        # rebalance passes wrote 3,355 cards against a 2,918 shortfall before the
        # budget ran out. A repeated question gets a distinct id instead, so the
        # slot is actually filled and the duplicate is left for the dedupe pass in
        # `validate` to judge on content rather than lost by accident.
        new_id = card_id(topic["slug"], card.prompt)
        taken = con.execute("select 1 from cards where id = ?", [new_id]).fetchone()
        for attempt in range(2, 12):
            if not taken:
                break
            new_id = card_id(topic["slug"], card.prompt, kind=f"dup{attempt}")
            taken = con.execute("select 1 from cards where id = ?", [new_id]).fetchone()
        if taken:
            continue  # eleven identical questions for one topic: stop writing them
        con.execute(
            """insert into cards
               (id, topic_slug, format, archetype, difficulty, prompt_md, options, answer_md, key_points,
                picked, constraints, pairs, value, tolerance, why_step,
                source_refs, quality, kept, status, source, created_at)
               values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'lesson', ?)""",
            [
                new_id,
                topic["slug"], card.format, card.archetype, card.difficulty, card.prompt,
                json.dumps(card.options) if card.options else None, card.answer,
                json.dumps(card.key_points),
                json.dumps(card.picked) if card.picked else None,
                json.dumps({"before": card.constraints}) if card.constraints else None,
                json.dumps(card.pairs) if card.pairs else None,
                card.value, card.tolerance,
                json.dumps(card.why_step.model_dump()) if card.why_step else None,
                _refs(topic, hard, card.difficulty),
                json.dumps({}),
                True, "draft", now,
            ],
        )
    return len(cards)


def run(con, only: list[str] | None = None, tier: str = "smart", llm=None,
        dry_run: bool = True) -> tuple[int, int, int]:
    """Trim every topic's surplus and write its shortfall.

    Returns `(written, dropped, refused)`. Mirrors `run_lessons.run`: the same
    worker count, the same budget stop, the same per-topic save under the lock,
    so a run that stops on spend keeps everything it finished.
    """
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed

    from ..llm import LLM, BudgetExceeded, LLMError, lock_for, spend_usd
    from .run_lessons import WORKERS, hard_sources, hard_text, write_topic

    rows = plan(con, only)
    print(summarise(rows) + "\n")
    if dry_run:
        print("dry run: nothing written. Re-run with --apply.")
        return 0, 0, 0

    llm = llm or LLM(con)
    db = lock_for(con)
    started, before = time.time(), spend_usd(con, getattr(llm, "run_id", None))
    written = dropped = refused = 0

    # Trimming needs no model, so it happens first and in one pass: if the write
    # half stops on budget, the corpus is already the right shape minus the
    # cards that were never written, rather than carrying both the surplus and a
    # partial top-up.
    with db:
        for _, (_, _, drop) in rows.items():
            dropped += drop_cards(con, drop)
    print(f"trimmed {dropped} surplus cards\n", flush=True)

    todo = [(topic, slots) for topic, slots, _ in rows.values() if slots]

    def work(item):
        topic, slots = item
        with db:
            hard = hard_sources(con, topic["slug"], topic["domain"])
        cards, refusals = write_topic(llm, topic, topic["lesson"], slots, hard_text(hard), tier)
        return topic, cards, refusals, hard

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(work, item): item[0] for item in todo}
        done = 0
        try:
            for future in as_completed(futures):
                topic = futures[future]
                try:
                    topic, cards, refusals, hard = future.result()
                except BudgetExceeded as e:
                    print(f"  stopping: {e}", flush=True)
                    break
                except LLMError as e:
                    print(f"{topic['slug']}: FAILED {e}", flush=True)
                    continue
                except Exception as e:
                    print(f"{topic['slug']}: FAILED {type(e).__name__}: {e}", flush=True)
                    continue
                with db:
                    written += save_additional(con, topic, cards, hard)
                    spent = spend_usd(con, getattr(llm, "run_id", None)) - before
                refused += len(refusals)
                done += 1
                print(f"[{done}/{len(todo)}] {topic['slug']}  wrote {len(cards)}  refused {len(refusals)}  "
                      f"${spent:.3f}  {int(time.time() - started)}s", flush=True)
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
    return written, dropped, refused
