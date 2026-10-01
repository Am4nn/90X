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
from . import blind_gate, gate
from .from_lessons import rewrite
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
        """select t.slug, t.name, t.domain, l.body_md from topics t
           join lessons l on l.topic_slug = t.slug
           where exists (select 1 from cards c where c.topic_slug = t.slug and c.source = 'lesson'
                         and c.status in ('draft', 'rejected'))
           order by t.importance desc, t.slug"""
    ).fetchall()
    out = [{"slug": s, "name": n, "domain": d, "lesson": b} for s, n, d, b in rows]
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


def merge_rejects(answerability: list[tuple[object, str]],
                  guessability: list[tuple[object, str]]) -> list[tuple[object, str]]:
    """Union of the two gates' rejections.

    The answerability gate's reason wins when a card fails both, because it is
    the more fundamental ("the marked answer is wrong") than "guessable by
    elimination". The card objects are the same ones `cards_of` returned, so a
    later `apply` matches them by identity.
    """
    out = list(answerability)
    for card, reason in guessability:
        if not any(card is c for c, _ in out):
            out.append((card, reason))
    return out


def store_fix(con, topic: dict, old: Draft, card, confidence: dict) -> bool:
    """Replace a rejected card with the rewrite that passed.

    The old row stays as `repaired`, carrying what the gate objected to, so the
    review pack can still show what was caught. Its id is keyed apart from the
    replacement's, because a rewrite that changes only the format or the answer
    keeps the question and the two would otherwise collide.
    """
    now = datetime.now(timezone.utc)
    new_id = card_id(topic["slug"], card.prompt)
    if con.execute("select 1 from cards where id = ? and id <> ?", [new_id, old.id]).fetchone():
        # The rewrite repeats a question the topic already has, and its id is
        # that card's. Replacing would delete a live card to store a duplicate.
        return False
    # Re-key the old row first. A card's id comes from its question, and a
    # rewrite that changes only the format or the answer keeps the question, so
    # the replacement's id equals the original's - and `insert or replace` then
    # overwrote the repaired row, erasing the gate's objection.
    con.execute(
        "update cards set id = ?, status = 'repaired', kept = false where id = ?",
        [card_id(topic["slug"], old.prompt, "repaired"), old.id],
    )
    refs = json.dumps([{"kind": "lesson", "id": topic["slug"], "title": topic["name"]}])
    con.execute(
        """insert or replace into cards
           (id, topic_slug, format, difficulty, prompt_md, options, answer_md, key_points,
            source_refs, quality, kept, status, source, reject_reason, created_at)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, true, 'draft', 'lesson', null, ?)""",
        [
            new_id, topic["slug"], card.format, card.difficulty, card.prompt,
            json.dumps(card.options) if card.options else None, card.answer,
            json.dumps(card.key_points), refs,
            json.dumps({"gate_confidence": confidence.get(id(card), 0.5), "regated": True}),
            now,
        ],
    )
    return True


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


def run(con, only: list[str] | None = None, tier: str = "smart", llm: LLM | None = None) -> dict:
    llm = llm or LLM(con)
    todo = topics_with_cards(con, only)
    db = lock_for(con)
    started, before = time.time(), spend_usd(con, getattr(llm, "run_id", None))
    totals = {"topics": 0, "judged": 0, "recovered": 0, "newly_rejected": 0, "rejected": 0, "reformatted": 0}

    def work(topic: dict):
        with db:
            cards = cards_of(con, topic["slug"])
        if not cards:
            return topic, [], [], {}, []
        result = gate.review(llm, topic, cards, tier=tier)
        rejected = gate.judge(cards, result)
        confidence = gate.confidence_by_card(cards, result)
        # The blind gate is a second, independent check: a card whose answer is
        # forced by the choices' shape alone is guessable even when its answer is
        # correct, so the answerability gate alone would let it through. Reject
        # on either gate, so the two can never un-reject each other.
        blind = blind_gate.review(llm, cards, tier=tier)
        rejected = merge_rejects(rejected, blind_gate.judge(cards, blind))
        # A stricter gate without a repair pass is just a delete button. Most of
        # what it turns down here is a good question in the wrong format - "what
        # iteration order do HashSet, LinkedHashSet and TreeSet give?" is a fair
        # interview question and a bad flash card - so each rejection gets the
        # same one rewrite the first pass gives, with the reason attached.
        fixes: list[tuple[object, object]] = []
        if rejected:
            try:
                replacements = rewrite(llm, topic, topic["lesson"], rejected, tier="smart")
            except LLMError:
                replacements = []
            if replacements:
                passed = gate.review(llm, topic, replacements)
                still_bad = {id(c) for c, _ in gate.judge(replacements, passed)}
                blind_passed = blind_gate.review(llm, replacements, tier=tier)
                still_bad |= {id(c) for c, _ in blind_gate.judge(replacements, blind_passed)}
                confidence.update(gate.confidence_by_card(replacements, passed))
                # Positional pairing is what the rewrite prompt asks for; when
                # the counts disagree there is no honest mapping, so nothing is
                # claimed and the originals stay rejected.
                if len(replacements) == len(rejected):
                    fixes = [(old, new) for (old, _), new in zip(rejected, replacements)
                             if id(new) not in still_bad]
        return topic, cards, rejected, confidence, fixes

    print(f"{len(todo)} topics to re-judge, {WORKERS} at a time", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(work, t): t for t in todo}
        try:
            for future in as_completed(futures):
                topic = futures[future]
                try:
                    topic, cards, rejected, confidence, fixes = future.result()
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
                    fixes = [(o, c) for o, c in fixes if store_fix(con, topic, o, c, confidence)]
                    spent = spend_usd(con, getattr(llm, "run_id", None)) - before
                totals["topics"] += 1
                totals["judged"] += len(cards)
                totals["recovered"] += recovered
                totals["newly_rejected"] += newly
                totals["rejected"] += len(rejected) - len(fixes)
                totals["reformatted"] += len(fixes)
                if recovered or newly or fixes:
                    print(f"  {topic['slug']}: +{recovered} recovered, -{newly} newly rejected, "
                          f"{len(fixes)} rewritten", flush=True)
                if totals["topics"] % 25 == 0:
                    print(f"[{totals['topics']}/{len(todo)}] {totals['judged']} judged, "
                          f"+{totals['recovered']} / -{totals['newly_rejected']}  ${spent:.3f}  "
                          f"{int(time.time() - started)}s", flush=True)
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
    return totals
