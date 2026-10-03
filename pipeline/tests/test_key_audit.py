"""The answer-key audit: a key rendered as sentences a reviewer can compare with prose.

A grid stores flat cell indices, an order stores rules, an assemble stores constraints
over tokens. None of those can be compared with a paragraph, which is why a key that
contradicted its explanation shipped. These pin the rendering, because a wrong
rendering would make the audit confidently wrong.
"""

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from pipeline.cards import key_audit as ka


def card(**kw):
    base = dict(format="pick_one", prompt="Q?", options=None, answer="An explanation.", picked=None,
                constraints=None, pairs=None, value=None, tolerance=None, why_step=None, key_points=[])
    base.update(kw)
    return SimpleNamespace(**base)


def test_a_grid_key_is_decoded_cell_by_cell_with_the_right_stride():
    """Flat indices are row * columns + column. Decoding with the wrong stride is exactly
    how a wrong key hides, so this is the case that has to be right."""
    c = card(format="grid_toggle",
             options={"rows": ["Class inheritance", "Interface inheritance", "Composition"],
                      "columns": ["Is-a", "Inherits implementation", "Runtime replaceable"]},
             picked=[0, 1, 3, 6, 8])
    assert ka.key_text(c) == [
        "Class inheritance: ticked Is-a, Inherits implementation",
        "Interface inheritance: ticked Is-a",
        "Composition: ticked Is-a, Runtime replaceable",
    ]


def test_a_grid_row_with_no_tick_says_so_rather_than_vanishing():
    c = card(format="grid_toggle", options={"rows": ["a", "b"], "columns": ["x", "y"]}, picked=[0])
    assert ka.key_text(c) == ["a: ticked x", "b: ticked nothing"]


def test_a_grid_cell_outside_the_grid_is_reported_unreadable_not_dropped():
    c = card(format="grid_toggle", options={"rows": ["a", "b"], "columns": ["x", "y"]}, picked=[9])
    assert ka.key_text(c) == ["The stored answer key could not be read."]


def test_pick_one_names_the_option_not_its_position():
    c = card(options=["Atomicity", "Durability", "Isolation", "Consistency"], picked=[0])
    assert ka.key_text(c) == ["Marked correct: Atomicity"]


def test_the_why_step_key_is_included_as_text():
    c = card(options=["a", "b", "c", "d"], picked=[1],
             why_step={"options": ["wrong reason", "right reason"], "correct": 1})
    assert ka.key_text(c) == ["Marked correct: b", "Reason marked correct (second question): right reason"]


def test_an_order_is_rendered_as_its_rules_because_it_has_no_single_sequence():
    c = card(format="order", options=["execute", "log", "ack"], constraints={"before": [[0, 1], [1, 2]]})
    assert ka.key_text(c) == ["'execute' must come before 'log'", "'log' must come before 'ack'"]


def test_an_assemble_is_rendered_as_the_line_it_builds():
    c = card(format="assemble",
             options={"tokens": ["a", "String", "is", "an", "object"], "fixed": [None] * 5},
             constraints={"before": [[1, 2], [2, 3], [3, 4], [0, 1]]})
    assert ka.key_text(c) == ["The line built is: a String is an object"]


def test_an_assemble_whose_line_is_not_fixed_is_unreadable_not_guessed():
    c = card(format="assemble", options={"tokens": ["a", "b", "c"], "fixed": [None] * 3},
             constraints={"before": [[0, 1]]})
    assert ka.key_text(c) == ["The stored answer key could not be read."]


def test_match_bucket_and_claim_grid_render_their_pairs():
    m = card(format="match", options={"left": ["301", "404"], "right": ["Not found", "Moved"]}, pairs=[[0, 1], [1, 0]])
    assert ka.key_text(m) == ["301 -> Moved", "404 -> Not found"]
    b = card(format="bucket", options={"items": ["DNS", "SSH"], "columns": ["UDP", "TCP"]}, pairs=[[0, 0], [1, 1]])
    assert ka.key_text(b) == ["DNS -> UDP", "SSH -> TCP"]
    g = card(format="claim_grid", options=["s0", "s1"], pairs=[[0, 1], [1, 0]])
    assert ka.key_text(g) == ["TRUE: s0", "FALSE: s1"]


def test_numeric_shows_the_value_and_its_tolerance():
    assert ka.key_text(card(format="numeric", value=4.17, tolerance=0.05)) == ["Expected value: 4.17 (accepted within 0.05)"]
    assert ka.key_text(card(format="numeric", value=8, tolerance=0)) == ["Expected value: 8"]


def test_primitives_without_a_stored_key_have_nothing_to_audit():
    assert ka.key_text(card(format="self_rate")) is None
    assert ka.key_text(card(format="compose")) is None


def test_a_missing_verdict_is_a_schema_error_so_it_gets_retried():
    """An omitted verdict must not read as agreement."""
    with pytest.raises(ValidationError):
        ka.KeyVerdict.model_validate_json('{"index": 0}')


def test_only_a_contradiction_is_reported_silence_and_doubt_are_not():
    cards = [card(), card(), card()]
    result = ka.KeyAudit(verdicts=[
        ka.KeyVerdict(index=0, verdict="agrees"),
        ka.KeyVerdict(index=1, verdict="unclear", reason="the explanation is silent"),
        ka.KeyVerdict(index=2, verdict="contradicts", reason="ticks X but the explanation says no"),
    ])
    assert ka.contradictions(cards, result) == {2: "ticks X but the explanation says no"}


def test_the_auditor_sees_the_options_the_key_and_the_explanation_together():
    c = card(options=["Atomicity", "Durability", "Isolation", "Consistency"], picked=[1],
             answer="Atomicity is all-or-nothing.")
    seen = ka.prompt_for(c)
    assert "option: Atomicity" in seen
    assert "Marked correct: Durability" in seen
    assert "Atomicity is all-or-nothing." in seen


def test_a_grid_with_nothing_ticked_or_nothing_to_tick_is_unreadable_not_plausible():
    """"row: ticked nothing" for every row reads as a key that contradicts nothing, so an
    auditor would happily agree with it. The writer already refuses an empty result; a stored
    one must not be treated as a key either."""
    unreadable = ["The stored answer key could not be read."]
    assert ka.key_text(card(format="grid_toggle", options={"rows": ["a", "b"], "columns": ["x"]}, picked=[])) == unreadable
    assert ka.key_text(card(format="grid_toggle", options={"rows": ["a"], "columns": []}, picked=[])) == unreadable
    assert ka.key_text(card(format="grid_toggle", options={"rows": [], "columns": ["x"]}, picked=[0])) == unreadable


def test_a_tap_the_line_key_says_the_line_is_the_answer_not_that_it_is_good_code():
    """Re-reading flagged cards by hand showed 'Marked correct: lock.lock();' on a card whose
    explanation says that line is the bug. The auditor read 'correct' as 'correct code' and
    reported a contradiction where the key and explanation agreed exactly. For a tap card
    the line IS the answer, so the key has to say so."""
    c = card(format="tap_in_place", options=["a = 1", "lock.lock();", "return a"], picked=[1])
    (line,) = ka.key_text(c)
    assert "lock.lock();" in line
    assert "the answer itself" in line
    assert "Marked correct" not in line
    # Other chosen shapes keep the plain wording.
    assert ka.key_text(card(options=["x", "y"], picked=[1])) == ["Marked correct: y"]


def test_the_auditor_is_told_the_three_misreadings_that_produced_false_flags():
    text = ka.SYSTEM
    assert "IS the answer" in text, "a tapped line is the answer, not an endorsement"
    assert "single spaces" in text and "Ignore spacing" in text, "token spacing is the renderer's, not the card's"
    assert "exponent" in text, "a number may be an exponent the explanation writes as O(n^2)"
    assert 'say "unclear"' in text, "doubt must not become a contradiction"
