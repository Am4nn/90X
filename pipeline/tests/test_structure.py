"""The free structural rules: elimination by shape is caught before any model."""

from dataclasses import dataclass, field

from pipeline.cards import structure


@dataclass
class Card:
    options: list[str] = field(default_factory=list)


def test_a_sole_of_kind_number_fails():
    card = Card([
        "It keeps buckets short by rehashing",
        "Lookup is O(1) on average",
        "Collisions are handled by chaining",
        "42",
    ])
    probs = structure.problems(card)
    assert any("only bare number" in p for p in probs), probs


def test_a_sole_of_kind_code_block_fails():
    card = Card([
        "It keeps buckets short by rehashing",
        "Lookup is O(1) on average",
        "Collisions are handled by chaining",
        "```python\nprint(1)\n```",
    ])
    probs = structure.problems(card)
    assert any("code" in p for p in probs), probs


def test_an_out_of_band_length_option_fails():
    card = Card([
        "O(1)",
        "O(n)",
        "O(log n)",
        "Amortised constant time, because rehashing doubles the table and moves every element once",
    ])
    probs = structure.problems(card)
    assert any("far longer" in p or "far shorter" in p for p in probs), probs


def test_an_all_of_the_above_option_fails():
    card = Card([
        "It is connection-oriented",
        "It retransmits lost segments",
        "It guarantees ordering",
        "All of the above",
    ])
    probs = structure.problems(card)
    assert any("All of the above" in p for p in probs), probs


def test_a_none_of_the_above_option_fails():
    card = Card(["Only one of these is real", "Another false lead", "None of the above", "A fourth"])
    probs = structure.problems(card)
    assert any("None of the above" in p for p in probs), probs


def test_a_clean_set_passes():
    card = Card([
        "It keeps buckets short by rehashing",
        "Lookup is O(1) on average",
        "Collisions are handled by chaining",
        "It degrades toward O(n) at high load factor",
    ])
    assert structure.problems(card) == []


def test_a_card_without_options_is_not_checked():
    assert structure.problems(Card([])) == []
