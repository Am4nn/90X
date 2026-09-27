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

from pydantic import BaseModel, Field

from .generate import Card

# Roughly one card per key idea; the important topics earn a few more.
def card_budget(importance: float) -> int:
    return 8 if importance < 0.7 else (10 if importance < 0.9 else 12)


SYSTEM = """You write interview-prep cards from a lesson the reader has already studied.

THE READER CANNOT SEE THE LESSON when answering. The card tests whether they learned the topic, not whether they can find a sentence. Never write "the lesson", "the passage", "the text", "the above", "as described", "the reference solution", or anything else that points at material in front of them. If a question only makes sense with the lesson open, it is a broken card.

Every card must be answerable by a competent engineer who studied this topic anywhere, and must be something an interviewer would plausibly ask.

Choose the format from the shape of the answer, not by quota:
- typed: the answer is an explanation, a reason, or a trade-off, given in 1-3 sentences. Use this for "why" and "when would you" questions.
- flash: the answer is one crisp fact, a definition, or a complexity. One sentence.
- mcq: the answer is one of several enumerable alternatives, or free typing would be unfair because the expected answer is a specific list or term. Exactly 4 options, plausible distractors, and `answer` must equal one option exactly.
- output: the prompt contains a short fenced code snippet and the answer is its exact output. Only when the lesson genuinely supports it.

Never write a typed card whose honest answer is a list of items to enumerate. That is an mcq.

Rules:
- Everything in the answer must follow from the lesson. Do not add facts it does not support.
- key_points: 2-4 short, independently checkable points a good answer contains. These grade typed answers, so they must be things a grader can actually look for.
- Spread the cards across the lesson: the core idea, the key points, the trade-offs, the traps, and the follow-up ladder. Do not write four cards on the same sentence.
- difficulty: Easy, Medium or Hard for an interview candidate.
Write in plain, direct English."""


class CardSet(BaseModel):
    cards: list[Card] = Field(min_length=3, max_length=12)


def for_lesson(llm, topic: dict, lesson_md: str, tier: str = "smart") -> list[Card]:
    n = card_budget(topic.get("importance") or 0.5)
    user = (
        f"Topic: {topic['name']} ({topic['domain']})\n"
        f"Write {n} cards.\n\n"
        f"Lesson:\n{lesson_md}"
    )
    return llm.complete_json(SYSTEM, user, CardSet, tier=tier, purpose="cards-from-lesson").cards
