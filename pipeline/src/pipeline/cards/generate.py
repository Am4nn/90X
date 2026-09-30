"""Generate feed cards grounded in one source: a problem or a document
section. Every card tests one concept, has 2-4 key points for grading, and
must be something an interviewer would plausibly ask."""

import re
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

RULES = """Rules for every card:
- Test exactly one concept an interviewer would plausibly ask about. No trivia, no questions about the text itself ("according to the passage...").
- Everything in the answer must be supported by the source given. Don't invent facts.
- prompt: a question a candidate can answer in 1-3 sentences (typed/flash) or by picking an option (mcq).
- answer: the reference answer, 1-3 sentences.
- key_points: 2-4 short, independently checkable points a good answer must contain. They are used to grade typed answers.
- mcq: exactly 4 options, plausible distractors, `answer` must equal one option exactly.
- output: a short code snippet in the prompt (fenced), answer = exact output.
- difficulty: Easy, Medium or Hard for an interview candidate.
Write in plain, direct English."""


# Book/course sections that describe the book itself, not interview material.
NOT_CARD_WORTHY = re.compile(
    r"(?i)\b(lab projects?|homework|exercises?|preface|foreword|acknowledg\w*|table of contents|"
    r"contributing|license|references|bibliography|further reading|about the author|how to use this)\b"
)
MIN_SECTION_CHARS = 600


def is_card_worthy(doc: dict) -> bool:
    return len(doc.get("body") or "") >= MIN_SECTION_CHARS and not NOT_CARD_WORTHY.search(doc.get("title") or "")


class WhyStep(BaseModel):
    """A Hard card's second chosen answer: the reason, picked from options.

    `options` are plausible reasons somebody actually gives; `correct` is the
    0-based index of the real one. A correct answer with a wrong reason is a
    wrong card, so wrong reasons must not be implausible.
    """

    options: list[str] = Field(min_length=2, max_length=4)
    correct: int = Field(ge=0)


def _is_index(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_index_pair(pair) -> bool:
    return isinstance(pair, (list, tuple)) and len(pair) == 2 and all(_is_index(i) for i in pair)


def _is_str_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(x, str) for x in value)


def options_error(format: str, options) -> str | None:
    """Validate `options` against the primitive's `optionsShape`, or None when ok.

    This is the pipeline side of `web/src/lib/feed/options.ts` parseOptions, the
    canonical `cards.options` encoding:

      list     -> string[]                    (pick_one, order, tap_in_place, claim_grid)
      match    -> { left, right }
      bucket   -> { items, columns }
      assemble -> { tokens, fixed }           (fixed[i] is a token index or null)
      grid     -> { rows, columns }
      none     -> null                        (numeric, self_rate)

    Legacy chunk formats (typed/flash/mcq/output) are not primitives, so they
    have no optionsShape and are left to their own validators.
    """
    from .archetypes import options_shape_of

    shape = options_shape_of(format)
    if shape is None:
        return None
    if shape == "none":
        if options not in (None, [], {}):
            return f"{format} cards carry no options"
        return None
    if shape == "list":
        if not _is_str_list(options) or not options:
            return f"{format} needs `options` as a non-empty list of strings"
        return None
    if not isinstance(options, dict):
        return f"{format} needs `options` as an object ({shape})"
    if shape == "match":
        if not _is_str_list(options.get("left")) or not _is_str_list(options.get("right")) \
                or not options["left"] or not options["right"]:
            return "match options need non-empty `left` and `right` string lists"
    elif shape == "bucket":
        if not _is_str_list(options.get("items")) or not _is_str_list(options.get("columns")) \
                or not options["items"] or not options["columns"]:
            return "bucket options need non-empty `items` and `columns` string lists"
    elif shape == "assemble":
        tokens = options.get("tokens")
        if not _is_str_list(tokens) or not tokens:
            return "assemble options need a non-empty `tokens` string list"
        fixed = options.get("fixed")
        if fixed is not None:
            if not isinstance(fixed, list) or len(fixed) != len(tokens):
                return "assemble `fixed` must have one entry per token, or be omitted"
            if not all(f is None or (_is_index(f) and 0 <= f < len(tokens)) for f in fixed):
                return "assemble `fixed` entries must be a token index or null"
    elif shape == "grid":
        if not _is_str_list(options.get("rows")) or not _is_str_list(options.get("columns")) \
                or not options["rows"] or not options["columns"]:
            return "grid options need non-empty `rows` and `columns` string lists"
    return None


class Card(BaseModel):
    # `format` now holds a primitive id (pick_one, order, ...); the legacy chunk
    # formats (typed/flash/mcq/output) still parse, but the Feed v2 writer never
    # emits them. See the Feed v2 migration: cards.format becomes the primitive.
    format: str
    archetype: str | None = None
    prompt: str = Field(min_length=10)
    answer: str = Field(min_length=1)
    key_points: list[str] = Field(min_length=2, max_length=4)
    # `options` is the canonical per-shape encoding (see options_error): a flat
    # string list for "list", an object for match/bucket/assemble/grid, None for
    # "none". Legacy formats store the flat list the old writer produced.
    options: list[str] | dict[str, Any] | None = None
    difficulty: Literal["Easy", "Medium", "Hard"]
    # Per-shape answer columns, matching public.cards from the Feed v2 migration.
    picked: list[int] | None = None          # chosen: the correct indices
    constraints: list[list[int]] | None = None  # ordered: [before, after] pairs
    pairs: list[list[int]] | None = None     # mapping: [left, right] pairs
    value: float | None = None               # number: the expected value
    tolerance: float | None = None           # number: allowed absolute error
    why_step: WhyStep | None = None          # Hard cards: second chosen answer

    @model_validator(mode="after")
    def _mcq(self):
        if self.format == "mcq":
            if not self.options or len(self.options) != 4:
                raise ValueError("mcq cards need exactly 4 options")
            if self.answer not in self.options:
                raise ValueError("mcq answer must be one of the options")
        return self

    @model_validator(mode="after")
    def _options_shape(self):
        # A primitive must carry its options in the canonical shape the app
        # renders. A card whose options don't match is malformed, not fixed.
        if (err := options_error(self.format, self.options)):
            raise ValueError(err)
        return self

    @model_validator(mode="after")
    def _answer_shape(self):
        # A card whose format is a primitive must carry the answer columns of
        # its shape. Legacy formats have no shape and are not checked, which is
        # how the old chunk path (for_problem/for_document) keeps working.
        from .archetypes import shape_of

        shape = shape_of(self.format)
        if shape == "chosen":
            if not self.picked:
                raise ValueError("chosen cards need `picked` (the correct indices)")
            if not all(_is_index(i) for i in self.picked):
                raise ValueError("`picked` must be a list of integer indices")
        if shape == "ordered":
            if not self.constraints:
                raise ValueError("ordered cards need `constraints` ([before, after] pairs)")
            if not all(_is_index_pair(p) for p in self.constraints):
                raise ValueError("`constraints` must be a list of [before, after] index pairs")
        if shape == "mapping":
            if not self.pairs:
                raise ValueError("mapping cards need `pairs` ([left, right] pairs)")
            if not all(_is_index_pair(p) for p in self.pairs):
                raise ValueError("`pairs` must be a list of [left, right] index pairs")
        if shape == "number" and (self.value is None or self.tolerance is None):
            raise ValueError("number cards need `value` and `tolerance`")
        return self


class CardSet(BaseModel):
    cards: list[Card] = Field(min_length=1, max_length=5)


PROBLEM_SYSTEM = f"""You write interview-prep flashcards from a LeetCode problem and its reference solution.
Write 2-3 cards:
1. typed: "Which pattern / approach fits this problem, and why?" (describe the problem briefly in the prompt; never name it by its title).
2. typed or flash: the key insight or invariant that makes the optimal solution work, or its time/space complexity with the reason.
3. optionally mcq: a common wrong approach vs the right one.
{RULES}"""

DOC_SYSTEM = f"""You write interview-prep flashcards from one section of study material.
Write 2-4 cards on the most interview-relevant ideas in the section. Prefer "why" and trade-off questions over definitions.
Use a mix of formats: typed for explanations, flash for crisp facts, mcq when there are clear wrong alternatives,
output only for a code snippet whose output follows from the section.
If the section has nothing interview-relevant, return one flash card on its most useful fact.
{RULES}"""


def for_problem(llm, problem: dict, tier: str = "smart") -> list[dict]:
    user = (
        f"Problem: {problem['title']} ({problem['difficulty']}), pattern: {problem.get('pattern') or 'unknown'}\n\n"
        f"Statement:\n{problem['statement'][:4000]}\n\nReference solution:\n{(problem.get('solution') or '')[:3000]}"
    )
    result = llm.complete_json(PROBLEM_SYSTEM, user, CardSet, tier=tier, purpose="cards-problem")
    return [{**c.model_dump(), "problem_slug": problem["slug"], "document_id": None,
             "topic_slug": problem.get("pattern_slug")} for c in result.cards]


def for_document(llm, doc: dict, tier: str = "smart") -> list[dict]:
    user = f"Area: {doc['domain']}\nSection: {doc['title']}\n\n{doc['body'][:6000]}"
    result = llm.complete_json(DOC_SYSTEM, user, CardSet, tier=tier, purpose="cards-doc")
    return [{**c.model_dump(), "problem_slug": None, "document_id": doc["id"],
             "topic_slug": doc.get("topic_slug")} for c in result.cards]
