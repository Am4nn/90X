"""Bring cards that overshoot a registry limit back inside it, by trimming.

302 cards are rejected as not well formed. Most of those reasons need a writer -
tokens below the minimum cannot be invented, and a claim grid where every claim
is true needs a different claim. But one family is arithmetic: a card that offers
seven options against a maximum of six, four columns against three, six rows
against five. Nothing has to be written to fix those. Something has to go.

The rule that governs every line below: **a trim must carry the answer key with
it, or refuse.** `wellformed.problems` checks that a key is well formed, not that
it still points at the same content. A column dropped from a grid leaves every
flat cell index in range while moving each one to a different cell, and the
validator accepts the result. The first version of this script did exactly that
and put a card with a wrong answer key into production. So the validator is a
second guard, never the only one:

  - Anything the answer key names - `picked`, the ordering `constraints`, the
    cells ticked in a grid, the token pre-filled in an assemble slot - is
    protected from being dropped, and re-indexed when something before it goes.
  - A key in a shape this script does not understand is a reason to leave the
    card alone, not to guess.
  - Every trim is then re-checked with `wellformed.problems` and written only if
    it comes back empty.

It also prefers to drop an entry the answer prose does not mention, so the
explanation cannot end up describing a choice that is no longer on screen.

Nothing below a minimum is touched. Those need content, and this script has none.

Run from `pipeline/`. Dry run unless called with --apply.
"""

import json
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, "src")

import duckdb

from pipeline.cards import archetypes, wellformed

APPLY = "--apply" in sys.argv


def load(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return None
    return value


def as_card(row, cols):
    card = SimpleNamespace(**dict(zip(cols, row)))
    for field in ("options", "picked", "constraints", "pairs", "why_step"):
        setattr(card, field, load(getattr(card, field, None)))
    return card


def unwrap(value):
    """The ordering pairs inside `constraints`, and whether they were wrapped.

    The writer produces a flat list; the database stores `{"before": [...]}`. The
    first version iterated the wrapper as if it were the list, got the string
    "before" for a pair, and silently produced no constraints at all - which is why
    two dozen ordered cards were discarded as "constraints missing or malformed"
    when the cards were fine.

    Returns `(None, wrapped)` for anything that is not a list of int pairs, so the
    caller can refuse rather than guess.
    """
    wrapped = isinstance(value, dict)
    inner = value.get("before") if wrapped else value
    if not isinstance(inner, list):
        return None, wrapped
    out = []
    for pair in inner:
        if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
            return None, wrapped
        if not all(isinstance(n, int) and not isinstance(n, bool) for n in pair):
            return None, wrapped
        out.append([int(pair[0]), int(pair[1])])
    return out, wrapped


def rewrap(pairs, wrapped):
    return {"before": pairs} if wrapped else pairs


def keep_order(count: int, drop: set[int]) -> list[int]:
    """The surviving indices, in order, so old positions can be remapped."""
    return [i for i in range(count) if i not in drop]


def remap(pairs, keep_a: list[int], keep_b: list[int] | None = None):
    """Rewrite index pairs after a trim, dropping any pair that lost a side."""
    a = {old: new for new, old in enumerate(keep_a)}
    b = a if keep_b is None else {old: new for new, old in enumerate(keep_b)}
    out = []
    for pair in pairs or []:
        if len(pair) != 2:
            continue
        left, right = pair
        if left in a and right in b:
            out.append([a[left], b[right]])
    return out


def remap_verdicts(pairs, keep: list[int]):
    """Re-index claim verdicts, which are `[statement index, 0 or 1]`.

    Only the first number is an index. Treating both as indices - what `remap`
    does - would read a verdict of 1 as "the statement at position 1".
    """
    new = {old: i for i, old in enumerate(keep)}
    return [[new[p[0]], p[1]] for p in pairs or [] if len(p) == 2 and p[0] in new]


def droppable(texts: list[str], protect: set[int], answer: str, surplus: int) -> set[int] | None:
    """Which entries to remove: never a protected one, and an entry the answer
    mentions only once nothing else is left to drop."""
    answer = (answer or "").lower()
    free = [i for i in range(len(texts)) if i not in protect]
    unmentioned = [i for i in free if str(texts[i]).lower().strip() not in answer]
    mentioned = [i for i in free if i not in unmentioned]
    # Last first: a writer's surplus tends to pile up at the end of the list.
    pick = list(reversed(unmentioned)) + list(reversed(mentioned))
    if len(pick) < surplus:
        return None
    return set(pick[:surplus])


def _in_range(pairs, size: int) -> bool:
    return all(0 <= n < size for pair in pairs for n in pair)


def _trim_list(card, options: list, bounds) -> bool:
    """pick_one, tap_in_place, claim_grid, order: one list, an answer key over it."""
    constraints, wrapped = (None, False)
    if card.constraints:
        constraints, wrapped = unwrap(card.constraints)
        # A key we cannot read, or one pointing outside the list, is not ours to fix.
        if constraints is None or not _in_range(constraints, len(options)):
            return False
    if card.picked is not None and not all(isinstance(i, int) and 0 <= i < len(options) for i in card.picked):
        return False

    protect = set(card.picked or [])
    protect |= {n for pair in (constraints or []) for n in pair}
    drop = droppable(options, protect, card.answer_md, len(options) - bounds[1])
    if drop is None:
        return False

    keep = keep_order(len(options), drop)
    where = {old: new for new, old in enumerate(keep)}
    card.options = [options[i] for i in keep]
    if card.picked is not None:
        card.picked = [where[i] for i in card.picked]
    if constraints is not None:
        card.constraints = rewrap(remap(constraints, keep), wrapped)
    if card.format == "claim_grid" and card.pairs:
        card.pairs = remap_verdicts(card.pairs, keep)
    return True


def _trim_assemble_tokens(card, options: dict, bounds) -> bool:
    """assemble: tokens are an ordering problem, and the pre-filled slots index them."""
    values = options["tokens"]
    constraints, wrapped = unwrap(card.constraints) if card.constraints else (None, False)
    if constraints is None or not _in_range(constraints, len(values)):
        return False
    # A mask that pre-fills a slot names tokens by index and has one entry per
    # token, so dropping a token means choosing which slot disappears. That is a
    # judgement about the line being built, not arithmetic. Refuse.
    fixed = options.get("fixed")
    if isinstance(fixed, list) and any(entry is not None for entry in fixed):
        return False

    protect = {n for pair in constraints for n in pair}
    drop = droppable([str(v) for v in values], protect, card.answer_md, len(values) - bounds[1])
    if drop is None:
        return False
    keep = keep_order(len(values), drop)
    options["tokens"] = [values[i] for i in keep]
    if "fixed" in options:
        options["fixed"] = [None] * len(keep)
    card.constraints = rewrap(remap(constraints, keep), wrapped)
    return True


def _trim_dict(card, options: dict) -> bool:
    primitive = card.format

    def limit(field):
        return archetypes.limit_for(primitive, field)

    if primitive == "assemble":
        bounds = limit("tokens")
        values = options.get("tokens")
        if bounds and isinstance(values, list) and len(values) > bounds[1]:
            return _trim_assemble_tokens(card, options, bounds)
        return False

    # A grid stores its ticked cells as flat indices, row * columns + column. Drop a
    # column and every index changes meaning while staying in range, which the
    # validator cannot see. So the cells are decoded now, the rows and columns that
    # hold one are protected, and the indices are rebuilt from the survivors after.
    grid = primitive == "grid_toggle" and isinstance(options.get("rows"), list) and isinstance(options.get("columns"), list)
    cells: list[tuple[int, int]] = []
    if grid:
        old_rows, old_cols = len(options["rows"]), len(options["columns"])
        picked = card.picked
        if not (isinstance(picked, list) and all(isinstance(i, int) and 0 <= i < old_rows * old_cols for i in picked)):
            return False
        cells = [(i // old_cols, i % old_cols) for i in picked]
    keep_rows = list(range(len(options["rows"]))) if grid else []
    keep_cols = list(range(len(options["columns"]))) if grid else []

    changed = False
    # Columns and rows first: dropping one takes its cells with it, which can
    # bring an item count inside its own limit without touching the items.
    for field in ("columns", "rows", "items", "left", "right"):
        values = options.get(field)
        bounds = limit(field)
        if not isinstance(values, list) or not bounds or len(values) <= bounds[1]:
            continue
        surplus = len(values) - bounds[1]
        pairs = card.pairs or []

        if grid and field == "columns":
            protect = {c for _, c in cells}
        elif grid and field == "rows":
            protect = {r for r, _ in cells}
        elif field in ("columns", "rows"):
            # A column or row that is the only home for something is protected, so
            # the trim cannot empty the card of its own answer.
            axis = 1 if field == "columns" else 0
            used = {pair[axis] for pair in pairs if len(pair) == 2}
            protect = used if len(used) + surplus > len(values) else set()
        else:
            protect = set()

        drop = droppable([str(v) for v in values], protect, card.answer_md, surplus)
        if drop is None:
            continue
        keep = keep_order(len(values), drop)
        options[field] = [values[i] for i in keep]

        if grid and field == "columns":
            keep_cols = keep
        elif grid and field == "rows":
            keep_rows = keep
        elif field in ("left", "right") and isinstance(options.get("left"), list) and isinstance(options.get("right"), list):
            # A match is a bijection. Dropping a term drops the meaning it was
            # paired with, or the card keeps an orphan on the other side and
            # fails a different rule instead of this one.
            partner = {p[0]: p[1] for p in pairs if len(p) == 2}
            if field == "right":
                partner = {b: a for a, b in partner.items()}
            other = "right" if field == "left" else "left"
            other_values = options[other]
            other_keep = keep_order(len(other_values), {partner[i] for i in drop if i in partner})
            options[other] = [other_values[i] for i in other_keep]
            card.pairs = remap(pairs, keep if field == "left" else other_keep, other_keep if field == "left" else keep)
        elif field == "items":
            card.pairs = remap(pairs, keep, keep_order(len(options.get("columns") or []), set()))
        elif field == "columns":
            left_len = len(options.get("items") or options.get("rows") or [])
            card.pairs = remap(pairs, keep_order(left_len, set()), keep)
        changed = True

    if grid and changed:
        new_cols = len(keep_cols)
        row_at = {old: new for new, old in enumerate(keep_rows)}
        col_at = {old: new for new, old in enumerate(keep_cols)}
        card.picked = [row_at[r] * new_cols + col_at[c] for r, c in cells]
    card.options = options
    return changed


def trim(card) -> bool:
    """Bring every over-maximum field inside its limit. True if anything changed."""
    options = card.options
    if isinstance(options, list):
        bounds = archetypes.limit_for(card.format, "options") or archetypes.limit_for(card.format, "tokens")
        if bounds and len(options) > bounds[1]:
            return _trim_list(card, options, bounds)
        return False
    if isinstance(options, dict):
        return _trim_dict(card, options)
    return False


def main() -> None:
    con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"), read_only=not APPLY)
    cols = ["id", "topic_slug", "format", "difficulty", "prompt_md", "options", "answer_md",
            "archetype", "picked", "constraints", "pairs", "value", "tolerance", "why_step", "reject_reason"]
    rows = con.execute(f"""
        select {", ".join(cols)} from cards
         where source = 'lesson' and status = 'rejected'
           and reject_reason like 'not well formed%' and reject_reason like '%above the maximum%'
    """).fetchall()

    print(f"{len(rows)} cards over a maximum")
    fixed, refused, unchanged = [], 0, 0

    for row in rows:
        card = as_card(row, cols)
        before = wellformed.problems(card)
        if not before:
            continue
        if not trim(card):
            unchanged += 1
            continue
        after = wellformed.problems(card)
        if after:
            refused += 1
            continue
        fixed.append(card)

    print(f"  repaired and re-checked clean: {len(fixed)}")
    print(f"  trimmed but still not well formed, discarded: {refused}")
    print(f"  nothing safe to drop: {unchanged}")

    if not APPLY:
        print("\ndry run; pass --apply to write")
        return

    for card in fixed:
        con.execute(
            """update cards set options = ?, picked = ?, constraints = ?, pairs = ?,
                      status = 'draft', kept = true, reject_reason = null,
                      quality = json_merge_patch(coalesce(quality, '{}'),
                                                json_object('repaired_limits', ?))
               where id = ?""",
            [
                json.dumps(card.options) if card.options is not None else None,
                json.dumps(card.picked) if card.picked is not None else None,
                json.dumps(card.constraints) if card.constraints else None,
                json.dumps(card.pairs) if card.pairs else None,
                card.reject_reason,
                card.id,
            ],
        )
    con.commit()
    print(f"\nwrote {len(fixed)} cards back to draft")
    left = con.execute("""select count(*) from cards where source='lesson' and status='rejected'
                           and reject_reason like '%above the maximum%'""").fetchone()[0]
    print(f"still over a maximum: {left}")


if __name__ == "__main__":
    main()
