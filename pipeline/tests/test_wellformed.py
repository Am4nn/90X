"""Well-formedness: every primitive, not just pick_one.

Each case here is a card the first full run actually produced and shipped, so a
regression means the same card ships again.
"""

from dataclasses import dataclass, field
from typing import Any

from pipeline.cards import wellformed


@dataclass
class Card:
    format: str = "pick_one"
    archetype: str = "concept"
    difficulty: str = "Medium"
    options: Any = field(default_factory=list)
    picked: Any = None
    constraints: Any = None
    pairs: Any = None
    value: Any = None
    tolerance: Any = None
    why_step: Any = None


def problems(**kwargs) -> list[str]:
    return wellformed.problems(Card(**kwargs))


# --- the cards that shipped broken ------------------------------------------

def test_a_grid_wider_than_three_columns_fails():
    # The 5x7 JVM card: 35 cells against a component that caps at three columns.
    card = Card(
        format="grid_toggle", archetype="complexity-table",
        options={"rows": ["Heap", "Java stack"], "columns": ["a", "b", "c", "d", "e", "f", "g"]},
        picked=[0, 8],
    )
    probs = wellformed.problems(card)
    assert any("columns: 7, above the maximum of 3" in p for p in probs), probs


def test_a_grid_of_five_rows_passes():
    # Height is cheap, width is not: rows 2-5 is deliberately allowed.
    card = Card(
        format="grid_toggle", archetype="complexity-table",
        options={"rows": ["a", "b", "c", "d", "e"], "columns": ["x", "y", "z"]},
        picked=[0, 4, 8, 12],
    )
    assert wellformed.problems(card) == []


def test_a_single_column_grid_fails():
    card = Card(
        format="grid_toggle", archetype="complexity-table",
        options={"rows": ["a", "b", "c"], "columns": ["True"]},
        picked=[0, 2],
    )
    probs = wellformed.problems(card)
    assert any("columns: 1, below the minimum of 2" in p for p in probs), probs


def test_a_snippet_with_two_identical_lines_fails():
    # 22 of these shipped: only one index counts, so tapping the other identical
    # line is marked wrong for no reason the reader can see.
    card = Card(
        format="tap_in_place", archetype="tap-the-bug",
        options=["def f(url):", "    return url", "    log(url)", "    return url"],
        picked=[1],
    )
    probs = wellformed.problems(card)
    assert any("correct line is not unique" in p for p in probs), probs


def test_a_match_reusing_a_right_item_fails():
    # match.tsx clears any pair already using a right item, so no answer the
    # reader can submit is the stored one.
    card = Card(
        format="match", archetype="error-cause-match",
        options={"left": ["a", "b", "c"], "right": ["x", "y", "z"]},
        pairs=[[0, 0], [1, 0], [2, 2]],
    )
    probs = wellformed.problems(card)
    assert any("share one right item" in p for p in probs), probs


def test_cyclic_assemble_constraints_fail():
    # 6 -> 7 -> 2 -> 8 -> ... -> 7: no permutation satisfies it, so the card is
    # wrong however it is answered.
    card = Card(
        format="assemble", archetype="fill-clause",
        options={"tokens": ["a", "b", "c", "d"]},
        constraints=[[0, 1], [1, 2], [2, 1], [1, 3]],
    )
    probs = wellformed.problems(card)
    assert any("cycle" in p for p in probs), probs


def test_assemble_with_two_valid_sentences_fails():
    # The tokens make one sentence. If two arrangements pass, a wrong one passes.
    card = Card(
        format="assemble", archetype="fill-clause",
        options={"tokens": ["a", "b", "c", "d"]},
        constraints=[[0, 1], [2, 3]],
    )
    probs = wellformed.problems(card)
    assert any("more than one way" in p for p in probs), probs


def test_a_fully_chained_assemble_passes():
    card = Card(
        format="assemble", archetype="fill-clause",
        options={"tokens": ["a", "b", "c", "d"]},
        constraints=[[0, 1], [1, 2], [2, 3]],
    )
    assert wellformed.problems(card) == []


def test_order_with_two_valid_orderings_passes():
    # Unlike assemble: `order` stores constraints precisely so that two genuinely
    # interchangeable steps both pass.
    card = Card(
        format="order", archetype="sequence",
        options=["first", "either", "or", "last"],
        constraints={"before": [[0, 1], [0, 2], [1, 3], [2, 3]]},
    )
    assert wellformed.problems(card) == []


def test_a_bucket_of_ten_items_fails():
    card = Card(
        format="bucket", archetype="two-way",
        options={"items": [str(n) for n in range(10)], "columns": ["TCP", "UDP"]},
        pairs=[[n, n % 2] for n in range(10)],
    )
    probs = wellformed.problems(card)
    assert any("items: 10, above the maximum of 8" in p for p in probs), probs


def test_a_claim_grid_where_every_claim_is_true_fails():
    card = Card(
        format="claim_grid", archetype="all-that-apply",
        options=["one", "two", "three", "four"],
        pairs=[[0, 1], [1, 1], [2, 1], [3, 1]],
    )
    probs = wellformed.problems(card)
    assert any("same verdict" in p for p in probs), probs


def test_a_grid_where_every_cell_is_correct_fails():
    card = Card(
        format="grid_toggle", archetype="complexity-table",
        options={"rows": ["a", "b"], "columns": ["x", "y"]},
        picked=[0, 1, 2, 3],
    )
    probs = wellformed.problems(card)
    assert any("every cell is correct" in p for p in probs), probs


# --- the answer contract ----------------------------------------------------

def test_pick_one_with_two_correct_options_fails():
    probs = problems(options=["a", "b", "c", "d"], picked=[0, 1])
    assert any("exactly one correct option" in p for p in probs), probs


def test_picked_out_of_range_fails():
    probs = problems(options=["a", "b", "c", "d"], picked=[9])
    assert any("out of range" in p for p in probs), probs


def test_a_negative_tolerance_fails():
    card = Card(format="numeric", archetype="complexity", value=4.0, tolerance=-1.0, options=None)
    probs = wellformed.problems(card)
    assert any("negative" in p for p in probs), probs


def test_a_numeric_card_without_a_tolerance_fails():
    card = Card(format="numeric", archetype="complexity", value=4.0, options=None)
    probs = wellformed.problems(card)
    assert any("no tolerance" in p for p in probs), probs


def test_a_tolerance_of_zero_passes():
    # Exact match is right for "how many comparisons"; only a missing or negative
    # tolerance is a defect.
    card = Card(format="numeric", archetype="complexity", value=4.0, tolerance=0.0, options=None)
    assert wellformed.problems(card) == []


def test_a_why_step_pointing_past_its_reasons_fails():
    probs = problems(options=["a", "b", "c", "d"], picked=[0], difficulty="Hard",
                     why_step={"options": ["because", "also"], "correct": 5})
    assert any("outside its 2 reasons" in p for p in probs), probs


def test_a_hard_card_without_a_why_step_fails():
    probs = problems(options=["a", "b", "c", "d"], picked=[0], difficulty="Hard")
    assert any("has none" in p for p in probs), probs


def test_a_difficulty_the_archetype_forbids_fails():
    # `flash` is Easy-only in the registry.
    card = Card(format="self_rate", archetype="flash", difficulty="Hard", options=None)
    probs = wellformed.problems(card)
    assert any("outside what flash allows" in p for p in probs), probs


# --- what this module must leave alone --------------------------------------

def test_a_legacy_card_is_not_judged_here():
    # No archetype: the old corpus predates the registry, and claiming it here
    # would reject every typed and mcq card the moment the gate ran.
    card = Card(format="typed", archetype=None, options=[])
    assert wellformed.problems(card) == []


def test_a_clean_pick_one_passes():
    assert problems(options=["a", "b", "c", "d"], picked=[2]) == []


# --- compose: the rubric is the answer definition ---------------------------

def test_a_compose_card_without_a_rubric_fails():
    # `key_points` is what the written answer is marked against, so too few of
    # them means there is nothing to grade.
    card = Card(format="compose", archetype="your-story", options=None)
    card.key_points = ["only one"]
    probs = wellformed.problems(card)
    assert any("keyPoints: 1, below the minimum of 3" in p for p in probs), probs


def test_a_compose_card_with_a_repeated_requirement_fails():
    card = Card(format="compose", archetype="your-story", options=None)
    card.key_points = ["names the result", "names the result", "says what you did"]
    probs = wellformed.problems(card)
    assert any("repeats a requirement" in p for p in probs), probs


def test_a_well_formed_compose_card_passes():
    card = Card(format="compose", archetype="your-story", options=None)
    card.key_points = ["names the situation", "says what you personally did", "states a measurable result"]
    assert wellformed.problems(card) == []
