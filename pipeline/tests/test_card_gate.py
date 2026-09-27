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
    rejected = gate([card], [Verdict(index=0, verdict="answerable")])
    assert len(rejected) == 1
    assert "unseen material" in rejected[0][1], rejected
    assert "reference solution" in rejected[0][1]


def test_rejects_what_the_reviewer_calls_unanswerable():
    card = FakeCard("What does the diagram show?")
    rejected = gate([card], [Verdict(index=0, verdict="needs_context", reason="no diagram is present")])
    assert rejected[0][1].startswith("needs_context")


def test_rejects_a_typed_card_that_should_be_multiple_choice():
    """Aman's second example: the honest answer is a list to enumerate."""
    card = FakeCard("Along which dimensions can content negotiation vary the representation of a resource?")
    rejected = gate([card], [Verdict(index=0, verdict="wrong_format", reason="the answer is a list")])
    assert rejected[0][1].startswith("wrong_format")


def test_keeps_a_fair_card():
    card = FakeCard("Why does a sliding window run in O(n) even with a nested loop?")
    assert gate([card], [Verdict(index=0, verdict="answerable")]) == []


def test_mcq_where_a_competent_answer_disagrees_is_rejected():
    card = FakeCard("Which is true of TCP?", answer="It is connection-oriented", format="mcq",
                    options=["It is connectionless", "It is connection-oriented"])
    rejected = gate([card], [Verdict(index=0, verdict="answerable", picked="It is connectionless")])
    assert "disagrees with the marked option" in rejected[0][1]


def test_mcq_agreement_is_kept():
    card = FakeCard("Which is true of TCP?", answer="It is connection-oriented", format="mcq",
                    options=["It is connectionless", "It is connection-oriented"])
    assert gate([card], [Verdict(index=0, verdict="answerable", picked=" It is connection-oriented ")]) == []


def test_a_card_the_reviewer_skipped_is_kept():
    """A short reply must not silently shrink the batch."""
    cards = [FakeCard("Why is TCP reliable?"), FakeCard("Why is UDP fast?")]
    assert gate(cards, [Verdict(index=0, verdict="answerable")]) == []


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
