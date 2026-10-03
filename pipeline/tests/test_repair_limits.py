"""`scripts/repair_limits.py`: a trim must carry the answer key with it, or refuse.

The validator (`wellformed.problems`) checks that a key is well formed, not that it
still points at the same content, so each case here asserts the thing it cannot:
that what the answer key names *before* the trim is what it names *after*.
"""

import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "repair_limits.py"


def load(path: Path | None = None):
    spec = importlib.util.spec_from_file_location("repair_limits_under_test", path or SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The script resolves the repo-relative `src` path at import; tests run from pipeline/.
os.chdir(Path(__file__).resolve().parents[1])
rl = load(Path(os.environ["REPAIR_LIMITS_UNDER_TEST"]) if os.environ.get("REPAIR_LIMITS_UNDER_TEST") else None)


def card(**kw):
    base = dict(id="x", format="pick_one", archetype=None, difficulty="Medium", answer_md="",
                options=None, picked=None, constraints=None, pairs=None, value=None,
                tolerance=None, why_step=None)
    base.update(kw)
    return SimpleNamespace(**base)


def test_wrapped_ordering_constraints_survive_a_trim():
    """The database stores `{"before": [...]}`; the writer produces a flat list. The
    first version iterated the wrapper as if it were the list, got the string
    "before" for a pair, and silently produced no constraints at all."""
    steps = [f"step {n}" for n in range(7)]
    # Item 0 is unconstrained and unmentioned, so it is the one to go.
    before = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
    c = card(format="order", options=list(steps), constraints={"before": before}, answer_md="steps 1 to 6")

    assert rl.trim(c) is True
    assert isinstance(c.constraints, dict), "the wrapper must be preserved"
    assert c.constraints["before"], "constraints must not be emptied"
    named = [(c.options[a], c.options[b]) for a, b in c.constraints["before"]]
    assert named == [(steps[a], steps[b]) for a, b in before], named


def test_a_malformed_constraint_key_is_left_alone_not_guessed_at():
    c = card(format="order", options=[f"s{n}" for n in range(7)], constraints={"before": "nonsense"})
    assert rl.trim(c) is False
    assert len(c.options) == 7, "nothing may be dropped when the key cannot be read"


def test_a_grid_column_holding_a_tick_is_never_dropped():
    """Flat indices are row * columns + column. Drop a column and every index stays
    in range while pointing at a different cell, which the validator accepts. This is
    what put a card with a wrong answer key into production."""
    rows, cols = ["r0", "r1"], ["c0", "c1", "c2", "c3"]
    ticked = {("r0", "c0"), ("r0", "c3"), ("r1", "c3")}
    picked = [rows.index(r) * len(cols) + cols.index(k) for r, k in ticked]
    c = card(format="grid_toggle", options={"rows": list(rows), "columns": list(cols)}, picked=sorted(picked))

    assert rl.trim(c) is True
    new_rows, new_cols = c.options["rows"], c.options["columns"]
    assert len(new_cols) == 3
    now = {(new_rows[i // len(new_cols)], new_cols[i % len(new_cols)]) for i in c.picked}
    assert now == ticked, f"the answer key moved: {now} != {ticked}"


def test_a_grid_with_a_tick_in_every_column_is_refused():
    cols = ["c0", "c1", "c2", "c3"]
    c = card(format="grid_toggle", options={"rows": ["r0", "r1"], "columns": list(cols)}, picked=[0, 1, 2, 3])
    assert rl.trim(c) is False
    assert c.options["columns"] == cols, "no column may be dropped when each holds a tick"


def test_dropping_a_trailing_grid_row_leaves_the_key_reading_the_same():
    """Not every grid trim is dangerous: a trailing row does not move any index."""
    rows, cols = [f"r{n}" for n in range(6)], ["c0", "c1"]
    ticked = {("r0", "c0"), ("r2", "c1")}
    picked = sorted(rows.index(r) * 2 + cols.index(k) for r, k in ticked)
    c = card(format="grid_toggle", options={"rows": list(rows), "columns": list(cols)}, picked=picked)
    assert rl.trim(c) is True
    assert {(c.options["rows"][i // 2], c.options["columns"][i % 2]) for i in c.picked} == ticked


def test_assemble_trim_keeps_constraints_pointing_at_the_same_tokens():
    tokens = [f"tok{n:02d}" for n in range(14)]
    # Tokens 0 and 1 are unconstrained and unmentioned; 2..13 form the line.
    before = [[n, n + 1] for n in range(2, 13)]
    c = card(format="assemble", options={"tokens": list(tokens), "fixed": [None] * 14},
             constraints={"before": before}, answer_md="")

    assert rl.trim(c) is True
    kept = c.options["tokens"]
    assert len(kept) == 12
    assert isinstance(c.constraints, dict)
    named = [(kept[a], kept[b]) for a, b in c.constraints["before"]]
    assert named == [(tokens[a], tokens[b]) for a, b in before], "constraints now name different tokens"
    assert len(c.options["fixed"]) == len(kept), "the mask must keep one entry per token"


def test_assemble_with_a_prefilled_slot_is_refused():
    """The mask names tokens by index, one entry per token. Which slot disappears when
    a token goes is a judgement about the line, not arithmetic."""
    tokens = [f"tok{n:02d}" for n in range(14)]
    fixed = [None] * 14
    fixed[3] = 3
    c = card(format="assemble", options={"tokens": list(tokens), "fixed": fixed},
             constraints={"before": [[n, n + 1] for n in range(2, 13)]})
    assert rl.trim(c) is False
    assert len(c.options["tokens"]) == 14


def test_claim_verdicts_are_reindexed_without_reading_a_verdict_as_an_index():
    """Verdicts are `[statement index, 0 or 1]`. Only the first is an index."""
    statements = [f"claim {w}" for w in ("zero", "one", "two", "three", "four")]
    pairs = [[0, 1], [1, 0], [2, 1], [3, 0], [4, 1]]
    c = card(format="claim_grid", options=list(statements), pairs=[list(p) for p in pairs],
             answer_md="claim four claim three claim two claim one")

    assert rl.trim(c) is True
    assert "claim zero" not in c.options, "the unmentioned statement should be the one dropped"
    said = {c.options[i]: v for i, v in c.pairs}
    assert said == {statements[i]: v for i, v in pairs if i != 0}, said
