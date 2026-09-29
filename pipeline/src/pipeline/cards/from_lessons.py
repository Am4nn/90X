"""The repair pass: rewrite cards the gate turned down.

The first card pass read a source section and wrote questions while holding
it, which is why drafts asked things like "In the reference solution, after
removing the run starting at x up to y-1, what invariant makes this correct?"
- unanswerable unless you can see a solution the reader never sees.

Generating from the lesson removed the leak at the root, and Feed v2 goes
further: the writer is no longer asked for a mixed `CardSet`, it is asked for
one named archetype and writes that one thing (see `write.py`). What remains
here is `rewrite`, the one-replacement-per-card repair pass the gate and the
human-review path (`fix.py`, `regate.py`) both reuse.
"""

from pydantic import BaseModel, Field, ValidationError, model_validator

from ..llm import LLMError

from .generate import Card

RULES_REMINDER = """Every card must still be answerable by a competent engineer who studied this topic anywhere, without seeing any particular text, and must be something an interviewer would plausibly ask. key_points are 2-4 short checkable points used to grade typed answers."""


class CardSet(BaseModel):
    cards: list[Card] = Field(min_length=1, max_length=12)

    @model_validator(mode="before")
    @classmethod
    def _drop_malformed(cls, data):
        """One bad card must not cost the eleven good ones beside it.

        A multiple-choice card with three options, or an answer that is not
        one of them, used to fail the whole set and lose the topic. It is
        dropped instead; if too few survive, the set still fails."""
        if isinstance(data, dict) and isinstance(data.get("cards"), list):
            good = []
            for item in data["cards"]:
                try:
                    good.append(Card.model_validate(item))
                except ValidationError:
                    continue
            return {**data, "cards": good}
        return data


REWRITE_SYSTEM = f"""You are fixing interview-prep cards that failed review. For each one you are given the card and the reason it was rejected.

Common reasons and what to do:
- "needs_context": it refers to something the reader cannot see - a solution, a snippet, an example, a bare variable. Rewrite it to carry its own setup, or to ask the same idea in a way that stands alone.
- "wrong_format": usually a typed card whose honest answer is a list to enumerate. Turn it into multiple choice, or narrow the question until one to three sentences answers it.
- "ambiguous": say exactly what is being asked, or narrow it until one answer is clearly right.
- "refers to unseen material": the prompt names the lesson, the passage or the text. Ask about the subject instead.

Keep the idea the card was testing. Return one replacement per card given, in the same order. If a card cannot be saved without changing what it tests, return it rewritten as best you can rather than dropping it.

{RULES_REMINDER}"""


def rewrite(llm, topic: dict, lesson_md: str, rejected: list[tuple[object, str]], tier: str = "smart") -> list[Card]:
    """One repair pass over the cards the gate turned down.

    At 6% rejection this is worth roughly 160 cards across a full run, and the
    gate already says exactly what is wrong with each one, which is usually
    enough to fix the wording without touching the idea being tested.
    """
    if not rejected:
        return []
    listing = "\n\n".join(
        f"[{i}] rejected because: {reason}\n"
        f"format: {card.format}\n"
        f"question: {card.prompt}\n"
        f"answer: {card.answer}"
        + (f"\noptions: {card.options}" if card.options else "")
        for i, (card, reason) in enumerate(rejected)
    )
    user = (
        f"Topic: {topic['name']} ({topic['domain']})\n\n"
        f"Cards to fix:\n{listing}\n\n"
        f"Lesson they came from:\n{lesson_md}"
    )
    return llm.complete_json(REWRITE_SYSTEM, user, CardSet, tier=tier, purpose="cards-rewrite").cards
