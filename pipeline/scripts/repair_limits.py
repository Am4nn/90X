"""Bring cards that overshoot a registry limit back inside it, by trimming.

302 cards are rejected as not well formed. Most of those reasons need a writer -
tokens below the minimum cannot be invented, and a claim grid where every claim
is true needs a different claim. But one family is arithmetic: a card that offers
seven options against a maximum of six, four columns against three, six rows
against five. Nothing has to be written to fix those. Something has to go.

What this will not do:

  - Drop an option the answer depends on. `picked` is preserved, and an option
    whose text appears in `answer_md` is kept where there is any alternative, so
    the prose does not end up explaining a choice that is no longer on screen.
  - Guess. Every trim is re-checked with `wellformed.problems`, the same function
    that rejected the card, and written only if it now comes back empty. A trim
    that fixes the count but trips a different rule - a claim grid left with one
    verdict, tokens that now assemble two ways - is discarded, not written.
  - Touch anything below a minimum. Those need content, and this script has none.

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

# field -> (where it lives in `options`, which pair column indexes it)
LIST_FIELDS = {"options": None, "tokens": "tokens", "items": "items", "left": "left", "right": "right",
               "columns": "columns", "rows": "rows"}


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


def trim(card) -> bool:
    """Bring every over-maximum field inside its limit. True if anything changed."""
    primitive = card.format
    options = card.options
    changed = False

    def limit(field):
        return archetypes.limit_for(primitive, field)

    if isinstance(options, list):
        bounds = limit("options") or limit("tokens")
        if bounds and len(options) > bounds[1]:
            protect = set(card.picked or [])
            # An ordered card's constraints name positions it must keep.
            if card.constraints:
                protect |= {i for pair in card.constraints for i in pair}
            drop = droppable(options, protect, card.answer_md, len(options) - bounds[1])
            if drop is None:
                return False
            keep = keep_order(len(options), drop)
            card.options = [options[i] for i in keep]
            if card.picked is not None:
                card.picked = [keep.index(i) for i in card.picked if i in keep]
            if card.constraints:
                card.constraints = remap(card.constraints, keep)
            changed = True

    elif isinstance(options, dict):
        # Columns and rows first: dropping one takes its cells with it, which can
        # bring an item count inside its own limit without touching the items.
        for field in ("columns", "rows", "items", "left", "right", "tokens"):
            values = options.get(field)
            bounds = limit(field)
            if not isinstance(values, list) or not bounds or len(values) <= bounds[1]:
                continue
            surplus = len(values) - bounds[1]
            pairs = card.pairs or []
            # Protect a column or row that is the only home for something, so the
            # trim cannot empty the card of its own answer.
            axis = 1 if field in ("columns",) else 0
            used = {pair[axis] for pair in pairs if len(pair) == 2} if field in ("columns", "rows") else set()
            drop = droppable([str(v) for v in values], used if len(used) + surplus > len(values) else set(),
                             card.answer_md, surplus)
            if drop is None:
                continue
            keep = keep_order(len(values), drop)
            options[field] = [values[i] for i in keep]
            if field in ("left", "right") and isinstance(options.get("left"), list) and isinstance(options.get("right"), list):
                # A match is a bijection. Dropping a term drops the meaning it was
                # paired with, or the card keeps an orphan on the other side and
                # fails a different rule instead of this one.
                partner = {a: b for a, b in ((p[0], p[1]) for p in pairs if len(p) == 2)}
                if field == "right":
                    partner = {b: a for a, b in partner.items()}
                other = "right" if field == "left" else "left"
                other_values = options[other]
                other_drop = {partner[i] for i in drop if i in partner}
                other_keep = keep_order(len(other_values), other_drop)
                options[other] = [other_values[i] for i in other_keep]
                left_keep = keep if field == "left" else other_keep
                right_keep = other_keep if field == "left" else keep
                card.pairs = remap(pairs, left_keep, right_keep)
            elif field in ("items", "rows"):
                card.pairs = remap(pairs, keep, keep_order(len(options.get("columns") or []), set()))
            elif field == "columns":
                left_len = len(options.get("items") or options.get("rows") or [])
                card.pairs = remap(pairs, keep_order(left_len, set()), keep)
            changed = True
        card.options = options

    return changed


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


main()
