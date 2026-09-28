"""Cards written from a lesson, not from a chunk of scraped text.

The first card pass read a source section and wrote questions while holding
it, which is why drafts asked things like "In the reference solution, after
removing the run starting at x up to y-1, what invariant makes this correct?"
- unanswerable unless you can see a solution the reader never sees.

Generating from the lesson removes the leak at the root: the lesson is
self-contained and the reader has actually read it. Format is chosen by the
shape of the answer rather than assigned up front, because a question whose
answer is an enumerable list ("along which dimensions can content negotiation
vary?") is unfair to type and belongs in multiple choice.
"""

from pydantic import BaseModel, Field, ValidationError, model_validator

from ..llm import LLMError

from .generate import Card

# Roughly one card per key idea; the important topics earn a few more.
def card_budget(importance: float) -> int:
    return 8 if importance < 0.7 else (10 if importance < 0.9 else 12)


RULES_REMINDER = """Every card must still be answerable by a competent engineer who studied this topic anywhere, without seeing any particular text, and must be something an interviewer would plausibly ask. key_points are 2-4 short checkable points used to grade typed answers."""

SYSTEM = """You write interview-prep cards from a lesson the reader has already studied.

THE READER CANNOT SEE THE LESSON when answering. The card tests whether they learned the topic, not whether they can find a sentence. Never write "the lesson", "the passage", "the text", "the above", "as described", "the reference solution", or anything else that points at material in front of them. If a question only makes sense with the lesson open, it is a broken card.

Every card must be answerable by a competent engineer who studied this topic anywhere, and must be something an interviewer would plausibly ask.

Choose the format from the shape of the answer, not by quota:
- typed: the answer is an explanation, a reason, or a trade-off, given in 1-3 sentences. Use this for "why" and "when would you" questions.
- flash: the answer is one crisp fact, a definition, or a complexity. One sentence.
- mcq: the answer is one of several enumerable alternatives, or free typing would be unfair because the expected answer is a specific list or term. Exactly 4 options, and `answer` must equal one option exactly.
  Every wrong option must be a mistake a candidate actually makes: the off-by-one threshold, the confused pair, the answer that is true of the neighbouring concept. An option nobody would pick is padding, and it turns the card into a reading exercise.
- output: the prompt contains a short fenced code snippet and the answer is its exact output. Only when the lesson genuinely supports it.

Never write a typed card whose honest answer is a list of items to enumerate. That is an mcq.

Rules:
- Everything in the answer must follow from the lesson. Do not add facts it does not support.
- key_points: 2-4 short, independently checkable points a good answer contains. These grade typed answers, so they must be things a grader can actually look for.
- Spread the cards across the lesson: the core idea, the key points, the trade-offs, the traps, and the follow-up ladder. Do not write four cards on the same sentence.
- Spread the difficulty too. A topic wants a few Easy cards that check the reader remembers the mechanism, more Medium ones that ask them to explain or compare, and at least one Hard card that makes them apply it to a situation the lesson did not spell out.
- difficulty: Easy, Medium or Hard for an interview candidate.
Write in plain, direct English."""


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


MIN_CARDS = 3


def for_lesson(llm, topic: dict, lesson_md: str, tier: str = "smart") -> list[Card]:
    """A topic's worth of cards. The set model allows one card because the
    repair pass reuses it and usually has one or two to fix; a generation that
    comes back with fewer than MIN_CARDS is the thing worth rejecting."""
    n = card_budget(topic.get("importance") or 0.5)
    user = (
        f"Topic: {topic['name']} ({topic['domain']})\n"
        f"Write {n} cards.\n\n"
        f"Lesson:\n{lesson_md}"
    )
    cards = llm.complete_json(SYSTEM, user, CardSet, tier=tier, purpose="cards-from-lesson").cards
    if len(cards) < MIN_CARDS:
        raise LLMError(f"only {len(cards)} cards for {topic['slug']}, wanted at least {MIN_CARDS}")
    return cards


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


