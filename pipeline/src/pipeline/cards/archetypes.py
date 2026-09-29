"""The archetype registry, read straight from `archetypes.json` at the repo root.

The app and the pipeline read the same file, so a card the pipeline writes is
always renderable by the app and always gradable by a shape the app understands.
Nothing here is copied into Python by hand: the JSON is the single source of
truth, and `eligible`, `budget` and `shape_of` all derive from it.

The budget is where the format is chosen, and it is chosen *by the pipeline, not
by the writer*. A writer asked for "a card" returns multiple choice every time
(DECISIONS round 2), which is how a corpus becomes 85% MCQ. So `budget` returns
concrete slots — one named archetype, one primitive, one difficulty target — and
the writer fills each exactly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache

from ..config import REPO_DIR

REGISTRY_PATH = REPO_DIR / "archetypes.json"

# The four answer shapes every consumer understands; `self_rate` has none.
# Kept here (not copied from the JSON) so `generate.Card` can validate a card's
# answer columns without parsing the registry every time.

# Count is proportional to importance, with a floor. With ~177 eligible topics
# at a weighted-average importance of ~0.82 this lands the corpus near 3,000
# cards, matching the round-4 target. The exact constant is a measured choice,
# not a rule: Gate 1 prices one card and the orchestrator can move it.
MIN_CARDS = 8
CARDS_PER_IMPORTANCE = 20

# The difficulty target is not a flat third. Round 3 measured the corpus as too
# easy (25 of 26 Hard cards were typed, and typed is leaving), so Medium is the
# workhorse and Hard keeps a real share; Easy stays for recall, not as the
# default the writer would otherwise drift toward.
DIFFICULTY_CYCLE = ("Easy", "Medium", "Medium", "Hard", "Medium")

# Dual-primitive archetypes (complexity, trace-the-value, estimate,
# impossible-bound) moved to numeric entry in round 3; numeric comes first, and
# pick_one stays in the corpus when a topic reuses one.
_DUAL_PRIMITIVES = ("numeric", "pick_one")


@dataclass(frozen=True)
class Archetype:
    id: str
    label: str
    primitives: tuple[str, ...]
    areas: tuple[str, ...]
    difficulties: tuple[str, ...]
    why_step: bool


@dataclass(frozen=True)
class CardSlot:
    """One thing the writer is asked for: an archetype, its primitive, and a
    difficulty target. The writer may refuse; it may not substitute."""

    archetype: str
    primitive: str
    difficulty: str


@dataclass(frozen=True)
class Registry:
    archetypes: tuple[Archetype, ...]
    shapes: dict[str, str | None]


@lru_cache(maxsize=1)
def registry() -> Registry:
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    shapes = {p["id"]: p.get("shape") for p in data["primitives"]}
    archetypes = tuple(
        Archetype(
            id=a["id"],
            label=a["label"],
            primitives=tuple(a["primitives"]),
            areas=tuple(a["areas"]),
            difficulties=tuple(a["difficulty"]),
            why_step=bool(a.get("whyStep", False)),
        )
        for a in data["archetypes"]
    )
    return Registry(archetypes=archetypes, shapes=shapes)


def by_id(archetype_id: str) -> Archetype:
    return next(a for a in registry().archetypes if a.id == archetype_id)


def shape_of(primitive: str) -> str | None:
    """The answer shape a primitive stores, or None when it stores none.

    `self_rate` (flash) has no right answer, so its shape is None; a legacy
    chunk format (`typed`, `mcq`, ...) is not a primitive and also has none.
    """
    return registry().shapes.get(primitive)


def eligible(area: str) -> list[Archetype]:
    """The archetypes the catalogue allows for an area, in registry order.

    `area` is a topic's `domain`. Areas the catalogue does not cover — `ai`,
    `lld`, `behavioral` — have no eligible archetypes and therefore no cards,
    which is the DECISIONS round-2 rule for behavioural and the honest reading
    of the catalogue for the rest.
    """
    return [a for a in registry().archetypes if area in a.areas]


def count_for(importance: float) -> int:
    return max(MIN_CARDS, round(CARDS_PER_IMPORTANCE * importance))


def pick_primitive(archetype: Archetype, occurrence: int) -> str:
    """The pipeline's pick among an archetype's primitives.

    Most archetypes have exactly one primitive. The four dual-primitive ones
    (round 3 moved them to numeric) start on numeric and alternate, so pick_one
    stays in the corpus when a topic reuses the archetype.
    """
    prims = archetype.primitives
    if len(prims) == 1:
        return prims[0]
    return _DUAL_PRIMITIVES[occurrence % 2]


def difficulty_for(archetype: Archetype, index: int) -> str:
    """The difficulty target for a slot, following the cycle and the archetype's
    own range. `flash` is Easy-only, so a slot landing on it is Easy whatever
    the cycle said."""
    target = DIFFICULTY_CYCLE[index % len(DIFFICULTY_CYCLE)]
    return target if target in archetype.difficulties else archetype.difficulties[0]


def budget(topic: dict) -> list[CardSlot]:
    """A topic's card slots: count proportional to importance, spread equally
    (round-robin) across the archetypes eligible for its domain, each with a
    difficulty target. Returns [] for a domain the catalogue does not cover."""
    area = topic.get("domain", "")
    archetypes = eligible(area)
    if not archetypes:
        return []
    n = count_for(topic.get("importance") or 0.5)
    seen: dict[str, int] = {}
    slots: list[CardSlot] = []
    for i in range(n):
        a = archetypes[i % len(archetypes)]
        occurrence = seen.get(a.id, 0)
        seen[a.id] = occurrence + 1
        slots.append(CardSlot(a.id, pick_primitive(a, occurrence), difficulty_for(a, i)))
    return slots
