"""Re-derive a card's answer key from its own explanation.

A card whose key contradicts its explanation has one of two defects, and the audit cannot
say which: the key is wrong, or the explanation is. This repairs the first kind by treating
the explanation as the authority. It is the author's own justification of the answer, so it
is the only evidence there is of what they meant, and a model that reads it can say what key
it describes.

Two rules keep that from making things worse.

The model never computes a stored index. A grid stores `row * columns + column`, and a model
asked for that number got it wrong in about half the grids it wrote, which is how the cards
this repairs came to exist. So the model names things in a numbering it can read off the page
(row 2, column 0; statement 3 is true; token 5 comes first) and the code turns that into the
columns the card stores.

And a part the explanation does not settle comes back as null, and a card with any null part
is not repaired. A guess would produce a key that agrees with the explanation by construction,
which makes the audit useless as a check on it.

Agreement with the explanation is not truth. If the explanation is itself wrong, this
faithfully copies the error. That is why a repaired card still goes back through the audit
with two models of different families before it is trusted.
"""

import json

from pydantic import BaseModel, Field

from . import archetypes
from .write import grid_picked


def _load(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return None
    return value


class Choice(BaseModel):
    choice: int | None = Field(description="the number of the option the explanation says is right, or null if it does not settle it")
    reason: str = Field(default="", description="one short clause")


class RowTicks(BaseModel):
    row: int
    columns: list[int] = Field(description="the numbers of the columns the explanation says hold for this row; empty if none do")


class Grid(BaseModel):
    ticks: list[RowTicks] | None = Field(description="one entry per row, or null if the explanation does not settle the grid")
    reason: str = ""


class Verdict(BaseModel):
    statement: int
    true: bool | None = Field(description="whether the explanation says this statement is true; null if it does not say")


class Claims(BaseModel):
    verdicts: list[Verdict]
    reason: str = ""


class Order(BaseModel):
    order: list[int] | None = Field(description="the numbers of the tokens in the order they form the line, or null if the explanation does not settle it")
    reason: str = ""


class Number(BaseModel):
    value: float | None = Field(description="the number the explanation gives as the answer, or null")
    reason: str = ""


class Pairs(BaseModel):
    pairs: list[list[int]] | None = Field(description="[left number, right number] pairs, or null if the explanation does not settle them")
    reason: str = ""


class Placements(BaseModel):
    placements: list[list[int]] | None = Field(description="[item number, column number] for every item, or null if the explanation does not settle them")
    reason: str = ""


SCHEMA = {
    "pick_one": Choice, "tap_in_place": Choice, "grid_toggle": Grid, "claim_grid": Claims,
    "assemble": Order, "numeric": Number, "match": Pairs, "bucket": Placements,
}

SYSTEM = """You are repairing the answer key of a study card whose key and explanation disagree.

The explanation is what the card's author wrote to justify the answer, so it is the authority on what the key should be. Read it, and give the key it describes, using the numbering shown on the card.

Rules:
- Take the explanation at its word. Do not overrule it with your own knowledge of the subject, even if you think it is mistaken.
- If the explanation numbers statements ("statements 1 and 3 are true"), those numbers may not match the numbering shown here. Match statements by what they say, not by their number.
- If the explanation does not settle some part of the key, give null for that part. Do not guess. A null is the right answer whenever you would be inventing something.
- For a card where the reader taps a line, the key is the line the explanation names as the problem (the bug, the bottleneck, the insertion point).

Reply with JSON only, in the shape asked for."""


def numbered(card) -> list[str]:
    """What the card shows, with a number on everything the key can refer to."""
    options = _load(getattr(card, "options", None))
    fmt = card.format
    lines: list[str] = []
    if fmt in ("pick_one", "tap_in_place") and isinstance(options, list):
        lines += [f"  option {i}: {t}" for i, t in enumerate(options)]
    elif fmt == "claim_grid" and isinstance(options, list):
        lines += [f"  statement {i}: {t}" for i, t in enumerate(options)]
    elif fmt == "grid_toggle" and isinstance(options, dict):
        lines += [f"  row {i}: {t}" for i, t in enumerate(options.get("rows") or [])]
        lines += [f"  column {j}: {t}" for j, t in enumerate(options.get("columns") or [])]
    elif fmt == "assemble" and isinstance(options, dict):
        lines += [f"  token {i}: {t}" for i, t in enumerate(options.get("tokens") or [])]
    elif fmt == "match" and isinstance(options, dict):
        lines += [f"  left {i}: {t}" for i, t in enumerate(options.get("left") or [])]
        lines += [f"  right {j}: {t}" for j, t in enumerate(options.get("right") or [])]
    elif fmt == "bucket" and isinstance(options, dict):
        lines += [f"  item {i}: {t}" for i, t in enumerate(options.get("items") or [])]
        lines += [f"  column {j}: {t}" for j, t in enumerate(options.get("columns") or [])]
    return lines


ASK = {
    "pick_one": "Give `choice`: the number of the one option the explanation says is right.",
    "tap_in_place": "Give `choice`: the number of the one line the explanation names as the answer.",
    "grid_toggle": "Give `ticks`: for every row, the numbers of the columns the explanation says hold for it.",
    "claim_grid": "Give `verdicts`: for every statement, whether the explanation says it is true.",
    "assemble": "Give `order`: the numbers of ALL the tokens, in the order they form the line.",
    "numeric": "Give `value`: the number the explanation gives as the answer (an exponent, a count, a ratio, as the question asks).",
    "match": "Give `pairs`: [left number, right number] for every left item.",
    "bucket": "Give `placements`: [item number, column number] for every item.",
}


def derive(llm, card, tier: str = "smart"):
    """Ask what key the explanation describes. None when the primitive cannot be repaired."""
    schema = SCHEMA.get(card.format)
    if schema is None:
        return None
    user = "\n".join([
        f"format: {card.format}",
        f"question: {card.prompt}",
        *numbered(card),
        "explanation:",
        f"  {(getattr(card, 'answer', '') or '').strip()}",
        "",
        ASK[card.format],
    ])
    return llm.complete_json(SYSTEM, user, schema, tier=tier, purpose="key-repair")


def _permutation(values, size: int) -> bool:
    return isinstance(values, list) and sorted(values) == list(range(size))


def new_key(card, derived) -> dict | None:
    """The stored columns the derived key implies, or None if any part is unsettled or invalid.

    Returns only the columns that change (`picked`, `pairs`, `constraints` or `value`). The
    arithmetic from numbers the model can read to indices the card stores happens here, never
    in the model.
    """
    if derived is None:
        return None
    options = _load(getattr(card, "options", None))
    fmt = card.format

    if fmt in ("pick_one", "tap_in_place"):
        n = len(options) if isinstance(options, list) else 0
        choice = derived.choice
        return {"picked": [choice]} if isinstance(choice, int) and 0 <= choice < n else None

    if fmt == "grid_toggle":
        if derived.ticks is None or not isinstance(options, dict):
            return None
        rows = len(options.get("rows") or [])
        seen = [t.row for t in derived.ticks]
        if sorted(seen) != list(range(rows)):  # every row, once
            return None
        cells = [[t.row, c] for t in derived.ticks for c in t.columns]
        picked = grid_picked(options, cells)
        return {"picked": picked} if picked is not None else None

    if fmt == "claim_grid":
        n = len(options) if isinstance(options, list) else 0
        said = {v.statement: v.true for v in derived.verdicts}
        if sorted(said) != list(range(n)) or any(v is None for v in said.values()):
            return None
        return {"pairs": [[i, 1 if said[i] else 0] for i in range(n)]}

    if fmt == "assemble":
        tokens = options.get("tokens") if isinstance(options, dict) else None
        if not isinstance(tokens, list) or not _permutation(derived.order, len(tokens)):
            return None
        order = derived.order
        return {"constraints": {"before": [[order[i], order[i + 1]] for i in range(len(order) - 1)]}}

    if fmt == "numeric":
        return {"value": derived.value} if derived.value is not None else None

    if fmt == "match":
        left = len(options.get("left") or []) if isinstance(options, dict) else 0
        right = len(options.get("right") or []) if isinstance(options, dict) else 0
        pairs = derived.pairs
        if not pairs or any(len(p) != 2 for p in pairs):
            return None
        if sorted(p[0] for p in pairs) != list(range(left)) or sorted(p[1] for p in pairs) != list(range(right)):
            return None
        return {"pairs": [list(p) for p in pairs]}

    if fmt == "bucket":
        items = len(options.get("items") or []) if isinstance(options, dict) else 0
        columns = len(options.get("columns") or []) if isinstance(options, dict) else 0
        placed = derived.placements
        if not placed or any(len(p) != 2 for p in placed):
            return None
        if sorted(p[0] for p in placed) != list(range(items)) or any(not 0 <= p[1] < columns for p in placed):
            return None
        return {"pairs": [list(p) for p in placed]}

    return None


def can_repair(fmt: str) -> bool:
    return fmt in SCHEMA and archetypes.options_shape_of(fmt) is not None
