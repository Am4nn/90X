"""The blind gate: could a reader guess the answer from the choices' shape alone?

A card is guessable when its answer is forced by the choices' structure rather
than by knowing the topic: one option far longer than the rest, the only number
among prose, an "all of the above", an ordering already in the correct order, a
matching card already paired left-to-right. The pipeline shows a model only what
a reader without the lesson sees — the options for a pick-one card, the items
for an ordering or mapping, the question for a numeric card — and asks it to
judge whether the answer is forced by shape alone.

The gate deliberately does NOT reject a card just because a knowledgeable model
knows the answer. "An index speeds up lookups", "a B-tree is O(log n)", "a hash
map gives O(1) lookup" are famous facts a model trivially knows, but a learner —
the actual Feed reader — does not yet. Rejecting those shredded the corpus:
every one went through a repair pass that had nothing to fix, then was dropped.
So the gate rules on *elimination by structure*, not on *knowing the topic*.

Three samples per card, rejected at two or more flags. One sample would reject
a quarter of good cards by luck alone; three brings a false reject to ~16%, and
a false reject only costs a rewrite (DECISIONS round 4). The rejection reason is
"guessable", which the repair pass turns into a rewrite with the options made
genuinely competitive.

The gate shows the choices and nothing else. The lesson, the topic and the area
never reach the model: fold the source text in and the gate is defeated.
"""

from pydantic import BaseModel, Field

from ..llm import LLMError
from .archetypes import options_shape_of, shape_of

SAMPLES = 3
REJECT_AT = 2


class Judgement(BaseModel):
    """One sample's verdict: is the answer forced by the choices' shape alone?

    `guessable` is true only when a reader with no knowledge of the topic could
    still determine the answer by eliminating options — structure, length, type,
    or an obvious give-away — rather than by knowing the subject.
    """

    guessable: bool = Field(
        description=(
            "true when a reader with no knowledge of the topic could still get the answer "
            "right by eliminating options (structure, length, type, or an obvious give-away), "
            "rather than by knowing the subject"
        )
    )
    reason: str = Field(default="", description="when guessable, the tell in a few words; otherwise empty")


class BlindVerdict(BaseModel):
    index: int
    flags: int


SYSTEM = """You are testing whether an interview-prep card's answer is given away by its answer choices alone. You see only what a reader sees — the choices, never the lesson, the topic, or the source material.

You are NOT answering the question. You are judging: could a reader with NO knowledge of this topic still get the answer right by eliminating options — from the choices' structure, length, type, or an obvious give-away?

A card is guessable by elimination only when the choices themselves force the answer without any knowledge of the subject:
- one choice is far longer or shorter than the rest,
- one choice is the only one of its kind (the only number, the only code, the only one in a different format),
- "all of the above" / "none of the above",
- an odd-one-out a reader would pick or eliminate on sight,
- an ordering whose items are already in the correct order, or sorted alphabetically or by length,
- a matching card whose left and right columns are already paired by position,
- any other mechanical tell that lets a reader eliminate to the answer without knowing the subject.

The answer requiring ACTUAL knowledge is NOT guessable — even when the fact is famous or obvious to an expert. "The primary purpose of an index is to speed up lookups", "a B-tree is O(log n)", "a hash map gives O(1) lookup" are all things a learner does not know yet. If the choices are structurally balanced (similar length, same type, all plausible) and telling the right one from the wrong ones needs the topic, the card is fine. "Obvious if you know the topic" is exactly what the card is testing, and it is not a structural tell. Do not reject it.

Return exactly one object with `guessable` and `reason`."""

_INSTRUCTIONS = {
    "chosen": "Judge the choices: is the correct one forced by their structure, length, type, or an obvious give-away, with no knowledge of the topic?",
    "ordered": "Judge the items in the order they are shown: is the correct order forced by the shown order, the alphabet, or length, with no knowledge of the topic?",
    "mapping": "Judge the two columns: is the correct pairing forced by position or by wording, with no knowledge of the topic?",
    "number": "Judge the question: could a reader with no knowledge of the topic produce this number from common knowledge or trivial arithmetic alone?",
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


def _numbered(items) -> str:
    return "\n".join(f"{i}. {o}" for i, o in enumerate(items or []))


def view(card) -> str:
    """The answer choices and nothing else — never the question, lesson, topic
    or area.

    The choices are the `options` in their canonical per-shape encoding: a flat
    list for pick_one/order/tap_in_place/claim_grid (and legacy mcq), an object
    for match/bucket/assemble/grid. A numeric card stores no choices, so its
    question is the reader's view; the source text still never reaches the model
    either way.
    """
    options = getattr(card, "options", None)
    if isinstance(options, list) and options:
        return "Options:\n" + _numbered(options)
    if isinstance(options, dict):
        shape = options_shape_of(getattr(card, "format", None))
        if shape == "match":
            return "Left:\n" + _numbered(options.get("left")) + "\nRight:\n" + _numbered(options.get("right"))
        if shape == "bucket":
            return "Items:\n" + _numbered(options.get("items")) + "\nBuckets:\n" + _numbered(options.get("columns"))
        if shape == "assemble":
            tokens = options.get("tokens") or []
            fixed = options.get("fixed")
            out = ["Tokens:", _numbered(tokens)]
            # Pre-filled slots are part of what a reader sees: an assemble card
            # whose fixed slots already reveal the answer must not pass the gate.
            if isinstance(fixed, list):
                pre = [f"slot {i} -> token {f}" for i, f in enumerate(fixed)
                       if isinstance(f, int) and 0 <= f < len(tokens)]
                if pre:
                    out.append("Pre-filled: " + ", ".join(pre))
            return "\n".join(out)
        if shape == "grid":
            return "Rows:\n" + _numbered(options.get("rows")) + "\nColumns:\n" + _numbered(options.get("columns"))
    return card.prompt


def judge_card(llm, card, tier: str = "fast") -> int:
    """How many of SAMPLES samples judged the card guessable by elimination (0..SAMPLES).

    A sample the model fails to return (bad JSON, provider error) is not
    evidence either way, so it is skipped rather than counted as a flag.
    """
    if shape(card) is None:
        return 0
    flags = 0
    for _ in range(SAMPLES):
        try:
            # Thinking is OFF here for correctness, not cost: a model reasoning
            # for thousands of tokens invents tells a reader skimming four
            # options on a phone would never notice. With thinking on it becomes
            # a false-positive machine, and every false rejection costs a smart
            # repair pass. Do not "fix" this into a stronger judge.
            verdict = llm.complete_json(SYSTEM, _user(card), Judgement, tier=tier, purpose="blind-gate", thinking=False)
        except LLMError:
            continue
        if verdict.guessable:
            flags += 1
    return flags


def _user(card) -> str:
    return f"{view(card)}\n\n{_INSTRUCTIONS[shape(card)]}"


def review(llm, cards: list, tier: str = "fast") -> list[BlindVerdict]:
    """One blind verdict per card, three samples each."""
    return [BlindVerdict(index=i, flags=judge_card(llm, card, tier)) for i, card in enumerate(cards)]


def judge(cards: list, verdicts: list[BlindVerdict]) -> list[tuple[object, str]]:
    """Returns (card, reason) for every card a reader could guess by elimination.

    Rejection is at REJECT_AT flagged samples out of SAMPLES, so a single lucky
    flag does not cost a good card a rewrite.
    """
    by_index = {v.index: v for v in verdicts}
    rejected = []
    for i, card in enumerate(cards):
        v = by_index.get(i)
        if v and v.flags >= REJECT_AT:
            rejected.append((card, f"guessable by elimination: {v.flags}/{SAMPLES} samples flagged it"))
    return rejected


def repair(llm, topic: dict, lesson_md: str, rejected: list[tuple[object, str]], tier: str = "smart"):
    """Blind-gate rejections reuse the same rewrite path as every other gate
    rejection: one replacement per card, in order, via from_lessons.rewrite."""
    from .from_lessons import rewrite

    return rewrite(llm, topic, lesson_md, rejected, tier=tier)
