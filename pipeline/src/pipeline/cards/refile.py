"""Re-file a card the gate rejected for sitting under the wrong archetype.

The conformance gate rejects a card whose question does not do what its archetype
says. For most of them the question is fine and only the label is wrong - a card
asking which design principle a snippet breaks is a good card, just not an
`output-prediction` card. The repair pass cannot help: it rewrites a question to
fit its archetype, where the honest fix is to move the question to the archetype it
already matches.

So this asks, per card, which archetype the question actually belongs to, and
moves it there. The move is tightly bounded:

* the candidate must be eligible for the topic's area, or the corpus would carry a
  card its area never asks for;
* the candidate must list the card's **current primitive**, because the answer
  columns are shaped for it - `picked` for chosen, `pairs` for mapping. Moving a
  mapping card under a pick-one archetype would leave an answer nothing can grade;
* the candidate must allow the card's difficulty;
* and the model's answer is checked against that candidate list rather than
  trusted, so an invented id is a refusal rather than a corrupt row.

A moved card returns to `draft` and is re-gated afterwards, which is what proves
the new label actually fits. A card with no candidate stays rejected.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from . import archetypes

SYSTEM = """You file interview-prep cards under the archetype that matches the question they ask.

You are given one question and a numbered list of candidate archetypes, each with a line saying what a question of that archetype must do. Choose the candidate whose line the question already satisfies.

Choose by what the question actually asks, not by what it is about: a question asking which design principle a snippet breaks belongs to the archetype about naming a violated principle, whatever the snippet's subject matter.

Return the id of exactly one candidate, or null when no candidate's line fits the question. Null is the right answer whenever you would have to stretch a line to make it fit - a card filed nowhere is better than a card filed wrongly, because the gate will reject it again and the reader never sees it."""


class Choice(BaseModel):
    archetype: str | None = Field(default=None, description="the chosen candidate id, or null when none fits")
    reason: str = Field(default="", description="one short clause saying why")


def candidates(card, area: str) -> list[archetypes.Archetype]:
    """The archetypes this card could move to without breaking anything.

    Eligibility by area, the card's own primitive, and its difficulty. The card's
    present archetype is excluded: it is the one already judged not to fit.
    """
    difficulty = getattr(card, "difficulty", "") or ""
    primitive = getattr(card, "format", "")
    current = getattr(card, "archetype", None)
    out = []
    for a in archetypes.registry().archetypes:
        if a.id == current or area not in a.areas:
            continue
        if primitive not in a.primitives:
            continue
        if difficulty and difficulty not in a.difficulties:
            continue
        out.append(a)
    return out


def _user(card, options: list[archetypes.Archetype]) -> str:
    lines = [f"Question:\n{card.prompt}", "", "Candidates:"]
    for a in options:
        lines.append(f"- {a.id}: {a.intent}")
    return "\n".join(lines)


def choose(llm, card, options: list[archetypes.Archetype], tier: str = "fast") -> archetypes.Archetype | None:
    """The archetype this question belongs to, or None.

    `fast` by default: picking from a short list against one-line definitions is a
    classification, not a judgement, and the answer is validated against the list
    either way.
    """
    if not options:
        return None
    result = llm.complete_json(SYSTEM, _user(card, options), Choice, tier=tier, purpose="card-refile")
    if not result.archetype:
        return None
    # Checked, not trusted: an id outside the candidate list is a refusal.
    return next((a for a in options if a.id == result.archetype), None)


def pending(con) -> list[dict]:
    """Cards rejected for the wrong archetype, with their topic's area."""
    rows = con.execute(
        """select c.id, c.topic_slug, t.domain, c.archetype, c.format, c.difficulty, c.prompt_md
           from cards c join topics t on t.slug = c.topic_slug
           where c.archetype is not null and c.status = 'rejected'
             and c.reject_reason like 'wrong archetype%'
           order by c.topic_slug, c.id"""
    ).fetchall()
    keys = ["id", "topic_slug", "area", "archetype", "format", "difficulty", "prompt"]
    return [dict(zip(keys, r)) for r in rows]


def verify(con, llm, card_ids: list[str], tier: str = "smart") -> dict:
    """Ask the gate whether each moved card asks what its new archetype says.

    A move is a claim, and the four bounds in `candidates` - area, primitive,
    difficulty, the model answer validating against the list - are necessary but not
    sufficient. Measured on the first real pass: 489 of 523 moves fit, 34 did not,
    and all 34 had already gone live, because this check lived in a separate script
    nobody was obliged to run.

    Only the moved cards are judged. `card-regate` works per topic, and the moved
    cards are spread thin - 523 of them over 159 topics - so re-gating by topic means
    judging some 4,000 cards to check 523 and re-rolling verdicts already paid for.

    The answerability gate only: no blind gate, no rewrite pass. The question is
    narrow, and a card that fails goes back to rejected naming the archetype it
    failed in, so the move is undone in effect and visible in the record.
    """
    from collections import defaultdict

    from ..llm import BudgetExceeded, LLMError
    from . import gate, regate

    wanted: dict[str, set[str]] = defaultdict(set)
    rows = con.execute(
        f"""select topic_slug, id from cards
            where id in ({",".join("?" * len(card_ids))})""",
        card_ids,
    ).fetchall() if card_ids else []
    for slug, card_id in rows:
        wanted[slug].add(card_id)

    topics = {t["slug"]: t for t in regate.topics_with_cards(con, list(wanted))}
    checked = unfit = 0
    reasons: list[tuple[str, str]] = []

    for slug, ids in wanted.items():
        topic = topics.get(slug)
        if not topic:
            continue
        cards = [c for c in regate.cards_of(con, slug) if c.id in ids]
        if not cards:
            continue
        try:
            result = gate.review(llm, topic, cards, tier=tier)
        except BudgetExceeded as e:
            print(f"  stopping: {e}", flush=True)
            break
        except (LLMError, Exception) as e:  # noqa: BLE001 - one topic's failure
            print(f"  {slug}: FAILED {type(e).__name__}: {e}", flush=True)
            continue
        rejected = gate.judge(cards, result)
        checked += len(cards)
        unfit += len(rejected)
        for card, why in rejected:
            reasons.append((card.id, why))
        if rejected:
            regate.apply(con, cards, rejected, gate.confidence_by_card(cards, result))
            print(f"  {slug}: {len(rejected)} of {len(cards)} did not fit", flush=True)

    return {"checked": checked, "fit": checked - unfit, "unfit": unfit, "reasons": reasons}


def run(con, llm=None, tier: str = "fast", dry_run: bool = True,
        check: bool = True, check_tier: str = "smart") -> dict:
    """Move what can be moved, then confirm each move with the gate.

    The check used to be the caller's job - the step printed "run card-regate to
    confirm they fit now" and left it there, which is how 34 cards reached readers
    under an archetype that did not fit. A step that cannot verify its own output
    should not be writing it.
    """
    from types import SimpleNamespace

    from ..llm import LLM, BudgetExceeded

    llm = llm or LLM(con)
    todo = pending(con)
    # card id -> (archetype it was filed under, archetype it is moving to)
    moved: dict[str, tuple[str, str]] = {}
    no_candidates = unchanged = failed = 0
    considered = 0
    stopped = False

    for row in todo:
        card = SimpleNamespace(**row)
        options = candidates(card, row["area"])
        considered += 1
        if not options:
            no_candidates += 1
            continue
        try:
            chosen = choose(llm, card, options, tier=tier)
        except BudgetExceeded as e:
            # Count only what was actually looked at, and say the run is short.
            # Reporting the full pending count as `considered` made an early stop
            # read as a complete run, which is the one thing a caller deciding
            # whether to re-run needs to know.
            considered -= 1
            stopped = True
            print(f"  stopping: {e}", flush=True)
            break
        except Exception as e:  # noqa: BLE001 - any provider failure is this card's
            # Broad on purpose. An exception from the model client that is not an
            # LLMError used to escape the loop entirely, so every move already
            # chosen was discarded before the write below and no later card was
            # tried. One card's failure should cost that card, not the pass.
            failed += 1
            print(f"  {row['id'][:8]}: FAILED {type(e).__name__}: {e}", flush=True)
            continue
        if chosen is None:
            unchanged += 1
            continue
        moved[row["id"]] = (row["archetype"], chosen.id)

    if not dry_run and moved:
        # Back to draft so the next gate pass judges it under its new label. That
        # pass, not this one, is what proves the move was right.
        #
        # The move is recorded in `quality` rather than thrown away. Setting
        # reject_reason to null erased the only trace that a card had been moved,
        # so a follow-up gate could not be aimed at the cards that needed it and
        # the whole corpus had to be re-judged instead - $6 rather than under $1,
        # every time the step runs. `refiled_from` is also the honest record of
        # why a card carries the archetype it does.
        con.executemany(
            """update cards set archetype = ?, status = 'draft', kept = true,
                      reject_reason = null,
                      quality = json_merge_patch(coalesce(quality, '{}'),
                                                json_object('refiled_from', ?))
               where id = ?""",
            [[new, old, card_id] for card_id, (old, new) in moved.items()],
        )

    checked = {"checked": 0, "fit": 0, "unfit": 0, "reasons": []}
    if not dry_run and moved and check:
        checked = verify(con, llm, list(moved), tier=check_tier)

    return {
        "considered": considered,
        "pending": len(todo),
        "moved": len(moved),
        "verified_fit": checked["fit"],
        "verified_unfit": checked["unfit"],
        "no_candidate_archetype": no_candidates,
        "nothing_fitted": unchanged,
        "failed": failed,
        "stopped_early": stopped,
        "dry_run": dry_run,
    }


def refiled(con) -> list[str]:
    """Topic slugs holding a card this step moved.

    The point of recording the move: a gate pass can be aimed at these topics
    rather than at all 274, which is the difference between $6 and under $1.
    """
    rows = con.execute(
        """select distinct topic_slug from cards
           where archetype is not null
             and json_extract_string(quality, '$.refiled_from') is not null"""
    ).fetchall()
    return [r[0] for r in rows]
