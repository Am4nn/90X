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


def run(con, llm=None, tier: str = "fast", dry_run: bool = True) -> dict:
    """Move what can be moved. Returns counts; the caller re-gates afterwards."""
    from types import SimpleNamespace

    from ..llm import LLM, BudgetExceeded

    llm = llm or LLM(con)
    todo = pending(con)
    moved: dict[str, str] = {}
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
        moved[row["id"]] = chosen.id

    if not dry_run and moved:
        # Back to draft so the next gate pass judges it under its new label. That
        # pass, not this one, is what proves the move was right.
        con.executemany(
            """update cards set archetype = ?, status = 'draft', kept = true,
                      reject_reason = null where id = ?""",
            [[new, card_id] for card_id, new in moved.items()],
        )

    return {
        "considered": considered,
        "pending": len(todo),
        "moved": len(moved),
        "no_candidate_archetype": no_candidates,
        "nothing_fitted": unchanged,
        "failed": failed,
        "stopped_early": stopped,
        "dry_run": dry_run,
    }
