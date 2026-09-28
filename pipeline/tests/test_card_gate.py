"""The card gate. Every case is a draft the first card pass actually shipped."""

from dataclasses import dataclass, field

from pipeline.cards.from_lessons import card_budget
from pipeline.cards.gate import GateResult, Verdict, judge, prompt_only


@dataclass
class FakeCard:
    prompt: str
    answer: str = "an answer"
    format: str = "typed"
    options: list[str] = field(default_factory=list)


def gate(cards, verdicts):
    return judge(cards, GateResult(verdicts=verdicts))


def test_rejects_a_card_that_needs_the_source():
    """The card Aman found: it quotes a solution the reader never sees."""
    card = FakeCard("In the reference solution, after removing the run starting at x up to y-1, "
                    "it sets d[x] = d[y] + y - x. What invariant makes this correct?")
    rejected = gate([card], [Verdict(index=0)])
    assert len(rejected) == 1
    assert "unseen material" in rejected[0][1], rejected
    assert "reference solution" in rejected[0][1]


def test_rejects_what_the_reviewer_calls_unanswerable():
    card = FakeCard("What does the diagram show?")
    rejected = gate([card], [Verdict(index=0, answerable=False, reason="no diagram is present")])
    assert rejected[0][1].startswith("not answerable")


def test_rejects_a_typed_card_that_should_be_multiple_choice():
    """Aman's second example: the honest answer is a list to enumerate."""
    card = FakeCard("Along which dimensions can content negotiation vary the representation of a resource?")
    rejected = gate([card], [Verdict(index=0, fits_format=False, reason="the answer is a list")])
    assert rejected[0][1].startswith("wrong_format")


def test_keeps_a_fair_card():
    card = FakeCard("Why does a sliding window run in O(n) even with a nested loop?")
    assert gate([card], [Verdict(index=0)]) == []


def test_mcq_where_a_competent_answer_disagrees_is_rejected():
    card = FakeCard("Which is true of TCP?", answer="It is connection-oriented", format="mcq",
                    options=["It is connectionless", "It is connection-oriented",
                             "It never retransmits", "It has no ordering guarantee"])
    rejected = gate([card], [Verdict(index=0, picked="It is connectionless")])
    assert "disagrees with the marked option" in rejected[0][1]


def test_mcq_agreement_is_kept():
    card = FakeCard("Which is true of TCP?", answer="It is connection-oriented", format="mcq",
                    options=["It is connectionless", "It is connection-oriented",
                             "It never retransmits", "It has no ordering guarantee"])
    assert gate([card], [Verdict(index=0, picked=" It is connection-oriented ")]) == []


def test_a_card_the_reviewer_never_ruled_on_is_rejected():
    """Keeping it meant a truncated reply silently passed questions nobody
    checked. Rejected is not deleted: it goes through the repair pass and is
    gated again, so an omission costs a retry rather than a card."""
    cards = [FakeCard("Why is TCP reliable?"), FakeCard("Why is UDP fast?")]
    rejected = gate(cards, [Verdict(index=0)])
    assert len(rejected) == 1
    assert rejected[0][0].prompt == "Why is UDP fast?"
    assert "did not rule" in rejected[0][1]


def test_the_gate_never_sees_the_answer():
    card = FakeCard("Why is a hash map O(1) on average?", answer="SECRET-REFERENCE-ANSWER")
    shown = prompt_only(card)
    assert "SECRET-REFERENCE-ANSWER" not in shown
    assert "Why is a hash map O(1) on average?" in shown


def test_mcq_options_are_shown_but_not_which_is_right():
    card = FakeCard("Which is true?", answer="B", format="mcq", options=["A", "B"])
    shown = prompt_only(card)
    assert "A" in shown and "B" in shown
    assert "answer" not in shown.lower()


def test_card_budget_follows_importance():
    assert card_budget(0.5) == 8
    assert card_budget(0.8) == 10
    assert card_budget(1.0) == 12


def test_risk_column_holds_confidence_not_risk():
    """pickReviewSample sorts ascending and reviews the first half, so a LOW
    value is what gets looked at. Inverting the gate's confidence would put
    the cards it liked most in front of the reviewer."""
    from pipeline.cards.rebatch import risk_of

    doubtful = risk_of('{"gate_confidence": 0.3}')
    confident = risk_of('{"gate_confidence": 0.95}')
    assert doubtful < confident, "the doubtful card must sort first"
    assert confident == 0.95

    # Chunk-generated cards keep the old scale: lowest of three 0-5 scores.
    assert risk_of('{"correct": 2, "clear": 5, "relevant": 5}') == 0.4
    assert risk_of(None) is None


def test_lesson_card_ids_are_stable_uuids():
    """public.cards.id is a uuid, so a readable "slug:l0" id never publishes.
    uuid5 keeps regeneration idempotent instead of duplicating every card."""
    import uuid

    from pipeline.cards.run_lessons import CARD_NAMESPACE

    first = uuid.uuid5(CARD_NAMESPACE, "sliding-window:0")
    assert first == uuid.uuid5(CARD_NAMESPACE, "sliding-window:0")
    assert first != uuid.uuid5(CARD_NAMESPACE, "sliding-window:1")
    assert first != uuid.uuid5(CARD_NAMESPACE, "two-pointers:0")
    uuid.UUID(str(first))  # parses as a uuid, which Postgres requires


def test_one_malformed_card_does_not_cost_the_whole_topic():
    """A multiple-choice card with three options used to fail the whole set,
    losing eleven good cards and the topic with it."""
    from pipeline.cards.from_lessons import CardSet

    good = {
        "format": "typed",
        "prompt": "Why does a hash map give O(1) average lookup?",
        "answer": "Keys spread across buckets, so each holds a constant number.",
        "key_points": ["hashing spreads keys", "buckets stay short"],
        "difficulty": "Easy",
    }
    malformed = {**good, "format": "mcq", "answer": "not one of the options", "options": ["x", "y", "z"]}
    kept = CardSet.model_validate({"cards": [good, malformed, good, good]}).cards
    assert len(kept) == 3
    assert all(c.format == "typed" for c in kept)


def test_a_set_of_only_malformed_cards_still_fails():
    import pytest
    from pydantic import ValidationError

    from pipeline.cards.from_lessons import CardSet

    junk = {"format": "mcq", "prompt": "Which?", "answer": "nope", "key_points": ["a", "b"],
            "difficulty": "Easy", "options": ["x"]}
    with pytest.raises(ValidationError):
        CardSet.model_validate({"cards": [junk, junk, junk]})


class _FakeLLM:
    """Returns a scripted reply per purpose, so the repair path can be driven."""

    def __init__(self, replies):
        self.replies = replies
        self.purposes = []

    def complete_json(self, system, user, schema, tier="smart", purpose=""):
        self.purposes.append(purpose)
        return self.replies[purpose]


def _card(prompt, **over):
    from pipeline.cards.generate import Card

    return Card.model_validate({
        "format": "typed", "prompt": prompt, "answer": "An answer that is long enough.",
        "key_points": ["first point", "second point"], "difficulty": "Easy", **over,
    })


def test_a_rejected_card_is_repaired_before_it_is_discarded():
    """The gate says exactly what is wrong, which is usually enough to fix the
    wording. Discarding instead costs ~160 cards across a full run."""
    from pipeline.cards import run_lessons
    from pipeline.cards.from_lessons import CardSet
    from pipeline.cards.gate import GateResult, Verdict

    good = _card("Why is a sliding window linear despite the nested loop?")
    leaky = _card("In the reference solution, why does d[x] work?")
    fixed = _card("Why does memoising by index make the recurrence linear?")

    llm = _FakeLLM({
        "cards-from-lesson": CardSet(cards=[good, leaky, good, good]),
        "card-gate": GateResult(verdicts=[
            Verdict(index=0, confidence=0.9),
            Verdict(index=1, answerable=False, reason="names a solution", confidence=0.2),
            Verdict(index=2, confidence=0.9),
            Verdict(index=3, confidence=0.9),
        ]),
        "cards-rewrite": CardSet(cards=[fixed, fixed, fixed]),
    })
    # The gate is asked again about the repaired cards, and passes them.
    calls = {"n": 0}
    original_review = run_lessons.gate.review

    def review(_llm, topic, cards, tier="review"):
        calls["n"] += 1
        if calls["n"] == 1:
            return llm.replies["card-gate"]
        return GateResult(verdicts=[Verdict(index=i, confidence=0.8) for i in range(len(cards))])

    run_lessons.gate.review = review
    try:
        kept, rejected, sent_back, confidence = run_lessons.one(
            llm, {"name": "Sliding window", "domain": "dsa", "lesson": "A lesson body.", "importance": 1.0}
        )
    finally:
        run_lessons.gate.review = original_review

    assert "cards-rewrite" in llm.purposes, "the rejected card must get a repair pass"
    assert len(kept) == 6, f"3 good plus 3 repaired, got {len(kept)}"
    assert rejected == []
    # What the gate caught is reported separately from what it could not save.
    # Counting only the discards made a run the gate worked hard on look like a
    # 1% rejection rate, which reads as "the gate found almost nothing".
    assert len(sent_back) == 1, f"the gate's first-pass objection must be recorded, got {len(sent_back)}"
    assert all(0 <= c <= 1 for c in confidence.values())


def test_a_card_id_follows_its_question_not_its_position():
    """Keying on position meant the gate changing its mind about one card
    moved every later card's id, so published study history could attach to a
    different question."""
    from pipeline.cards.run_lessons import card_id

    first = card_id("sliding-window", "Why is it O(n) despite the nested loop?")
    assert first == card_id("sliding-window", "Why is it O(n) despite the nested loop?")
    # Reflowed whitespace is the same question.
    assert first == card_id("sliding-window", "  Why is it O(n)   despite the nested loop?\n")
    assert first != card_id("sliding-window", "When does the technique stop working?")
    assert first != card_id("two-pointers", "Why is it O(n) despite the nested loop?")


def test_the_gate_cannot_reject_a_card_for_having_a_valid_format():
    """The real rejection, from the published review pack:

        wrong_format: Format 'output' is not one of the allowed card formats
        (flash, typed, mcq).

    69 output cards were live at the time. The prompt documents `output` and
    the Card enum allows it - the reviewing model invented the restriction. A
    format from our own enum is legal by construction, so an objection that
    only says otherwise is not an objection.
    """
    card = FakeCard("What is the exact output?\n```python\nprint(sorted({3,1,2}))\n```",
                    answer="[1, 2, 3]", format="output")
    verdict = Verdict(index=0, fits_format=False,
                      reason="Format 'output' is not one of the allowed card formats (flash, typed, mcq).")
    assert gate([card], [verdict]) == []


def test_a_real_format_objection_still_rejects():
    """The guard must not swallow the objection it was built to allow."""
    card = FakeCard("What is the exact output?\n```python\nprint(time.time())\n```",
                    answer="1759000000.0", format="output")
    rejected = gate([card], [Verdict(index=0, fits_format=False,
                                     reason="the snippet prints a timestamp, so the output changes")])
    assert "wrong_format" in rejected[0][1]


def test_an_answerable_card_in_the_wrong_format_reports_the_format():
    """The stages are separate so both can be true at once. Collapsing them
    into one enum meant the reviewer had to choose, and the repair pass was
    told whichever it happened to pick."""
    card = FakeCard("Name the four transaction isolation levels.")
    rejected = gate([card], [Verdict(index=0, answerable=True, fits_format=False,
                                     reason="the honest answer is a list to enumerate")])
    assert rejected[0][1].startswith("wrong_format")


def test_the_earliest_failure_is_the_one_reported():
    """A card that needs unseen material is a worse card than one in the wrong
    format, and the repair pass should be told the more fundamental thing."""
    card = FakeCard("In the reference solution, name the four isolation levels.")
    rejected = gate([card], [Verdict(index=0, answerable=False, fits_format=False,
                                     reason="the answer is a list")])
    assert "unseen material" in rejected[0][1]


def test_a_structurally_broken_card_is_caught_without_the_model():
    card = FakeCard("Which isolation level?", answer="Serializable", format="mcq",
                    options=["Read committed", "Serializable"])
    rejected = gate([card], [Verdict(index=0)])
    assert "malformed" in rejected[0][1] and "4 options" in rejected[0][1]


def test_an_output_card_must_show_its_snippet():
    card = FakeCard("What does the loop print?", answer="3", format="output")
    rejected = gate([card], [Verdict(index=0)])
    assert "must show the snippet" in rejected[0][1]


def test_confidence_is_keyed_by_card_not_by_position():
    """The gate returns verdicts keyed by position; a caller holding cards has
    to join the two. Leaving that to callers cost every one of 2,804 cards its
    score: the re-gate looked up `id(card)` in a position-keyed map, missed
    every time, and stored the 0.5 fallback into the column the review screen
    sorts on."""
    from pipeline.cards.gate import confidence_by_card

    cards = [FakeCard("a"), FakeCard("b"), FakeCard("c")]
    result = GateResult(verdicts=[Verdict(index=0, confidence=0.2), Verdict(index=2, confidence=0.9)])
    scores = confidence_by_card(cards, result)
    assert scores[id(cards[0])] == 0.2
    assert scores[id(cards[2])] == 0.9
    # Never ruled on: the fallback, but only for that card.
    assert scores[id(cards[1])] == 0.5


def test_a_gradability_objection_is_never_suppressed():
    """The format-denial guard used to cover the gradable verdict too, so an
    ungradable card stayed publishable whenever the reason mentioned formats."""
    card = FakeCard("What is the exact output?\n```sql\nselect 1;\n```", answer="1", format="output")
    rejected = gate([card], [Verdict(index=0, gradable=False,
                                     reason="no standard plaintext format is valid for a SQL result set")])
    assert "not gradable" in rejected[0][1]


def test_a_real_format_objection_that_mentions_validity_still_rejects():
    """"this format is not valid for exact-match grading" is a genuine
    objection. A looser denial pattern swallowed it."""
    card = FakeCard("What is printed?\n```python\nprint(hash('a'))\n```", answer="x", format="output")
    rejected = gate([card], [Verdict(index=0, fits_format=False,
                                     reason="this format is not valid for exact-match grading here")])
    assert "wrong_format" in rejected[0][1]
