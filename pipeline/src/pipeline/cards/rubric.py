"""The difficulty rubric, in code: DECISIONS round 3's table as a pure score.

The writer labels its own difficulty and, asked for "a card", drifts toward
Easy. The rubric scores the card's stated properties instead, so difficulty is
a measurement rather than an opinion stored as data.

The five properties are content judgements a card does not store as fields, so
`score` takes them directly. The pipeline writes the rubric's answer; the
writer's label is ignored.
"""

from dataclasses import dataclass

EASY = "Easy"
MEDIUM = "Medium"
HARD = "Hard"

_RANK = {EASY: 0, MEDIUM: 1, HARD: 2}

# Each row of the round-3 table maps its own column's values to a level; the
# card's difficulty is the hardest level any property reaches.
_CONSTRAINT_LEVEL = {"no": EASY, "sometimes": MEDIUM, "yes": HARD}
_CALCULATION_LEVEL = {"no": EASY, "maybe": MEDIUM, "yes": HARD}


@dataclass(frozen=True)
class Properties:
    """A card's stated properties, as the round-3 table names them."""

    reasoning_steps: int
    constraint_changes_answer: str  # "no" | "sometimes" | "yes"
    spans_facts: bool
    misconception_distractors: bool  # "not required" -> False, "yes" -> True
    needs_calculation: str  # "no" | "maybe" | "yes"

    def __post_init__(self) -> None:
        if self.reasoning_steps < 1:
            raise ValueError("reasoning_steps must be at least 1")
        if self.constraint_changes_answer not in _CONSTRAINT_LEVEL:
            raise ValueError(
                f"constraint_changes_answer must be one of {tuple(_CONSTRAINT_LEVEL)}"
            )
        if self.needs_calculation not in _CALCULATION_LEVEL:
            raise ValueError(
                f"needs_calculation must be one of {tuple(_CALCULATION_LEVEL)}"
            )


def score(p: Properties) -> str:
    """The difficulty the round-3 table assigns to these properties.

    Each property lands on a difficulty level; the card takes the hardest one.
    A Medium card with a calculation and several facts is Hard, whatever its
    reasoning-step count says, because "needs a calculation" and "spans more
    than one fact" are Hard rows.
    """
    levels = [
        HARD if p.reasoning_steps >= 3 else MEDIUM if p.reasoning_steps == 2 else EASY,
        _CONSTRAINT_LEVEL[p.constraint_changes_answer],
        HARD if p.spans_facts else EASY,
        MEDIUM if p.misconception_distractors else EASY,
        _CALCULATION_LEVEL[p.needs_calculation],
    ]
    return max(levels, key=_RANK.get)
