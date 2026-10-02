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

**Ordered stages, because one rigid rule was killing good cards.** The first
version asked for a single verdict from one enum, so a format opinion and a
substance opinion competed for the same slot - and the reviewing model used it
to reject a perfectly good `output` card with "Format 'output' is not one of
the allowed card formats (flash, typed, mcq)", while 69 output cards were
already published. It had invented a restriction the prompt does not contain.

So the stages now run in order, and the two cheap deterministic ones run first:

1. **schema** - in code. A format from our own enum is legal by construction,
   and the model is never asked otherwise. Structure is checked here instead:
   four options on a multiple-choice card, a snippet on an output card.
2. **grounding** - in code. Does the question point at material the reader
   cannot see?
3. **answerable** - the model. Could a competent engineer answer it as asked?
4. **format fit** - the model, asked separately. Does the honest answer fit the
   format it was given? Never "is this format allowed".
5. **gradable** - the model. Can it be marked the way this format is marked?

Two more checks run ahead of the model stages. The **structural rules**
(`structure.py`) are free and deterministic, catching an option that gives the
answer away by shape before anyone pays to read it. The **blind gate**
(`blind_gate.py`) shows a model only the answer choices and rejects a card it
can answer without the lesson — the reader-side check this reviewer cannot make
from the question alone.

A card failing only stage 4 or 5 is a wording problem the rewrite usually
fixes; one failing stage 1, 2 or 3 is a worse card. Reporting the earliest
failure keeps the reason honest, so the repair pass is told what is actually
wrong rather than the last thing the reviewer happened to mention.
"""

import re

from pydantic import BaseModel, Field

from ..lessons.check import REFERS_TO_SOURCE
from . import archetypes, structure, wellformed

FENCED_SNIPPET = re.compile(r"```.*?```", re.DOTALL)
MCQ_OPTIONS = 4
# A reason that says our format list does not contain this format is the model
# overstepping: formats come from the enum, not from its opinion. The test is
# narrow on purpose - it must name the permitted set, by listing format names or
# by saying "one of". An earlier, looser version also matched a real objection
# like "this format is not valid for exact-match grading" and threw it away.
DENIES_THE_FORMAT = re.compile(
    r"\bformats?\b[^.]{0,60}?\b(?:not|isn't)\b[^.]{0,30}?"
    r"(?:one of|among|in the (?:list|set)|allowed formats|supported formats|valid formats)",
    re.IGNORECASE,
)

SYSTEM = f"""You are checking interview-prep cards. You see only the questions, exactly as a candidate sees them. You do NOT see the material they were written from, and that is deliberate.

There are exactly four card formats and all four are valid. This is settled and not yours to rule on:
- "typed" is free prose of one to three sentences, graded by a model against key points. It is NOT an exact-match answer box. An open-ended conceptual question - "why does this work", "what is the trade-off", "when would you not use it" - is the BEST kind of typed card. Never object to a typed card for being conceptual, open-ended, or requiring explanation. That is the format working as intended.
- "flash" is one crisp sentence.
- "mcq" is {MCQ_OPTIONS} options with one unambiguously correct.
- "output" shows a short code snippet and asks what it prints or returns, graded by exact match after whitespace is normalised.

For each card, answer four separate questions. Keep them separate: a card can be perfectly answerable and still be in the wrong format, and saying so in the wrong field loses the distinction.

1. `answerable` - could a competent engineer who has studied this topic answer this question as asked? Set it false only when something is genuinely missing or the question is ambiguous: it points at a specific solution, passage, diagram, snippet, example or bare variable the candidate cannot see, or several different answers would all be correct. Needing to know the topic well is not a reason.

2. `fits_archetype` - does the question do what "the question must" line above the card says? That line is the archetype's definition, not a hint: judge the question against it literally. A card can be excellent and still fail this, and a well-written question about something else is exactly the case to catch - a design-principle question under output prediction is a mismatch, not a bad card. Examples of the requirement: `output-prediction` must ask what the code prints or returns, `tap-the-bug` must ask which line is wrong, `which-approach` must ask which approach fits, `estimate` must ask for a quantity. Do not invent requirements the line does not state: it is about what the question asks, never about difficulty, option quality or grading.

3. `fits_format` - does the honest answer fit the format this card was given? This is about the answer's shape, never about whether the format is permitted - all four are.
   - typed: false only when the honest answer is a list of items to enumerate ("name the four isolation levels"), where the candidate cannot know how many you want, or when it truly needs several paragraphs.
   - flash: false when the honest answer needs a paragraph.
   - output: false when the snippet could print more than one thing - a timestamp, hash ordering, a locale.

4. `gradable` - can it be marked the way this format is marked? An output card whose expected text has no single obvious spelling (the delimiters of a SQL result set, say) is not gradable. A multiple-choice card with two defensible options is not gradable.

Give a short `reason` for each field you set false, and leave it empty otherwise.

Give `confidence` from 0 to 1 on every card: how sure you are it is fair and well formed. A card you would happily put in front of a candidate is near 1; one you are letting through with reservations is near 0.5. The review screen shows the least confident first, so this decides what a human looks at.

For multiple-choice cards, also give the option you would pick, copied exactly.

Do not comment on style, difficulty, or what you would have asked instead. Marking a good card as bad costs us a real question, so when a card is fair, say so."""


class Verdict(BaseModel):
    index: int = Field(description="the card's position in the list, starting at 0")
    answerable: bool = Field(default=True, description="a competent engineer could answer it as asked")
    fits_format: bool = Field(default=True, description="the honest answer fits the format given")
    # No default of True. A safety check that treats an omitted field as "fine"
    # fails open: the model simply not answering this question would pass every
    # mismatch silently, which is the opposite of what the check is for. None
    # means "did not answer", and for a card that has an archetype that is a
    # rejection, not a pass.
    fits_archetype: bool | None = Field(default=None, description="the question asks what its archetype names")
    gradable: bool = Field(default=True, description="it can be marked the way this format is marked")
    reason: str = Field(default="", description="one short sentence for whichever field is false")
    picked: str = Field(default="", description="multiple choice only: the option you would pick")
    confidence: float = Field(default=0.5, ge=0, le=1,
                              description="how sure you are this card is fair and well formed")


class GateResult(BaseModel):
    verdicts: list[Verdict]


def prompt_only(card) -> str:
    """What the gate is allowed to see.

    The archetype is included because nothing else checked that a card asks what
    its archetype names. A card filed under `output-prediction` asked which SOLID
    principle a design violates, and every gate passed it: `wellformed` checks the
    answer's shape, the blind gate checks guessability, and `fits_format` asks
    whether the answer fits the screen. None of them asks whether the question is
    the one the archetype promised.
    """
    archetype = getattr(card, "archetype", None)
    lines = []
    if archetype:
        try:
            found = archetypes.by_id(archetype)
            lines.append(f"archetype: {found.label} ({archetype})")
            if found.intent:
                lines.append(f"the question must: {found.intent}")
        except StopIteration:
            lines.append(f"archetype: {archetype}")
    lines += [f"format: {card.format}", f"question: {card.prompt}"]
    if card.format == "mcq" and card.options:
        lines += [f"  option: {o}" for o in card.options]
    return "\n".join(lines)


def review(llm, topic: dict, cards: list, tier: str = "smart") -> GateResult:
    body = "\n\n".join(f"[{i}]\n{prompt_only(c)}" for i, c in enumerate(cards))
    user = f"Topic: {topic['name']} ({topic['domain']})\n\n{body}"
    return llm.complete_json(SYSTEM, user, GateResult, tier=tier, purpose="card-gate")


def confidence_by_card(cards: list, result: GateResult) -> dict[int, float]:
    """How sure the gate was, keyed by `id(card)`.

    The verdicts arrive keyed by position, and a caller holding cards rather
    than indices has to join the two. Returning the position-keyed map and
    letting callers guess cost every one of 2,804 cards its score: the re-gate
    looked its cards up by `id(card)` in a map keyed by index, missed every
    time, and stored the 0.5 fallback. That is the column the review screen
    sorts on, so nothing could be shown least-confident-first.
    """
    scores = {v.index: v.confidence for v in result.verdicts}
    return {id(card): scores.get(i, 0.5) for i, card in enumerate(cards)}


def malformed(card) -> str:
    """Stage 1, in code: is the card structurally what its format requires?

    Nothing here asks whether a format is allowed. Every format in the enum is,
    and leaving that to a model is how a valid output card got thrown away for
    a rule nobody wrote.
    """
    if card.format == "mcq":
        options = card.options or []
        if len(options) != MCQ_OPTIONS:
            return f"multiple choice needs {MCQ_OPTIONS} options, has {len(options)}"
        if card.answer.strip() not in {o.strip() for o in options}:
            return "the marked answer is not one of the options"
    if card.format == "output" and not FENCED_SNIPPET.search(card.prompt):
        return "an output card must show the snippet it is asking about"
    return ""


def judge(cards: list, result: GateResult) -> list[tuple[object, str]]:
    """Returns (card, reason) for every card that must not ship.

    The stages are checked in order and the first failure is the one reported,
    so the repair pass is told the most fundamental thing that is wrong instead
    of whatever the reviewer mentioned last.

    A card the reviewer never ruled on is rejected, not kept. Keeping it means
    a short or truncated reply silently passes questions nobody checked, and
    the phrase-matching fallback only catches the obvious ones. Rejected is
    not deleted: these go through the repair pass and are gated again, so an
    omission costs a retry rather than a card.
    """
    verdicts = {v.index: v for v in result.verdicts}
    rejected = []
    for i, card in enumerate(cards):
        if problem := malformed(card):
            rejected.append((card, f"malformed: {problem}"))
            continue
        # Structural rules run before any model verdict: an option that is the
        # only number, the only code block, far out of length band, or an "all
        # of the above" gives the answer away by shape, which the reviewer and
        # the blind gate cannot see. Free and deterministic.
        if probs := structure.problems(card):
            rejected.append((card, f"guessable by shape: {probs[0]}"))
            continue
        # Well-formedness runs here too, and covers every primitive rather than
        # just pick_one: item counts against the registry's limits, repeated
        # options that make two indices equally correct, a mapping the answer
        # screen cannot express, constraints that cycle. Also free, and the
        # first full run shipped 241 cards that fail it.
        if probs := wellformed.problems(card):
            rejected.append((card, f"not well formed: {probs[0]}"))
            continue
        if m := REFERS_TO_SOURCE.search(card.prompt):
            rejected.append((card, f"refers to unseen material: {m.group(0)!r}"))
            continue
        v = verdicts.get(i)
        if v is None:
            rejected.append((card, "the reviewer did not rule on this card"))
            continue
        # The model may not overrule the format enum. A card whose only
        # objection is that its format "is not one of the allowed formats" has
        # no objection. This applies to the format verdict alone: a gradability
        # objection is about marking, and suppressing it here let an ungradable
        # card stay publishable.
        denied_the_format = bool(DENIES_THE_FORMAT.search(v.reason))
        if not v.answerable:
            rejected.append((card, f"not answerable: {v.reason}"))
        elif getattr(card, "archetype", None) and v.fits_archetype is not True:
            # Anything but an explicit True: a stated mismatch, or no answer at
            # all. A legacy card has no archetype to fit, so it is not asked.
            why = v.reason if v.fits_archetype is False else "the gate did not rule on whether it fits its archetype"
            rejected.append((card, f"wrong archetype: {why}"))
        elif not v.fits_format and not denied_the_format:
            rejected.append((card, f"wrong_format: {v.reason}"))
        elif not v.gradable:
            rejected.append((card, f"not gradable: {v.reason}"))
        elif card.format == "mcq" and v.picked and v.picked.strip() != card.answer.strip():
            rejected.append((card, "a competent answer disagrees with the marked option"))
    return rejected
