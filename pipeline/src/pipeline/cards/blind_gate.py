"""The blind gate: could a reader guess the answer without the lesson?

A card is guessable when its answer is visible from the choices alone. The
pipeline shows a model only what a reader without the lesson sees — the options
for a pick-one card, the items for an ordering or mapping, the question for a
numeric card — and asks it to answer. If the model gets it right, a reader can
too, and the card is rewritten.

Three samples per card, rejected at two or more correct. One sample would
reject a quarter of good cards by luck alone; three brings a false reject to
~16%, and a false reject only costs a rewrite (DECISIONS round 4). The
rejection reason is "guessable", which the repair pass turns into a rewrite
with the options made genuinely competitive.

The gate shows the choices and nothing else. The lesson, the topic and the area
never reach the model: fold the source text in and the gate is defeated.
"""

from pydantic import BaseModel, Field

from ..llm import LLMError
from .archetypes import shape_of

SAMPLES = 3
REJECT_AT = 2


class Guess(BaseModel):
    """The model's answer to one sample, in the shape's native form."""

    picked: list[int] | None = Field(default=None, description="chosen: the 0-based indices picked")
    order: list[int] | None = Field(default=None, description="ordered: the full ordering as 0-based indices")
    pairs: list[list[int]] | None = Field(default=None, description="mapping: [left, right] 0-based index pairs")
    value: float | None = Field(default=None, description="number: the value")


class BlindVerdict(BaseModel):
    index: int
    correct: int


SYSTEM = """You are testing whether an interview-prep card is guessable from its answer choices alone. You see only the choices a reader sees — never the lesson, the topic, or the source material. Answer honestly; being wrong costs nothing.

Return exactly one field, matching what you were asked:
- `picked`: a list of 0-based indices (pick one, grid cells, tap a line).
- `order`: the full ordering as a list of 0-based indices.
- `pairs`: a list of [left, right] 0-based index pairs.
- `value`: a number.

Do not explain. A correct answer here means the card's answer is given away by its choices."""

_INSTRUCTIONS = {
    "chosen": "Which would you pick as the answer? Return `picked` as a list of 0-based indices.",
    "ordered": "Put the items in the correct order. Return `order` as a list of 0-based indices.",
    "mapping": "Pair the items correctly. Return `pairs` as a list of [left, right] 0-based index pairs.",
    "number": "What is the number? Return `value`.",
}


def shape(card) -> str | None:
    """The card's answer shape, or None when it has no guessable answer.

    A self-rate card stores no answer and a legacy typed/flash card has no
    options to pick from; neither can be guessed blind. A legacy mcq still
    answers by picking an option, so it counts as chosen.
    """
    s = shape_of(getattr(card, "format", None))
    if s is None and getattr(card, "options", None):
        return "chosen"
    return s


def view(card) -> str:
    """The answer choices and nothing else — never the question, lesson, topic
    or area.

    A pick-one card stores its options separately, so the model sees exactly
    those, numbered. Every other primitive keeps its items inside the prompt,
    so the reader's view is the prompt; the source text still never reaches
    the model either way.
    """
    options = getattr(card, "options", None) or []
    if options:
        return "Options:\n" + "\n".join(f"{i}. {o}" for i, o in enumerate(options))
    return card.prompt


def _satisfies(order: list[int] | None, constraints: list[list[int]] | None) -> bool:
    if order is None or not constraints:
        return False
    # The item count comes from the constraints (the highest index they name),
    # not from the guess, so a short guess cannot satisfy a longer card.
    n = max(max(a, b) for a, b in constraints) + 1
    if sorted(order) != list(range(n)):
        return False  # must be a permutation of the item indices
    pos = {item: i for i, item in enumerate(order)}
    return all(pos[a] < pos[b] for a, b in constraints)


def _pairs_match(guess: list[list[int]] | None, expected: list[list[int]] | None) -> bool:
    if guess is None or expected is None:
        return False
    return sorted(map(tuple, guess)) == sorted(map(tuple, expected))


def correct(card, guess: Guess) -> bool:
    """Whether one sample's guess matches the card's stored answer."""
    s = shape(card)
    if s == "chosen":
        if getattr(card, "picked", None):
            return guess.picked is not None and sorted(guess.picked) == sorted(card.picked)
        # A legacy mcq stores its answer as one of the options, not as indices.
        options = getattr(card, "options", None) or []
        answer = getattr(card, "answer", "")
        if options and answer:
            try:
                return guess.picked == [[o.strip() for o in options].index(answer.strip())]
            except ValueError:
                return False
        return False
    if s == "ordered":
        return _satisfies(guess.order, getattr(card, "constraints", None))
    if s == "mapping":
        return _pairs_match(guess.pairs, getattr(card, "pairs", None))
    if s == "number":
        value = getattr(card, "value", None)
        tolerance = getattr(card, "tolerance", None) or 0
        return guess.value is not None and value is not None and abs(guess.value - value) <= tolerance
    return False


def judge_card(llm, card, tier: str = "smart") -> int:
    """How many of SAMPLES samples answered correctly (0..SAMPLES).

    A sample the model fails to answer (bad JSON, provider error) is not
    evidence of guessability, so it is skipped rather than counted correct or
    wrong.
    """
    if shape(card) is None:
        return 0
    correct_count = 0
    for _ in range(SAMPLES):
        try:
            guess = llm.complete_json(SYSTEM, _user(card), Guess, tier=tier, purpose="blind-gate")
        except LLMError:
            continue
        if correct(card, guess):
            correct_count += 1
    return correct_count


def _user(card) -> str:
    return f"{view(card)}\n\n{_INSTRUCTIONS[shape(card)]}"


def review(llm, cards: list, tier: str = "smart") -> list[BlindVerdict]:
    """One blind verdict per card, three samples each."""
    return [BlindVerdict(index=i, correct=judge_card(llm, card, tier)) for i, card in enumerate(cards)]


def judge(cards: list, verdicts: list[BlindVerdict]) -> list[tuple[object, str]]:
    """Returns (card, reason) for every card a reader could guess blind.

    Rejection is at REJECT_AT correct samples out of SAMPLES, so a single lucky
    sample does not cost a good card a rewrite.
    """
    by_index = {v.index: v for v in verdicts}
    rejected = []
    for i, card in enumerate(cards):
        v = by_index.get(i)
        if v and v.correct >= REJECT_AT:
            rejected.append((card, f"guessable: answered correctly {v.correct}/{SAMPLES} times from the choices alone"))
    return rejected


def repair(llm, topic: dict, lesson_md: str, rejected: list[tuple[object, str]], tier: str = "smart"):
    """Blind-gate rejections reuse the same rewrite path as every other gate
    rejection: one replacement per card, in order, via from_lessons.rewrite."""
    from .from_lessons import rewrite

    return rewrite(llm, topic, lesson_md, rejected, tier=tier)
