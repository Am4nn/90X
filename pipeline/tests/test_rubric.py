"""The difficulty rubric: each DECISIONS round-3 row scores to its difficulty."""

import pytest

from pipeline.cards.rubric import Properties, score


def test_easy_row():
    p = Properties(
        reasoning_steps=1, constraint_changes_answer="no", spans_facts=False,
        misconception_distractors=False, needs_calculation="no",
    )
    assert score(p) == "Easy"


def test_medium_row():
    p = Properties(
        reasoning_steps=2, constraint_changes_answer="sometimes", spans_facts=False,
        misconception_distractors=True, needs_calculation="maybe",
    )
    assert score(p) == "Medium"


def test_hard_row():
    p = Properties(
        reasoning_steps=3, constraint_changes_answer="yes", spans_facts=True,
        misconception_distractors=True, needs_calculation="yes",
    )
    assert score(p) == "Hard"


def test_the_hardest_dimension_wins():
    # Only two reasoning steps, but it needs a calculation and spans facts:
    # both are Hard rows, so the card is Hard.
    p = Properties(
        reasoning_steps=2, constraint_changes_answer="no", spans_facts=True,
        misconception_distractors=False, needs_calculation="yes",
    )
    assert score(p) == "Hard"


def test_three_plus_reasoning_steps_is_hard_alone():
    p = Properties(
        reasoning_steps=3, constraint_changes_answer="no", spans_facts=False,
        misconception_distractors=False, needs_calculation="no",
    )
    assert score(p) == "Hard"


def test_invalid_properties_are_rejected():
    with pytest.raises(ValueError):
        Properties(
            reasoning_steps=0, constraint_changes_answer="no", spans_facts=False,
            misconception_distractors=False, needs_calculation="no",
        )
    with pytest.raises(ValueError):
        Properties(
            reasoning_steps=1, constraint_changes_answer="maybe", spans_facts=False,
            misconception_distractors=False, needs_calculation="no",
        )
    with pytest.raises(ValueError):
        Properties(
            reasoning_steps=1, constraint_changes_answer="no", spans_facts=False,
            misconception_distractors=False, needs_calculation="rarely",
        )
