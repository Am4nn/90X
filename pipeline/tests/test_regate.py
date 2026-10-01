"""The combined gate pass: answerability + guessability reject on either."""

from dataclasses import dataclass

from pipeline.cards.regate import merge_rejects


@dataclass
class Card:
    prompt: str


def test_a_card_only_the_blind_gate_rejected_is_still_rejected():
    card = Card("which structure?")
    out = merge_rejects([], [(card, "guessable by elimination: 2/3 samples flagged it")])
    assert out == [(card, "guessable by elimination: 2/3 samples flagged it")]


def test_the_answerability_reason_wins_when_both_gates_reject():
    card = Card("which structure?")
    out = merge_rejects([(card, "the marked answer is wrong")], [(card, "guessable")])
    assert len(out) == 1
    assert out[0][1] == "the marked answer is wrong"


def test_value_equal_but_distinct_cards_are_not_deduped():
    # The two gates share the same card objects from `cards_of`, so deduping is
    # by identity, not by value. Two cards that merely read alike are distinct.
    a, b = Card("same prompt"), Card("same prompt")
    out = merge_rejects([(a, "wrong")], [(b, "guessable")])
    assert len(out) == 2
    assert out[0][0] is a and out[1][0] is b
