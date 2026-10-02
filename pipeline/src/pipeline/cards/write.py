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
- none     (self_rate, compose)                   -> no answer columns

`options` carries the items the reader sees, in the canonical per-shape encoding
from `web/src/lib/feed/options.ts`; `constraints` and `pairs` are indices into
those items, so the grader can check the reader's order/mapping without parsing
prose.
"""

import re

from pydantic import BaseModel, Field, ValidationError, model_validator

from ..llm import BudgetExceeded, LLMError

from . import archetypes
from .archetypes import CardSlot
from .generate import Card, WhyStep

SYSTEM = """You write interview-prep cards for the 90x Feed. You are asked for ONE card of ONE named archetype, and you write exactly that card — never a different format, never several cards.

The archetype, the primitive (how the reader answers) and the target difficulty are assigned for you in the request. Fill only the card content. Do not choose or rename the archetype or the format.

THE READER CANNOT SEE THE LESSON. The card tests whether they learned the topic, not whether they can find a sentence. Never write "the lesson", "the passage", "the text", "the above", "as described", "the reference solution". A question that only makes sense with the lesson open is broken.

The card must be answerable by a competent engineer who studied this topic anywhere, and must be something an interviewer would plausibly ask. Everything in the answer must follow from the material given. Do not invent facts, statistics, benchmarks, company names, or results.

ONE ANSWER, OR REFUSE. A question that asks for the "best", "fastest", "most likely", "cheapest", or asks the reader to "rank" has one right answer only under assumptions the reader is told: the workload, capacity, implementation, or the exact metric being ranked. State those assumptions in `prompt` (for example "queries are dominated by per-tenant lookups", "standard implementation", "no extra memory"). If the right answer genuinely changes with a factor the material does not pin down, refuse rather than grade a reader against an unstated assumption.

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

WHY-STEP (Hard only): a second question asking why ONE specific part of the answer is right. `why_step.options` is 2-4 plausible reasons and `why_step.correct` the 0-based index of the real one.

The correct reason must state the SAME conclusion as `answer`. If `answer` says the change improves throughput, the correct reason explains why it improves; it may never argue the opposite. A correct reason that contradicts `answer` is a wrong card.

Every wrong reason must be a FALSE statement about the very item, pair, row, or value the correct reason is about — the plausible mistake a candidate makes on THAT item. Never a true statement about a different item, and never a true-but-off-topic edge case:
- match / bucket / claim_grid / grid_toggle: ask why one specific pair or cell is right. Wrong reasons are false claims about that same pair (the swap, the near-miss), not true descriptions of a different pair in the card.
- numeric: wrong reasons must justify a WRONG number — the reasoning or arithmetic error that produces a different value — never a caveat that is actually true of the correct value.
- pick_one / order / tap_in_place / assemble: wrong reasons are false claims about that same answer.

A correct answer marked wrong for its reason only punishes the reader fairly if the wrong reasons are genuinely plausible, so this is a correctness requirement, not style.

Never write your reasoning, hedging, or self-correction into any field. If you reconsider an answer, replace the field with the final value. Do not leave "wait", "let me re-evaluate", "I need to adjust", or any chain of thought in `prompt`, `answer`, `key_points`, `options`, `picked`, `pairs`, `constraints`, `value`, `tolerance`, or `why_step`.

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
        "in a SHUFFLED order: the order you list them in must NOT be the correct order, and must "
        "not be alphabetical or by length, so a reader has to rearrange them. Ask for the correct "
        "order. Set `constraints` to a list of [before, after] pairs of 0-based indices into the "
        "SHUFFLED `options` that define every correct order: every correct order satisfies all of "
        "them, and any order satisfying them is correct. If the order is fully determined, chain "
        "the adjacent pairs. Do not state a constraint the material does not support."
    ),
    "match": (
        "MATCH. Put the left column in `options.left` and the right column in `options.right`, "
        "each a list of strings. List the RIGHT column in a SHUFFLED order, so the correct "
        "pairing is not left[i] with right[i] - a reader must not be able to match items by "
        "position. Set `pairs` to the one-to-one [[left, right], ...] mapping of 0-based "
        "indices into those shuffled lists. Every left item pairs to exactly one right item. "
        "Each left item must be confusable with more than one right item for a reader who has "
        "not studied the topic."
    ),
    "bucket": (
        "BUCKET. Put the items in `options.items` and the named buckets in `options.columns`, "
        "each a list of strings, and ask the reader to sort the items. List the ITEMS in a "
        "SHUFFLED order, so their homes are not revealed by position or by a one-to-one "
        "pattern. Set `pairs` to [[item, column], ...] of 0-based indices; the same column may "
        "repeat across items. Each item has exactly one home under the rule you state. Each "
        "item must be genuinely ambiguous between at least two buckets for a reader who has "
        "not studied the topic; do not reveal an item's home by its wording."
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
    "compose": (
        "COMPOSE. The reader writes their own short answer - 2 to 3 sentences, no more - and it "
        "is marked against `key_points`, so those are the rubric rather than a summary. Ask for "
        "something a reader can answer about their OWN experience or their own wording; never ask "
        "for a fact with one right phrasing, because a short written answer is the wrong screen "
        "for that. `prompt` states what the answer must contain, in the reader's terms (for "
        "example 'name the situation, what you did, and the result, in three sentences'). "
        "`key_points` are 3 or 4 short, independently checkable requirements, each one a thing "
        "the answer either does or does not do - 'states a specific measurable result', 'says "
        "what the candidate personally did rather than the team' - and never a matter of taste. "
        "`answer` is a model answer of the same length, which the reader sees afterwards as an "
        "example rather than as the right answer. Leave `options`, `picked`, `constraints`, "
        "`pairs`, `value` and `tolerance` empty."
    ),
    "assemble": (
        "ASSEMBLE. Put the token pool in `options.tokens` as a list of strings in a SHUFFLED "
        "order - the tokens must not already be in the order they are assembled into, so a "
        "reader has to rearrange them. Where the line has pre-filled slots, set `options.fixed` "
        "as one entry per token - the token index that slot is fixed to, or null for a gap the "
        "reader fills (omit `fixed` to leave every slot a gap); the pre-filled slots must not by "
        "themselves spell out the answer. Ask the reader to assemble a line (a SQL clause, a "
        "method signature, a definition). Set `constraints` to [before, after] pairs of 0-based "
        "token indices defining the correct sequence; for a fully determined line, chain the "
        "adjacent pairs."
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

# The writer's chain of thought must never reach a field the reader sees. These
# are the self-correction and narration markers it leaves when it reasons inside
# `answer` or an option instead of writing the final value — the same leak that
# put "Wait, ... let me re-evaluate ... I need to adjust the picked indices" into
# a grid-toggle answer. A field matching any of them is rejected rather than
# shipped.
# Deliberately narrow: only markers a writer uses to correct its own in-progress
# answer. Ordinary reader-facing words a valid card can legitimately quote —
# "wait,", "I meant", "let me check/verify/adjust" — are left out on purpose.
REASONING_LEAK = re.compile(
    r"(?i)(?:"
    r"\blet me (?:re-?evaluat\w*|reconsider\w*|think|redo|fix)\b|"
    r"\bi (?:need|should|will|have) to (?:adjust|reconsider|correct|fix|redo)\b|"
    r"\bscratch that\b|\bon second thought\b|\bupon (?:reflection|reconsideration)\b"
    r")"
)


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

    @model_validator(mode="after")
    def _no_reasoning_leak(self):
        # Reasoning or self-correction left in a reader-facing field is a broken
        # card: the reader sees the writer's deliberation, and the answer often
        # disagrees with itself mid-sentence.
        fields = [self.prompt, self.answer, *self.key_points, *_option_strings(self.options)]
        if self.why_step:
            fields += self.why_step.options
        for field in fields:
            if REASONING_LEAK.search(field):
                raise ValueError("a field carries the writer's reasoning or self-correction; write only the final value")
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
