"""Can this card actually be answered?

The gate reads the question and nothing else - no lesson, no source. That is
the whole idea. A card that needs the source text in front of you looks
perfectly fine next to the source, which is exactly how 8,556 drafts came to
include "In the reference solution, after removing the run starting at x up
to y-1, what invariant makes this correct?" Judged alone, that question has
no answer, and the gate sees what a reader would see.

Multiple choice gets a second, free signal: the reviewer picks an option
blind. If a competent engineer picks a different option than our reference
answer, either the question is ambiguous or our answer is wrong. Either way
the card is not ready.
"""

from typing import Literal

from pydantic import BaseModel, Field

from ..lessons.check import REFERS_TO_SOURCE

SYSTEM = """You are checking interview-prep flashcards. You see only the questions, exactly as a candidate sees them. You do NOT see the material they were written from, and that is deliberate.

For each card, rule on whether a competent engineer who has studied this topic could answer it:

- "answerable": a fair question with a knowable answer. The candidate may need to know the topic well, but nothing is missing.
- "needs_context": it refers to something not present - a specific solution, passage, diagram, snippet, variable or example the candidate cannot see. Phrases like "the reference solution", "the given code", "in the example above", or a bare variable name such as d[x] with no setup are the signature.
- "wrong_format": the question is fine but the format is not.

How the formats actually work here, because this decides most of your verdicts:
- "typed" is free prose of one to three sentences, graded by a model against key points. It is NOT an exact-match answer box. An open-ended conceptual question - "why does this work", "what is the trade-off", "when would you not use it" - is the BEST kind of typed card, not a wrong one. Do not flag a typed card for being conceptual, open-ended, or requiring explanation. That is the format working as intended.
- A typed card is only "wrong_format" when its honest answer is a list of items to enumerate ("name the four isolation levels"), where the candidate cannot know how many you want, or when it genuinely needs several paragraphs to answer at all.
- "flash" is one crisp sentence. Flag it if the honest answer needs a paragraph.
- "mcq" needs four options with one unambiguously correct.
- "ambiguous": you cannot tell what is being asked, or several different answers would all be correct.

Give `confidence` from 0 to 1 on every card: how sure you are it is fair and well formed. A card you would happily put in front of a candidate is near 1. A card you are letting through with reservations is near 0.5. The review screen shows the least confident cards first, so this decides what a human looks at.

For multiple-choice cards, also give the option you would pick, copied exactly.

Judge only answerability and format. Do not comment on style, difficulty, or what you would have asked instead. Marking a good card as bad costs us a real question, so when a card is fair, say so."""


class Verdict(BaseModel):
    index: int = Field(description="the card's position in the list, starting at 0")
    verdict: Literal["answerable", "needs_context", "wrong_format", "ambiguous"]
    reason: str = Field(default="", description="one short sentence; empty when answerable")
    picked: str = Field(default="", description="multiple choice only: the option you would pick")
    confidence: float = Field(default=0.5, ge=0, le=1,
                              description="how sure you are this card is fair and well formed")


class GateResult(BaseModel):
    verdicts: list[Verdict]


def prompt_only(card) -> str:
    """What the gate is allowed to see."""
    lines = [f"format: {card.format}", f"question: {card.prompt}"]
    if card.format == "mcq" and card.options:
        lines += [f"  option: {o}" for o in card.options]
    return "\n".join(lines)


def review(llm, topic: dict, cards: list, tier: str = "review") -> GateResult:
    if tier not in llm.models:
        tier = "smart"
    body = "\n\n".join(f"[{i}]\n{prompt_only(c)}" for i, c in enumerate(cards))
    user = f"Topic: {topic['name']} ({topic['domain']})\n\n{body}"
    return llm.complete_json(SYSTEM, user, GateResult, tier=tier, purpose="card-gate")


def confidence_of(result: GateResult) -> dict[int, float]:
    """How sure the gate was, per card index. Missing means it never ruled."""
    return {v.index: v.confidence for v in result.verdicts}


def judge(cards: list, result: GateResult) -> list[tuple[object, str]]:
    """Returns (card, reason) for every card that must not ship.

    A card the reviewer never ruled on is kept: a missing verdict is the
    reviewer's omission, not evidence against the card, and dropping silently
    on a short reply would quietly shrink every batch.
    """
    verdicts = {v.index: v for v in result.verdicts}
    rejected = []
    for i, card in enumerate(cards):
        if m := REFERS_TO_SOURCE.search(card.prompt):
            rejected.append((card, f"refers to unseen material: {m.group(0)!r}"))
            continue
        v = verdicts.get(i)
        if v is None:
            continue
        if v.verdict != "answerable":
            rejected.append((card, f"{v.verdict}: {v.reason}"))
        elif card.format == "mcq" and v.picked and v.picked.strip() != card.answer.strip():
            rejected.append((card, "a competent answer disagrees with the marked option"))
    return rejected
