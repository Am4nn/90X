"""Generate cards from lessons, one named archetype at a time, and save per topic.

Feed v2 replaces the writer that chose its own format. The budget decides the
mix up front (`archetypes.budget`), and the writer is asked for exactly one
archetype per call and may refuse. A refusal refills the slot with the next
eligible archetype — a strained ordering card is worse than an absent one.

Per-topic saving, again because the first card run lost 278 sources of work to
one interruption. Cards are saved as drafts; the blind gate (part F) judges them
later, so nothing is rejected or repaired here.
"""

import json
import uuid
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from ..llm import LLM, BudgetExceeded, LLMError, lock_for, spend_usd
from . import archetypes, write
from .archetypes import CardSlot

WORKERS = 12
# Topics in flight. Like the lesson run, a worker spends its time waiting on
# an HTTP response, so the ceiling is the provider's rate limit, not our cores.
# Fixed namespace so a card id is stable across runs.
CARD_NAMESPACE = uuid.UUID("90c0de00-0000-4000-8000-000000000001")

# Hard cards may draw on problem statements and pattern tricks, not only the
# lesson; a three-step question needs a concrete situation. Capped so the prompt
# stays about the lesson rather than becoming a stack of problem statements.
MAX_PROBLEMS = 6
MAX_TRICKS = 6
MAX_PROBLEM_CHARS = 1200


def card_id(topic_slug: str, prompt: str, kind: str = "") -> str:
    """A card's identity is its question, not where it landed in the list.

    Keying on position meant a card's id moved whenever the gate changed its
    mind about an earlier card, so published study history could end up
    attached to a different question. The question is what the reader answered,
    so the question is the identity.

    `kind` separates a row that is not a card from the card it describes.
    """
    prefix = f"{kind}:" if kind else ""
    return str(uuid.uuid5(CARD_NAMESPACE, f"{prefix}{topic_slug}:{' '.join(prompt.split())}"))


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


def hard_sources(con, slug: str, domain: str) -> dict:
    """The problem statements and pattern tricks a Hard card may draw on.

    Only DSA topics have them: a pattern's problems and its trick catalog. The
    source refs credit these on the cards that use them, so the reader's
    "Written from" line and the problem link both stay honest.
    """
    if domain != "dsa":
        return {"problems": [], "tricks": []}
    problems = [
        dict(zip(["slug", "title", "difficulty", "statement"], r))
        for r in con.execute(
            """select slug, title, difficulty, statement_md from problems
               where pattern_slug = ? and kind = 'leetcode'
                 and length(coalesce(statement_md, '')) > 200
               order by (nc150 or blind75) desc, importance desc limit ?""",
            [slug, MAX_PROBLEMS],
        ).fetchall()
    ]
    tricks = [
        dict(zip(["id", "name", "idea"], r))
        for r in con.execute(
            "select id, name, idea_md from pattern_tricks where pattern_slug = ? order by sort limit ?",
            [slug, MAX_TRICKS],
        ).fetchall()
    ]
    return {"problems": problems, "tricks": tricks}


def hard_text(hard: dict) -> str:
    parts = [f"Problem: {p['title']} ({p['difficulty']})\n{(p['statement'] or '')[:MAX_PROBLEM_CHARS]}"
             for p in hard["problems"]]
    parts += [f"Pattern trick — {t['name']}:\n{t['idea']}" for t in hard["tricks"]]
    return "\n\n".join(parts)


def _refill_order(slot: CardSlot, eligible: list[archetypes.Archetype]) -> list[archetypes.Archetype]:
    """The slot's archetype first, then the rest, skipping ones that cannot
    carry the slot's difficulty target."""
    ids = [a.id for a in eligible]
    start = ids.index(slot.archetype) if slot.archetype in ids else 0
    ordered = eligible[start:] + eligible[:start]
    return [a for a in ordered if slot.difficulty in a.difficulties]


def write_topic(llm, topic: dict, lesson_md: str, slots: list[CardSlot], hard_material: str,
                tier: str = "smart", progress: bool = False, thinking: bool = False) -> tuple[list, list]:
    """Write a topic's budget, refilling refusals with the next eligible
    archetype. Returns (cards, refused_slots)."""
    eligible = archetypes.eligible(topic["domain"])
    written, refused = [], []
    for i, slot in enumerate(slots):
        card = _write_with_refill(llm, topic, lesson_md, slot, hard_material, tier, eligible, thinking)
        if card is None:
            refused.append(slot)
            if progress:
                print(f"    [{i + 1}/{len(slots)}] {slot.archetype} ({slot.difficulty}) -> refused", flush=True)
        else:
            written.append(card)
            if progress:
                print(f"    [{i + 1}/{len(slots)}] {slot.archetype} ({slot.difficulty}) -> {card.format}", flush=True)
    return written, refused


def _write_with_refill(llm, topic: dict, lesson_md: str, slot: CardSlot, hard_material: str,
                       tier: str, eligible: list[archetypes.Archetype], thinking: bool = False):
    # Hard material is for Hard cards; an Easy card should not read problems.
    mat = hard_material if slot.difficulty == "Hard" else ""
    for a in _refill_order(slot, eligible):
        primitive = slot.primitive if a.id == slot.archetype else archetypes.pick_primitive(a, 0)
        result = write.write_one(llm, topic, lesson_md, CardSlot(a.id, primitive, slot.difficulty), mat, tier,
                                 thinking=thinking)
        if isinstance(result, write.Card):
            return result
    return None


def _refs(topic: dict, hard: dict, difficulty: str) -> str:
    refs = [{"kind": "lesson", "id": topic["slug"], "title": topic["name"]}]
    if difficulty == "Hard":
        refs += [{"kind": "problem", "id": p["slug"], "title": p["title"]} for p in hard["problems"]]
        refs += [{"kind": "trick", "id": t["id"], "title": t["name"]} for t in hard["tricks"]]
    return json.dumps(refs)


def save(con, topic: dict, cards: list, hard: dict) -> None:
    now = datetime.now(timezone.utc)
    con.execute("delete from cards where topic_slug = ? and source = 'lesson'", [topic["slug"]])
    for card in cards:
        con.execute(
            """insert or replace into cards
               (id, topic_slug, format, archetype, difficulty, prompt_md, options, answer_md, key_points,
                picked, constraints, pairs, value, tolerance, why_step,
                source_refs, quality, kept, status, source, created_at)
               values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'lesson', ?)""",
            [
                card_id(topic["slug"], card.prompt),
                topic["slug"], card.format, card.archetype, card.difficulty, card.prompt,
                json.dumps(card.options) if card.options else None, card.answer,
                json.dumps(card.key_points),
                json.dumps(card.picked) if card.picked else None,
                # Part B's grader reads constraints as {"before": [[a, b], ...]},
                # so the flat [[a, b], ...] the writer returns is wrapped here.
                json.dumps({"before": card.constraints}) if card.constraints else None,
                json.dumps(card.pairs) if card.pairs else None,
                card.value, card.tolerance,
                json.dumps(card.why_step.model_dump()) if card.why_step else None,
                _refs(topic, hard, card.difficulty),
                json.dumps({}),
                True, "draft", now,
            ],
        )


def run(con, only: list[str] | None = None, limit: int | None = None, redo: bool = False,
        tier: str = "smart", llm: LLM | None = None) -> tuple[int, int]:
    """Generate every topic's budget and save the cards as drafts. Returns
    (cards_written, slots_refused)."""
    llm = llm or LLM(con)
    todo = topics_with_lessons(con, only, limit, redo)
    started, before = time.time(), spend_usd(con)
    db = lock_for(con)
    written_total = refused_total = done = 0

    print(f"{len(todo)} topics with lessons, {WORKERS} at a time", flush=True)

    def work(topic: dict):
        with db:
            hard = hard_sources(con, topic["slug"], topic["domain"])
        slots = archetypes.budget(topic)
        if not slots:
            return topic, [], [], hard
        cards, refused = write_topic(llm, topic, topic["lesson"], slots, hard_text(hard), tier)
        return topic, cards, refused, hard

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(work, t): t for t in todo}
        try:
            for future in as_completed(futures):
                topic = futures[future]
                try:
                    topic, cards, refused, hard = future.result()
                except BudgetExceeded as e:
                    print(f"  stopping: {e}", flush=True)
                    break
                except LLMError as e:
                    print(f"{topic['slug']}: FAILED {e}", flush=True)
                    continue
                except Exception as e:
                    print(f"{topic['slug']}: FAILED {type(e).__name__}: {e}", flush=True)
                    continue
                if not cards and not refused:
                    continue  # a domain the catalogue does not cover
                with db:
                    save(con, topic, cards, hard)
                    spent = spend_usd(con) - before
                done += 1
                written_total += len(cards)
                refused_total += len(refused)
                print(f"[{done}/{len(todo)}] {topic['slug']}  wrote {len(cards)}  refused {len(refused)}  "
                      f"${spent:.3f}  {int(time.time() - started)}s", flush=True)
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
    return written_total, refused_total
