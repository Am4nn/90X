"""Well-formedness, free: can a reader answer this card at all?

`structure.py` asks whether a pick-one card gives itself away by shape, and it
returns early for every other format. Nothing checked the other nine primitives,
so the first full run shipped 112 cards a reader cannot answer correctly:

  * a 5x7 grid (35 cells) against a component that caps at three columns,
  * 22 snippets holding two identical lines where only one index counts, so a
    reader who taps the other identical line is marked wrong,
  * five match cards whose stored answer reuses a right-hand item, which the
    match screen cannot express - no reachable answer is correct,
  * one ordering whose constraints contain a cycle, so no permutation passes.

Every one of those is decidable in code, with no model and no cost. This module
is that decision. It runs beside the gate, and a card it rejects goes to the
repair pass like any other rejection.

The item-count limits live in `archetypes.json` (`limits`), not here, because the
3x3 cap spent the whole first run as a comment in a component while the pipeline
wrote 5x7. One file, both sides.
"""

from __future__ import annotations

from . import archetypes

# A verdict column in a claim grid is a yes/no, so the right-hand index of every
# pair is one of exactly two values.
_VERDICTS = (0, 1)


def _pairs(value) -> list[list[int]] | None:
    """`constraints` arrives flat from the writer and wrapped as
    `{"before": [...]}` from the database. Accept both, reject anything else."""
    if isinstance(value, dict):
        value = value.get("before")
    if not isinstance(value, (list, tuple)):
        return None
    out: list[list[int]] = []
    for item in value:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            return None
        if not all(isinstance(n, int) and not isinstance(n, bool) for n in item):
            return None
        out.append([int(item[0]), int(item[1])])
    return out


def _indices(value) -> list[int] | None:
    if not isinstance(value, (list, tuple)) or not value:
        return None
    if not all(isinstance(n, int) and not isinstance(n, bool) for n in value):
        return None
    return [int(n) for n in value]


def _texts(value) -> list[str] | None:
    if not isinstance(value, (list, tuple)) or not value:
        return None
    if not all(isinstance(s, str) and s.strip() for s in value):
        return None
    return [s for s in value]


def _duplicates(items: list[str]) -> list[str]:
    seen: set[str] = set()
    dupes: list[str] = []
    for item in items:
        key = item.strip()
        if key in seen and key not in dupes:
            dupes.append(key)
        seen.add(key)
    return dupes


def _within(primitive: str, field: str, count: int) -> str | None:
    limit = archetypes.limit_for(primitive, field)
    if limit is None:
        return None
    low, high = limit
    if count < low:
        return f"{field}: {count}, below the minimum of {low}"
    if count > high:
        return f"{field}: {count}, above the maximum of {high}"
    return None


def _orderings(count: int, before: list[list[int]]) -> tuple[bool, bool]:
    """`(satisfiable, unique)` for `count` items under these `before` pairs.

    Kahn's algorithm. A cycle leaves nodes with a permanent in-degree, and a card
    whose constraints cycle is marked wrong however the reader answers. The
    ordering is unique when exactly one node is ready at every step: that is what
    a sentence needs, while a list of steps may legitimately have two orders.
    """
    outgoing: dict[int, list[int]] = {i: [] for i in range(count)}
    indegree = dict.fromkeys(range(count), 0)
    for first, second in before:
        outgoing[first].append(second)
        indegree[second] += 1
    ready = [i for i, d in indegree.items() if d == 0]
    seen, unique = 0, True
    while ready:
        if len(ready) > 1:
            unique = False
        node = ready.pop()
        seen += 1
        for nxt in outgoing[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
    return seen == count, unique


def _chosen(primitive: str, card, size: int) -> list[str]:
    picked = _indices(getattr(card, "picked", None))
    if picked is None:
        return ["picked is not a non-empty list of integers"]
    found = []
    if len(set(picked)) != len(picked):
        found.append("picked names the same index twice")
    out = [n for n in picked if not 0 <= n < size]
    if out:
        found.append(f"picked is out of range: {out} with {size} choices")
    if primitive == "pick_one" and len(picked) != 1:
        found.append(f"pick_one must have exactly one correct option, not {len(picked)}")
    if primitive == "grid_toggle" and len(picked) == size:
        found.append("every cell is correct, so ticking all of them scores full marks")
    return found


def _ordered(primitive: str, card, count: int) -> list[str]:
    before = _pairs(getattr(card, "constraints", None))
    if not before:
        return ["constraints are missing or malformed"]
    out = sorted({n for pair in before for n in pair if not 0 <= n < count})
    if out:
        return [f"a constraint names index {out} with {count} items"]
    satisfiable, unique = _orderings(count, before)
    if not satisfiable:
        return ["the constraints contain a cycle, so no ordering can be correct"]
    # `order` stores constraints rather than one blessed sequence precisely so
    # that two genuinely interchangeable steps both pass, so a partial order is
    # correct there. `assemble` builds one sentence: if its tokens can be put
    # together two ways, a wrong sentence is marked right.
    if primitive == "assemble" and not unique:
        return ["the tokens can be assembled more than one way, so a wrong sentence would pass"]
    return []


def _mapping(primitive: str, card, options) -> list[str]:
    pairs = _pairs(getattr(card, "pairs", None))
    if not pairs:
        return ["pairs are missing or malformed"]
    lefts = [pair[0] for pair in pairs]
    rights = [pair[1] for pair in pairs]
    found = []

    if primitive == "match":
        left = _texts(options.get("left")) if isinstance(options, dict) else None
        right = _texts(options.get("right")) if isinstance(options, dict) else None
        if left is None or right is None:
            return ["options must be {left: [...], right: [...]} of non-empty strings"]
        if sorted(lefts) != list(range(len(left))):
            found.append(f"pairs must map each of the {len(left)} left items exactly once, got {sorted(lefts)}")
        if any(not 0 <= n < len(right) for n in rights):
            found.append(f"a pair names a right item out of range with {len(right)} on the right")
        elif len(set(rights)) != len(rights):
            # match.tsx clears any pair already using a right item, so a reader
            # physically cannot submit the same right twice: unanswerable.
            found.append("two left items share one right item, which the match screen cannot express")
    elif primitive == "bucket":
        items = _texts(options.get("items")) if isinstance(options, dict) else None
        columns = _texts(options.get("columns")) if isinstance(options, dict) else None
        if items is None or columns is None:
            return ["options must be {items: [...], columns: [...]} of non-empty strings"]
        if sorted(lefts) != list(range(len(items))):
            found.append(f"pairs must place each of the {len(items)} items exactly once, got {sorted(lefts)}")
        if any(not 0 <= n < len(columns) for n in rights):
            found.append(f"a pair names a bucket out of range with {len(columns)} buckets")
        elif len(set(rights)) == 1 and len(columns) > 1:
            found.append("every item belongs to one bucket, so putting them all there scores full marks")
    elif primitive == "claim_grid":
        claims = _texts(options) if isinstance(options, list) else None
        if claims is None:
            return ["options must be a non-empty list of claim strings"]
        if sorted(lefts) != list(range(len(claims))):
            found.append(f"pairs must judge each of the {len(claims)} claims exactly once, got {sorted(lefts)}")
        if any(n not in _VERDICTS for n in rights):
            found.append(f"a verdict is not 0 or 1: {sorted(set(rights))}")
        elif len(set(rights)) == 1:
            found.append("every claim has the same verdict, so one guess scores full marks")
    return found


def _why_step(card, archetype, difficulty: str) -> list[str]:
    why = getattr(card, "why_step", None)
    if why is not None and not isinstance(why, dict):
        why = getattr(why, "model_dump", lambda: None)()
    if why is None:
        if difficulty == "Hard" and archetype is not None and archetype.why_step:
            return ["a Hard card of an archetype that takes a why-step has none"]
        return []
    options = _texts(why.get("options"))
    correct = why.get("correct")
    if options is None or len(options) < 2:
        return ["the why-step needs at least two reasons"]
    if not isinstance(correct, int) or isinstance(correct, bool) or not 0 <= correct < len(options):
        return [f"the why-step's correct index {correct!r} is outside its {len(options)} reasons"]
    dupes = _duplicates(options)
    if dupes:
        return [f"the why-step repeats a reason: {dupes[0]!r}"]
    return []


def problems(card) -> list[str]:
    """Every reason this card cannot be answered correctly. Empty means it can.

    `card` is anything carrying the writer's fields: `format`, `archetype`,
    `difficulty`, `options`, `picked`, `constraints`, `pairs`, `value`,
    `tolerance`, `why_step`. The database row and `write.Card` both qualify.
    """
    archetype_id = getattr(card, "archetype", None)
    if not archetype_id:
        # A legacy card (`typed`, `mcq`, `output`, `bug`) predates the registry
        # and has no archetype. It is not this module's business: `structure.py`
        # is what judges those, and claiming them here would reject the whole old
        # corpus the moment the gate ran over it.
        return []
    primitive = getattr(card, "format", None)
    if not isinstance(primitive, str):
        return ["format is missing"]
    shape = archetypes.shape_of(primitive)
    options_shape = archetypes.options_shape_of(primitive)
    if options_shape is None:
        return [f"{primitive} is not a primitive in the registry"]

    options = getattr(card, "options", None)
    difficulty = getattr(card, "difficulty", "") or ""
    archetype = next((a for a in archetypes.registry().archetypes if a.id == archetype_id), None)

    found: list[str] = []
    if archetype is None:
        found.append(f"archetype {archetype_id!r} is not in the registry")
    else:
        if primitive not in archetype.primitives:
            found.append(f"{primitive} is not a primitive of archetype {archetype.id}")
        if difficulty not in archetype.difficulties:
            found.append(f"difficulty {difficulty!r} is outside what {archetype.id} allows")

    # --- how many items, and are any of them the same thing twice -----------
    size = 0
    if options_shape == "list":
        texts = _texts(options)
        if texts is None:
            return found + ["options must be a non-empty list of non-empty strings"]
        size = len(texts)
        if message := _within(primitive, "options", size):
            found.append(message)
        if dupes := _duplicates(texts):
            # Two identical options make two indices equally correct while only
            # one is stored, so a reader who picks the other one is marked wrong.
            #
            # Except in a snippet: real code has two `}` lines, and that is only
            # unfair when the *answer* is one of the repeated lines. Two identical
            # lines that are both wrong leave the correct line unambiguous.
            if primitive == "tap_in_place":
                picked = _indices(getattr(card, "picked", None)) or []
                answers = {texts[n].strip() for n in picked if 0 <= n < size}
                dupes = [d for d in dupes if d in answers]
                if dupes:
                    found.append(f"the correct line is not unique: {dupes[0]!r} appears twice")
            else:
                found.append(f"two options are the same text: {dupes[0]!r}")
    elif options_shape == "grid":
        rows = _texts(options.get("rows")) if isinstance(options, dict) else None
        columns = _texts(options.get("columns")) if isinstance(options, dict) else None
        if rows is None or columns is None:
            return found + ["options must be {rows: [...], columns: [...]} of non-empty strings"]
        size = len(rows) * len(columns)
        found += [m for m in (_within(primitive, "rows", len(rows)), _within(primitive, "columns", len(columns))) if m]
        for field, items in (("row", rows), ("column", columns)):
            if dupes := _duplicates(items):
                found.append(f"two {field} labels are the same text: {dupes[0]!r}")
    elif options_shape == "assemble":
        tokens = _texts(options.get("tokens")) if isinstance(options, dict) else None
        if tokens is None:
            return found + ["options must be {tokens: [...]} of non-empty strings"]
        size = len(tokens)
        if message := _within(primitive, "tokens", size):
            found.append(message)
        if dupes := _duplicates(tokens):
            # The constraints address tokens by index, so a repeated token makes
            # the intended sequence ambiguous and often unsatisfiable.
            found.append(f"two tokens are the same text: {dupes[0]!r}")
    elif options_shape == "match":
        for field in ("left", "right"):
            items = _texts(options.get(field)) if isinstance(options, dict) else None
            if items is None:
                continue
            if message := _within(primitive, field, len(items)):
                found.append(message)
            if dupes := _duplicates(items):
                found.append(f"two {field} items are the same text: {dupes[0]!r}")
    elif options_shape == "bucket":
        for field in ("items", "columns"):
            items = _texts(options.get(field)) if isinstance(options, dict) else None
            if items is None:
                continue
            if message := _within(primitive, field, len(items)):
                found.append(message)
            if dupes := _duplicates(items):
                found.append(f"two {field} are the same text: {dupes[0]!r}")
    elif options_shape == "none" and options not in (None, [], {}):
        found.append(f"{primitive} stores no options, but options are set")

    # --- is the stored answer one a reader could actually give --------------
    if shape == "chosen":
        found += _chosen(primitive, card, size)
    elif shape == "ordered":
        if size:
            found += _ordered(primitive, card, size)
    elif shape == "mapping":
        found += _mapping(primitive, card, options)
    elif shape == "number":
        value, tolerance = getattr(card, "value", None), getattr(card, "tolerance", None)
        if value is None:
            found.append("a numeric card has no expected value")
        if tolerance is None:
            found.append("a numeric card has no tolerance")
        elif tolerance < 0:
            found.append(f"tolerance {tolerance} is negative, so no answer can be correct")
    elif shape is None:
        for field in ("picked", "constraints", "pairs", "value"):
            if getattr(card, field, None) is not None:
                found.append(f"{primitive} stores no answer shape but carries {field}")
        if primitive == "compose":
            # `key_points` is the rubric a written answer is marked against, not a
            # summary, so a compose card with too few of them cannot be graded.
            points = _texts(getattr(card, "key_points", None))
            if points is None:
                found.append("a compose card needs key_points as its rubric")
            else:
                if message := _within(primitive, "keyPoints", len(points)):
                    found.append(message)
                if dupes := _duplicates(points):
                    found.append(f"the rubric repeats a requirement: {dupes[0]!r}")

    found += _why_step(card, archetype, difficulty)
    return found
