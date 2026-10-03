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

    def complete_json(self, system, user, schema, tier="smart", purpose="", thinking=False):
        self.calls.append({"system": system, "user": user, "schema": schema, "tier": tier, "purpose": purpose, "thinking": thinking})
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
             options=["A", "B"], constraints=[[0]])  # a lone index is not a [before, after] pair
    Card(format="order", archetype="sequence", difficulty="Medium",
         prompt="Put these in order.", answer="1, 2.", key_points=["a", "b"],
         options=["A", "B"], constraints=[[0, 1]])


def test_a_hard_card_carries_a_why_step():
    card = Card(
        format="pick_one", archetype="concept", difficulty="Hard",
        prompt="Which invariant survives resizing?",
        answer="Load stays bounded.", key_points=["rehash keeps buckets short", "amortised O(1)"],
        options=["A", "B", "C", "D"], picked=[0],
        why_step=WhyStep(options=["rehashing rebalances", "nothing grows", "buckets never change"], correct=0),
    )
    assert card.why_step.correct == 0


def test_the_lesson_prefix_comes_before_the_per_card_content():
    llm = FakeLLM(write.WriteResult(refused="nope"))
    slot = CardSlot("concept", "pick_one", "Easy")
    write.write_one(llm, TOPIC, LESSON, slot, tier="smart")
    user = llm.calls[0]["user"]
    assert user.index("Lesson:") < user.index("Archetype:"), "the lesson must be the stable prefix"
    assert LESSON in user


def test_the_writer_stamps_per_shape_options():
    draft = write.CardDraft(
        prompt="Match each term to its meaning.",
        answer="Atomicity is all-or-nothing.",
        key_points=["all or nothing", "single unit"],
        options={"left": ["A", "C"], "right": ["Atomicity", "Consistency"]},
        pairs=[[0, 0], [1, 1]],
    )
    llm = FakeLLM(write.WriteResult(draft=draft))
    slot = CardSlot("term-meaning", "match", "Medium")
    result = write.write_one(llm, TOPIC, LESSON, slot, tier="smart")
    assert isinstance(result, Card)
    assert result.options == {"left": ["A", "C"], "right": ["Atomicity", "Consistency"]}
    assert result.pairs == [[0, 0], [1, 1]]


def test_options_that_mismatch_the_shape_become_a_refusal():
    # A match card whose options are a flat list cannot render as left/right, so
    # it is refused rather than stored blank.
    bad = _draft()  # options: list[str], picked: [int] -> pick_one shape
    llm = FakeLLM(write.WriteResult(draft=write.CardDraft(**bad)))
    slot = CardSlot("term-meaning", "match", "Medium")
    result = write.write_one(llm, TOPIC, LESSON, slot, tier="smart")
    assert isinstance(result, write.Refusal)
    assert "malformed" in result.reason


def test_output_guards_reject_pathological_lengths():
    base = dict(prompt="Which structure gives O(1) lookup?", answer="A hash map.",
                key_points=["hashing spreads keys", "buckets stay short"],
                options=["A", "B", "C", "D"], picked=[0])
    with pytest.raises(ValidationError):
        write.CardDraft(**{**base, "answer": "x" * (write.ANSWER_MAX + 1)})
    with pytest.raises(ValidationError):
        write.CardDraft(**{**base, "key_points": ["a", "x" * (write.KEY_POINT_MAX + 1)]})
    with pytest.raises(ValidationError):
        write.CardDraft(**{**base, "options": ["A", "B", "C", "x" * (write.OPTION_MAX + 1)]})
    with pytest.raises(ValidationError):
        write.CardDraft(**{**base, "prompt": "x" * (write.PROMPT_MAX + 1)})


def test_why_step_options_are_length_capped():
    overlong = "x" * (write.OPTION_MAX + 1)
    with pytest.raises(ValidationError):
        write.CardDraft(
            prompt="Which invariant survives resizing?",
            answer="Load stays bounded.",
            key_points=["rehash keeps buckets short", "amortised O(1)"],
            options=["A", "B", "C", "D"], picked=[0],
            why_step=WhyStep(options=["rehashing rebalances", overlong], correct=0),
        )


def test_a_reply_that_never_validates_becomes_a_refusal():
    class _Raising:
        def complete_json(self, *a, **k):
            raise write.LLMError("cards-write: invalid JSON after retry")

    slot = CardSlot("concept", "pick_one", "Easy")
    result = write.write_one(_Raising(), TOPIC, LESSON, slot, tier="smart")
    assert isinstance(result, write.Refusal)
    assert "did not validate" in result.reason


def test_a_budget_failure_still_propagates():
    class _Budget:
        def complete_json(self, *a, **k):
            raise write.BudgetExceeded("cap reached")

    slot = CardSlot("concept", "pick_one", "Easy")
    with pytest.raises(write.BudgetExceeded):
        write.write_one(_Budget(), TOPIC, LESSON, slot, tier="smart")


def test_write_one_passes_thinking_through():
    llm = FakeLLM(write.WriteResult(refused="nope"))
    slot = CardSlot("concept", "pick_one", "Easy")
    write.write_one(llm, TOPIC, LESSON, slot, tier="smart", thinking=True)
    assert llm.calls[0]["thinking"] is True
    write.write_one(llm, TOPIC, LESSON, slot, tier="smart")
    assert llm.calls[1]["thinking"] is False


def test_a_draft_with_leaked_reasoning_is_rejected():
    # The writer's chain of thought must never reach a reader-facing field; a
    # self-correcting answer is the leak the grid-toggle card shipped.
    bad = _draft(answer="The answer is B. Wait, let me re-evaluate: actually A. I need to adjust the indices.")
    with pytest.raises(ValidationError):
        write.CardDraft(**bad)


def test_ordinary_quoted_phrases_are_not_treated_as_leaks():
    # The guard is deliberately narrow: "wait,", "I meant" and "let me check"
    # are ordinary words a valid card can quote, so they must not be rejected.
    ok = _draft(answer="wait, I meant the reader should pick B, but let me check the options")
    assert write.CardDraft(**ok).answer


def test_a_why_step_correct_index_must_name_an_option():
    with pytest.raises(ValidationError):
        WhyStep(options=["a", "b"], correct=2)  # only 0 and 1 exist


def test_order_and_assemble_tell_the_writer_to_shuffle():
    assert "SHUFFLED" in write.PRIMITIVE_INSTRUCTIONS["order"]
    assert "SHUFFLED" in write.PRIMITIVE_INSTRUCTIONS["assemble"]
    # match and bucket leak the same way: the writer lists both sides in the
    # matching order, so the answer is the diagonal.
    assert "SHUFFLED" in write.PRIMITIVE_INSTRUCTIONS["match"]
    assert "SHUFFLED" in write.PRIMITIVE_INSTRUCTIONS["bucket"]


def test_the_writer_is_told_wrong_reasons_must_be_false_about_the_same_item():
    assert "very item, pair, row, or value" in write.SYSTEM


def test_the_writer_is_told_best_and_rank_questions_need_stated_assumptions():
    assert "ONE ANSWER, OR REFUSE" in write.SYSTEM
    assert "unstated assumption" in write.SYSTEM


GRID_OPTIONS = {"rows": ["ArrayList", "HashMap", "CopyOnWriteArrayList", "ConcurrentHashMap"],
                "columns": ["Throws CME", "Never throws", "Snapshot"]}


def test_grid_cells_are_named_by_row_and_column_and_the_code_does_the_arithmetic():
    """The model used to be asked for flat row-major indices and got the multiplication
    wrong in 55 of 109 live grids. A flat index that lands on the wrong cell is just
    another valid index, so nothing caught it. It now names each cell and the pipeline
    computes row * columns + column."""
    cells = [[0, 0], [1, 0], [2, 1], [2, 2], [3, 1]]
    llm = FakeLLM(write.WriteResult(draft=write.CardDraft(**_draft(options=GRID_OPTIONS, picked=None, cells=cells))))
    result = write.write_one(llm, TOPIC, LESSON, CardSlot("complexity-table", "grid_toggle", "Medium"), tier="smart")
    assert isinstance(result, Card), result
    assert result.picked == [0, 3, 7, 8, 10], result.picked


def test_a_grid_that_still_sends_flat_picked_is_not_trusted():
    """If the model ignores the instruction and sends the old flat indices, the card must
    not go through on numbers nobody can check."""
    llm = FakeLLM(write.WriteResult(draft=write.CardDraft(**_draft(options=GRID_OPTIONS, picked=[0, 4, 5, 7]))))
    result = write.write_one(llm, TOPIC, LESSON, CardSlot("complexity-table", "grid_toggle", "Medium"), tier="smart")
    assert isinstance(result, write.Refusal), result


def test_grid_cells_outside_the_grid_are_refused_rather_than_clamped():
    for bad in ([[4, 0]], [[0, 3]], [[-1, 0]], [[0]], [[0, 0, 0]], [["a", "b"]]):
        assert write.grid_picked(GRID_OPTIONS, bad) is None, bad


def test_grid_picked_is_sorted_and_deduplicated():
    assert write.grid_picked(GRID_OPTIONS, [[3, 1], [0, 0], [0, 0]]) == [0, 10]


def test_the_grid_instruction_no_longer_asks_for_flat_indices():
    text = write.PRIMITIVE_INSTRUCTIONS["grid_toggle"]
    assert "row-major" not in text, "the model must not be asked to compute a flat index"
    assert "`cells`" in text and "[row, column]" in text


def test_the_writer_is_told_what_the_archetype_asks_and_what_the_lesson_must_offer():
    """The writer used to be given only the archetype's label. `intent` reached the gate and
    the refile step but never the writer, so for a topic with no natural fit it guessed what
    "Where the data leaks" meant and wrote a Python data-structures quiz; "Interleaving"
    became a single-threaded HashMap lookup. The gate rejected 558 cards as the wrong
    archetype, and rejecting them did nothing about the writer that made them."""
    arch = archetypes.by_id("data-leak-spotter")
    assert arch.intent and arch.requires
    llm = FakeLLM(write.WriteResult(refused="the lesson has no pipeline"))
    write.write_one(llm, TOPIC, LESSON, CardSlot("data-leak-spotter", "claim_grid", "Medium"), tier="smart")
    user = llm.calls[0]["user"]
    assert arch.intent in user, "the writer must be told what the question has to do"
    assert f"ONLY if the lesson {arch.requires}" in user, "and what the lesson must offer before it writes"
    assert "refuse" in user


def test_an_archetype_with_no_precondition_adds_no_such_line():
    arch = archetypes.by_id("concept")
    assert not arch.requires
    llm = FakeLLM(write.WriteResult(refused="x"))
    write.write_one(llm, TOPIC, LESSON, CardSlot("concept", "pick_one", "Easy"), tier="smart")
    assert "ONLY if the lesson" not in llm.calls[0]["user"]
    assert arch.intent in llm.calls[0]["user"]


def test_every_precondition_reads_as_the_end_of_the_sentence_the_writer_is_given():
    """`requires` is spliced after "Write this archetype ONLY if the lesson", so it has to be a
    clause: a verb phrase, lower case, no full stop."""
    for a in archetypes.registry().archetypes:
        if not a.requires:
            continue
        assert a.requires[0].islower(), a.id
        assert not a.requires.endswith("."), a.id
        assert a.intent, f"{a.id} has a precondition but no statement of what the question asks"
