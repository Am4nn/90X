"""Generate cards from lessons, gate them, and save per topic.

Per-topic saving, again because the first card run lost 278 sources of work
to one interruption. Rejected cards are kept with their reason rather than
deleted: a rejection rate that climbs is the signal that the generator or the
lessons have drifted, and that is invisible if failures are thrown away.
"""

import json
import uuid
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from ..llm import LLM, BudgetExceeded, LLMError, lock_for, spend_usd
from . import gate
from .from_lessons import for_lesson, rewrite

WORKERS = 12
# Topics in flight. Like the lesson run, a worker spends its time waiting on
# an HTTP response, so the ceiling is the provider's rate limit, not our cores.
# Fixed namespace so a card id is stable across runs.
CARD_NAMESPACE = uuid.UUID("90c0de00-0000-4000-8000-000000000001")


def card_id(topic_slug: str, prompt: str, kind: str = "") -> str:
    """A card's identity is its question, not where it landed in the list.

    Keying on position meant a card's id moved whenever the gate changed its
    mind about an earlier card, so published study history could end up
    attached to a different question, and `on conflict do nothing` could leave
    the old question sitting under that id. The question is what the reader
    answered, so the question is the identity.

    `kind` separates a row that is not a card from the card it describes. A
    rewrite that fixes only the answer keeps the question, so the replacement
    and the wording the gate objected to had the same id: one overwrote the
    other, and whichever lost took the gate's objection out of the record.
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


def _kept(cards: list, result) -> tuple[list, list[tuple[object, str]], dict]:
    rejected = gate.judge(cards, result)
    bad = {id(c) for c, _ in rejected}
    confidence = {id(c): gate.confidence_of(result).get(i, 0.5) for i, c in enumerate(cards)}
    return [c for c in cards if id(c) not in bad], rejected, confidence


def one(llm: LLM, topic: dict, tier: str = "smart") -> tuple[list, list[tuple[object, str]], list[tuple[object, str]], dict]:
    """Generate, gate, and repair once what the gate turned down.

    The gate says exactly why it rejected each card, which is usually enough
    to fix the wording without changing the idea. Throwing them away instead
    costs roughly 160 cards across a full run.

    Returns (kept, discarded, sent_back, confidence). `sent_back` is what the
    gate objected to on the first pass, which the rewrite then replaced.
    Reporting only `discarded` made the run look like a 1% rejection rate and
    said nothing about how much work the gate was actually doing - which is the
    number Aman is judging when he reads the sample.

    `sent_back` is not a claim that the rewrite succeeded. The rewrite returns
    one replacement per card in the same order, but nothing enforces that, so
    there is no reliable mapping from an original to its replacement - and
    calling a card fixed on the strength of a guess would be exactly the kind
    of confident wrong number this reporting exists to stop. What is true of
    every card here is that the gate objected and it did not ship; a
    replacement the gate turned down again lands in `discarded` on its own.
    """
    cards = for_lesson(llm, topic, topic["lesson"], tier=tier)
    kept, rejected, confidence = _kept(cards, gate.review(llm, topic, cards))
    if not rejected:
        return kept, rejected, [], confidence

    try:
        fixed = rewrite(llm, topic, topic["lesson"], rejected, tier=tier)
    except LLMError:
        # A failed repair is not worse than the discard it replaces.
        return kept, rejected, [], confidence
    if not fixed:
        return kept, rejected, [], confidence

    repaired, still_bad, fixed_confidence = _kept(fixed, gate.review(llm, topic, fixed))
    # `still_bad` holds replacements the gate turned down again - different
    # cards from the originals in `rejected`, which are the wordings it caught
    # first and which are recorded rather than dropped.
    return kept + repaired, still_bad, rejected, {**confidence, **fixed_confidence}


def save(con, topic: dict, kept: list, rejected: list[tuple[object, str]], confidence: dict,
         sent_back: list[tuple[object, str]] | None = None) -> None:
    now = datetime.now(timezone.utc)
    con.execute("delete from cards where topic_slug = ? and source = 'lesson'", [topic["slug"]])
    # Three statuses: draft is what publishes, rejected is what the gate threw
    # away for good, repaired is the wording the gate caught before the rewrite
    # replaced it. Only draft reaches Supabase; the other two are the record of
    # what the gate did, which is the thing under review alongside the cards.
    #
    # A repaired row is keyed apart from the card it describes, because a
    # rewrite that fixes only the answer keeps the question and the two would
    # otherwise share an id - one overwriting the other, and taking either the
    # publishable card or the gate's objection out of the record.
    rows = (
        [(c, reason, "repaired") for c, reason in (sent_back or [])]
        + [(c, reason, "rejected") for c, reason in rejected]
        + [(c, None, "draft") for c in kept]
    )
    # kept, quality and source_refs are what /admin/cards reads: without them a
    # lesson card never reaches the review screen, which is where Aman looks.
    refs = json.dumps([{"kind": "lesson", "id": topic["slug"], "title": topic["name"]}])
    # public.cards.id is a uuid, so a readable "slug:l0" id would never publish.
    for card, reason, status in rows:
        con.execute(
            """insert or replace into cards
               (id, topic_slug, format, difficulty, prompt_md, options, answer_md, key_points,
                source_refs, quality, kept, status, source, reject_reason, created_at)
               values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'lesson', ?, ?)""",
            [
                card_id(topic["slug"], card.prompt, "repaired" if status == "repaired" else ""),
                topic["slug"], card.format, card.difficulty, card.prompt,
                json.dumps(card.options) if card.options else None, card.answer,
                json.dumps(card.key_points), refs,
                json.dumps({"gate_confidence": confidence.get(id(card), 0.5)}),
                status == "draft", status, reason, now,
            ],
        )


def run(con, only: list[str] | None = None, limit: int | None = None, redo: bool = False,
        tier: str = "smart", llm: LLM | None = None) -> tuple[int, int]:
    llm = llm or LLM(con)
    todo = topics_with_lessons(con, only, limit, redo)
    started, before = time.time(), spend_usd(con)
    # The connection's lock, not one of our own: a save here and a worker's
    # cost log are the same connection, and two locks let them interleave.
    db = lock_for(con)
    kept_total = rejected_total = sent_back_total = done = 0

    print(f"{len(todo)} topics with lessons, {WORKERS} at a time", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(one, llm, t, tier): t for t in todo}
        try:
            for future in as_completed(futures):
                topic = futures[future]
                try:
                    kept, rejected, sent_back, confidence = future.result()
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
                    save(con, topic, kept, rejected, confidence, sent_back)
                    spent = spend_usd(con) - before
                done += 1
                kept_total += len(kept)
                rejected_total += len(rejected)
                sent_back_total += len(sent_back)
                seen = kept_total + rejected_total
                # Two rates, because they answer different questions: how much
                # the gate caught, and how much it could not save.
                caught = (sent_back_total + rejected_total) / max(1, seen)
                lost = rejected_total / max(1, seen)
                print(
                    f"[{done}/{len(todo)}] {topic['slug']}  kept {len(kept)}  "
                    f"fixed {len(sent_back)}  dropped {len(rejected)}  "
                    f"(gate caught {caught:.0%}, dropped {lost:.0%} so far)  "
                    f"${spent:.3f}  {int(time.time() - started)}s",
                    flush=True,
                )
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
    return kept_total, rejected_total
