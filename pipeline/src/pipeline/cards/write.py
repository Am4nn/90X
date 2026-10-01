"""Write one card for one named archetype, or refuse.

The writer is asked for exactly one archetype (and, for a dual-primitive
archetype, the pipeline's chosen primitive) and returns exactly one card — never
a different format, never several cards. It may refuse: a topic with no natural
sequence, say, has none, and a strained card is worse than an absent one. A
refusal is a valid return, not an error, and the budget refills the slot with
another archetype.

The writer fills content only. The pipeline stamps `format` (the primitive),
`archetype` and `difficulty` on every card — the writer never chooses any of
them. This is enforced in code, not asked of the model: asked for "a card" it
returns multiple choice every time (DECISIONS round 2), and asked to fill
`format` it sometimes writes the archetype id instead of the primitive.

The answer contract is the four shapes from `archetypes.json`:

- chosen   (pick_one, tap_in_place, grid_toggle)  -> `picked`: correct indices
- ordered  (order, assemble)                      -> `constraints`: [before, after] pairs
- mapping  (match, bucket, claim_grid)            -> `pairs`: [left, right] pairs
- number   (numeric)                              -> `value` + `tolerance`
- none     (self_rate)                            -> no answer columns

`options` carries the items the reader sees, in the canonical per-shape encoding
from `web/src/lib/feed/options.ts`; `constraints` and `pairs` are indices into
those items, so the grader can check the reader's order/mapping without parsing
prose.
"""

from pydantic import BaseModel, Field, ValidationError, model_validator

from ..llm import BudgetExceeded, LLMError

from . import archetypes
from .archetypes import CardSlot
from .generate import Card, WhyStep

SYSTEM = """You write interview-prep cards for the 90x Feed. You are asked for ONE card of ONE named archetype, and you write exactly that card — never a different format, never several cards.

The archetype, the primitive (how the reader answers) and the target difficulty are assigned for you in the request. Fill only the card content. Do not choose or rename the archetype or the format.

THE READER CANNOT SEE THE LESSON. The card tests whether they learned the topic, not whether they can find a sentence. Never write "the lesson", "the passage", "the text", "the above", "as described", "the reference solution". A question that only makes sense with the lesson open is broken.

The card must be answerable by a competent engineer who studied this topic anywhere, and must be something an interviewer would plausibly ask. Everything in the answer must follow from the material given. Do not invent facts, statistics, benchmarks, company names, or results.

DISTRACTORS AND WRONG REASONS. Every wrong option and every wrong reason must be a substantive mistake a real candidate makes about THIS topic — the confused pair, the off-by-one, the neighbouring concept, the wrong-but-plausible justification. A reader must be able to pick it for a reason that lives in the topic, not in the shape of the card.

Never use a structural or meta tell as a wrong option or wrong reason:
- the length, position, or alphabetical order of the options;
- a count of rows, tables, columns or steps ("classified by the number of tables involved", "ordered by row count");
- "these are common interview questions", "this is in the official documentation", "the lesson lists them in this order";
- a statement that is true but off-topic — a real fact that is not actually a reason for this specific answer.

If the material cannot support the required number of genuinely plausible wrong options or wrong reasons, refuse rather than pad. A wrong option nobody would pick is a card defect, not a formatting choice.

DIFFICULTY RUBRIC. You are given a target difficulty. Write a card that MEETS that row, not one you merely label with it. If the material cannot support a card at that difficulty for this archetype, refuse rather than soften the card.
- Easy: 1 reasoning step. No stated constraint changes the answer. Spans a single fact. Distractors need not encode real misconceptions. No calculation required.
- Medium: 2 reasoning steps. A stated constraint sometimes changes the answer. Spans a single fact. Distractors must encode real misconceptions. A calculation is optional.
- Hard: 3+ reasoning steps. A stated constraint changes the answer. Spans more than one fact. Distractors must encode real misconceptions. Needs a calculation. A Hard card also carries a why-step.

WHY-STEP (Hard only): a second question asking why the answer is right. `why_step.options` is 2-4 plausible reasons and `why_step.correct` the 0-based index of the real one. Every wrong reason must be a reason somebody actually gives for THIS answer — the plausible-but-wrong justification, never a meta-reason and never a true-but-off-topic fact. A correct answer marked wrong for its reason only punishes the reader fairly if the wrong reasons are genuinely plausible, so this is a correctness requirement, not style.

If this topic genuinely has no natural card of this archetype, return `refused` with a one-sentence reason and leave `draft` null. A refusal is a valid answer; do not force a card.

`answer` is the explanation shown after the reader answers — 1-3 sentences, including why the right answer is right. `key_points` are 2-4 short, independently checkable points. Write in plain, direct English."""

# What the reader does and what the answer columns must hold, per primitive.
# `options` carries the display items in the canonical shape the app renders
# (web/src/lib/feed/options.ts), so a list-shaped card stores a string[] and a
# match/bucket/assemble/grid card stores its object.
PRIMITIVE_INSTRUCTIONS = {
    "pick_one": (
        "PICK ONE. Ask a question with exactly one right answer. Put the 4 answer choices in "
        "`options` as a list of strings, and set `picked` to the single 0-based index of the "
        "correct one. Every wrong option must be a substantive mistake a candidate actually "
        "makes about the topic - the off-by-one, the confused pair, the neighbouring concept - "
        "never a structural tell (length, alphabetical order, position) and never a "
        "true-but-off-topic fact. An option nobody would pick is padding; if the material "
        "cannot support 3 plausible wrong options, refuse rather than pad."
    ),
    "order": (
        "ORDER. Put the N items to order in `options` as a list of strings, one item per entry, "
        "in the prompt order (do not sort them). Ask for the correct order. Set `constraints` "
        "to a list of [before, after] pairs of 0-based indices into `options` that define every "
        "correct order: every correct order satisfies all of them, and any order satisfying them "
        "is correct. If the order is fully determined, chain the adjacent pairs. Do not state a "
        "constraint the material does not support. A reader who has not studied the topic must "
        "not be able to infer the order from the items' wording (alphabetical, by length, "
        "already sorted)."
    ),
    "match": (
        "MATCH. Put the left column in `options.left` and the right column in `options.right`, "
        "each a list of strings in display order, and ask the reader to pair them. Set `pairs` "
        "to the one-to-one [[left, right], ...] mapping of 0-based indices. Every left item "
        "pairs to exactly one right item. Each left item must be confusable with more than one "
        "right item for a reader who has not studied the topic; do not pair first-to-first, "
        "second-to-second."
    ),
    "bucket": (
        "BUCKET. Put the items in `options.items` and the named buckets in `options.columns`, "
        "each a list of strings, and ask the reader to sort the items. Set `pairs` to "
        "[[item, column], ...] of 0-based indices; the same column may repeat across items. "
        "Each item has exactly one home under the rule you state. Each item must be genuinely "
        "ambiguous between at least two buckets for a reader who has not studied the topic; do "
        "not reveal an item's home by its wording."
    ),
    "tap_in_place": (
        "TAP IN PLACE. Put the snippet, plan or diagram's lines in `options` as a list of "
        "strings, one string per numbered line, in order, and ask which line or token is the "
        "answer (the bug, the bottleneck, the missing insertion point, the unsafe line). Set "
        "`picked` to the single 0-based index of that line or token."
    ),
    "self_rate": (
        "SELF-RATE (flash). Name one term or fact and ask the reader to self-rate knew-it/"
        "didn't. `answer` is the one-sentence fact. Leave `options`, `picked`, `constraints`, "
        "`pairs`, `value` and `tolerance` empty."
    ),
    "assemble": (
        "ASSEMBLE. Put the token pool in `options.tokens` as a list of strings and, where the "
        "line has pre-filled slots, `options.fixed` as one entry per token - the token index "
        "that slot is fixed to, or null for a gap the reader fills (omit `fixed` to leave every "
        "slot a gap). Ask the reader to assemble a line (a SQL clause, a method signature, a "
        "definition). Set `constraints` to [before, after] pairs of 0-based token indices "
        "defining the correct sequence; for a fully determined line, chain the adjacent pairs."
    ),
    "numeric": (
        "NUMERIC. Ask for a number - a complexity, a storage size, a row count, a lower bound. "
        "Set `value` to the expected number and `tolerance` to the allowed absolute error "
        "(exact for a count, an order of magnitude for an estimate). Leave `options` empty."
    ),
    "claim_grid": (
        "CLAIM GRID. Put the 3-4 statements in `options` as a list of strings, one statement "
        "per entry, and ask the reader to mark each true or false. Set `pairs` to "
        "[[statement, 0|1], ...] where 1 means true and 0 means false. Every statement must "
        "need knowledge of the topic to judge - not be obviously true or false from its shape "
        "or wording."
    ),
    "grid_toggle": (
        "GRID TOGGLE. Put the row labels in `options.rows` and the column labels in "
        "`options.columns`, each a list of strings (at most 3x3), and ask which cells hold. "
        "Set `picked` to the 0-based cell indices, row-major, that are correct."
    ),
}


class Refusal(BaseModel):
    """The writer's honest answer when no natural card of this archetype fits."""

    reason: str = Field(min_length=1)


# Generous output caps, one set across difficulties: a Hard card's explanation
# and a tap-in-place or assemble snippet can run long, and the writer is not
# the quality gate (the gate rejects a rambling answer later). These only stop
# the truly pathological case — a reply that has clearly run away. A reply over
# a cap fails validation, so the card is refused and the slot refills; it is
# never truncated mid-sentence.
PROMPT_MAX = 3000
ANSWER_MAX = 2000
KEY_POINT_MAX = 500
OPTION_MAX = 800


def _option_strings(options) -> list[str]:
    """Every string the reader sees as an option, from either encoding."""
    if isinstance(options, list):
        return [o for o in options if isinstance(o, str)]
    if isinstance(options, dict):
        out: list[str] = []
        for key in ("left", "right", "items", "columns", "tokens", "rows"):
            value = options.get(key)
            if isinstance(value, list):
                out += [x for x in value if isinstance(x, str)]
        return out
    return []


class CardDraft(BaseModel):
    """What the model fills. `format`, `archetype` and `difficulty` are stamped
    by the pipeline, so they are deliberately absent from this model."""

    prompt: str = Field(min_length=10, max_length=PROMPT_MAX)
    answer: str = Field(min_length=1, max_length=ANSWER_MAX)
    key_points: list[str] = Field(min_length=2, max_length=4)
    options: list[str] | dict | None = None
    picked: list[int] | None = None
    constraints: list[list[int]] | None = None
    pairs: list[list[int]] | None = None
    value: float | None = None
    tolerance: float | None = None
    why_step: WhyStep | None = None

    @model_validator(mode="after")
    def _length_guards(self):
        for pt in self.key_points:
            if len(pt) > KEY_POINT_MAX:
                raise ValueError(f"a key point is {len(pt)} chars (cap {KEY_POINT_MAX})")
        for option in _option_strings(self.options):
            if len(option) > OPTION_MAX:
                raise ValueError(f"an option is {len(option)} chars (cap {OPTION_MAX})")
        if self.why_step:
            for option in self.why_step.options:
                if len(option) > OPTION_MAX:
                    raise ValueError(f"a why-step option is {len(option)} chars (cap {OPTION_MAX})")
        return self


class WriteResult(BaseModel):
    draft: CardDraft | None = None
    refused: str | None = None

    @model_validator(mode="after")
    def _exactly_one(self):
        if (self.draft is None) == (self.refused is None):
            raise ValueError("return exactly one of `draft` or `refused`")
        return self


def _user(topic: dict, lesson_md: str, slot: CardSlot, arch: archetypes.Archetype, hard_material: str) -> str:
    instruction = PRIMITIVE_INSTRUCTIONS[slot.primitive]
    # The lesson is the one stable prefix across a topic's cards, so it goes
    # first. DeepSeek context-caches the prompt prefix, and putting the
    # per-card variable content (topic, archetype, primitive, difficulty,
    # instructions, hard material) before it would defeat that cache. Keep the
    # lesson immediately after the system prompt, then everything per-card.
    lines = [
        "Lesson:",
        lesson_md,
        "",
        f"Topic: {topic['name']} ({topic['domain']})",
        f"Archetype: {arch.label} ({slot.archetype})",
        f"Primitive: {slot.primitive}",
        f"Target difficulty: {slot.difficulty}",
        "",
        instruction,
    ]
    if hard_material:
        lines += ["", "Additional source material you may use (problem statements and pattern tricks):", hard_material]
    return "\n".join(lines)


def write_one(
    llm, topic: dict, lesson_md: str, slot: CardSlot, hard_material: str = "", tier: str = "smart",
    thinking: bool = False,
) -> Card | Refusal:
    """Write one card for one named archetype, or refuse. Never raises for a
    refusal or for a reply that does not validate — only for a provider or
    budget failure the caller must stop on.

    `thinking` is off by default: generation is from stated content, not
    diagnosis. Whether a Hard card writes better with it on is an open question
    (DECISIONS.md); the experiment that answers it runs through the
    `trial --writer-thinking` flag.
    """
    arch = archetypes.by_id(slot.archetype)
    try:
        result = llm.complete_json(SYSTEM, _user(topic, lesson_md, slot, arch, hard_material), WriteResult,
                                   tier=tier, purpose="cards-write", thinking=thinking)
    except BudgetExceeded:
        # The spend cap is a hard stop for the whole run, not a card to refill.
        raise
    except LLMError:
        # The model answered but its reply never validated (an over-length
        # draft, a malformed options shape) even after a retry. That is a
        # refusal: the slot refills with another archetype. A provider error is
        # not an LLMError, so it still propagates.
        return Refusal(reason="the writer's reply did not validate after a retry")
    if result.draft is None:
        return Refusal(reason=result.refused or "no natural card of this archetype")
    draft = result.draft
    try:
        # The pipeline assigns the format, archetype and difficulty; the writer
        # only fills content. Stamping here, and re-validating, means a confused
        # model cannot smuggle a different format through.
        return Card(
            format=slot.primitive,
            archetype=slot.archetype,
            difficulty=slot.difficulty,
            prompt=draft.prompt,
            answer=draft.answer,
            key_points=draft.key_points,
            options=draft.options,
            picked=draft.picked,
            constraints=draft.constraints,
            pairs=draft.pairs,
            value=draft.value,
            tolerance=draft.tolerance,
            why_step=draft.why_step,
        )
    except ValidationError as e:
        # Answer columns that do not match the primitive make the card malformed;
        # treat it like a refusal so the budget refills rather than saving it.
        return Refusal(reason=f"malformed answer for {slot.primitive}: {str(e).splitlines()[0]}")
