"""The one-archetype writer: it writes exactly what it is asked, or refuses."""

import pytest
from pydantic import ValidationError

from pipeline.cards import archetypes, write
from pipeline.cards.archetypes import CardSlot
from pipeline.cards.generate import Card, WhyStep

TOPIC = {"name": "Arrays & Hashing", "domain": "dsa", "slug": "arrays-hashing"}
LESSON = "A hash map gives O(1) average lookup by spreading keys across buckets."


class FakeLLM:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def complete_json(self, system, user, schema, tier="smart", purpose=""):
        self.calls.append({"system": system, "user": user, "schema": schema, "tier": tier, "purpose": purpose})
        return self.result


def _draft(**over):
    base = {
        "prompt": "Which structure gives O(1) average lookup?",
        "answer": "A hash map, because keys spread across buckets.",
        "key_points": ["hashing spreads keys", "lookup is average O(1)"],
        "options": ["Linked list", "Hash map", "Sorted array", "Binary tree"],
        "picked": [1],
    }
    base.update(over)
    return base


def test_a_refusal_is_a_valid_return():
    llm = FakeLLM(write.WriteResult(refused="no natural sequence for this topic"))
    slot = CardSlot("sequence", "order", "Medium")
    result = write.write_one(llm, TOPIC, LESSON, slot, tier="smart")
    assert isinstance(result, write.Refusal)
    assert result.reason == "no natural sequence for this topic"


def test_the_pipeline_stamps_format_archetype_and_difficulty():
    llm = FakeLLM(write.WriteResult(draft=write.CardDraft(**_draft())))
    slot = CardSlot("concept", "pick_one", "Easy")
    result = write.write_one(llm, TOPIC, LESSON, slot, tier="smart")
    assert isinstance(result, Card)
    assert result.format == "pick_one", "the pipeline sets format to the primitive, never the archetype"
    assert result.archetype == "concept"
    assert result.difficulty == "Easy"
    assert result.picked == [1], "the draft's answer column survives"
    assert archetypes.shape_of(result.format) is not None


def test_the_writer_is_told_the_archetype_and_primitive():
    llm = FakeLLM(write.WriteResult(refused="nope"))
    slot = CardSlot("complexity", "numeric", "Hard")
    write.write_one(llm, TOPIC, LESSON, slot, hard_material="some problems", tier="smart")
    user = llm.calls[0]["user"]
    assert "Archetype: Complexity (complexity)" in user
    assert "Primitive: numeric" in user
    assert "Target difficulty: Hard" in user
    assert "some problems" in user, "hard material reaches a Hard card"


def test_a_draft_whose_columns_mismatch_its_shape_becomes_a_refusal():
    # A pick_one draft with no `picked` cannot be stamped as a chosen card, so
    # the writer refills rather than saving a malformed card.
    bad = _draft()
    del bad["picked"]
    del bad["options"]
    llm = FakeLLM(write.WriteResult(draft=write.CardDraft(**bad)))
    slot = CardSlot("concept", "pick_one", "Easy")
    result = write.write_one(llm, TOPIC, LESSON, slot, tier="smart")
    assert isinstance(result, write.Refusal)
    assert "malformed" in result.reason


def test_a_chosen_card_without_picked_is_rejected():
    with pytest.raises(ValidationError):
        Card(
            format="pick_one", archetype="concept", difficulty="Easy",
            prompt="Which structure gives O(1) average lookup?",
            answer="A hash map.", key_points=["a", "b"],
            options=["A", "B", "C", "D"],
        )


def test_a_number_card_needs_value_and_tolerance():
    with pytest.raises(ValidationError):
        Card(format="numeric", archetype="estimate", difficulty="Easy",
             prompt="How many bytes?", answer="Roughly 2 GB.", key_points=["a", "b"], value=2e9)
    Card(format="numeric", archetype="estimate", difficulty="Easy",
         prompt="How many bytes?", answer="Roughly 2 GB.", key_points=["a", "b"],
         value=2e9, tolerance=5e8)


def test_an_ordered_card_needs_before_after_pairs():
    with pytest.raises(ValidationError):
        Card(format="order", archetype="sequence", difficulty="Medium",
             prompt="Put these in order.", answer="1, 2.", key_points=["a", "b"],
             constraints=[[0]])  # a lone index is not a [before, after] pair
    Card(format="order", archetype="sequence", difficulty="Medium",
         prompt="Put these in order.", answer="1, 2.", key_points=["a", "b"],
         constraints=[[0, 1]])


def test_a_hard_card_carries_a_why_step():
    card = Card(
        format="pick_one", archetype="concept", difficulty="Hard",
        prompt="Which invariant survives resizing?",
        answer="Load stays bounded.", key_points=["rehash keeps buckets short", "amortised O(1)"],
        options=["A", "B", "C", "D"], picked=[0],
        why_step=WhyStep(options=["rehashing rebalances", "nothing grows", "buckets never change"], correct=0),
    )
    assert card.why_step.correct == 0
