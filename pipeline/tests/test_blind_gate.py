"""The blind gate: three samples, options only, reject at two or more correct."""

from pipeline.cards import blind_gate
from pipeline.cards.blind_gate import BlindVerdict, Guess
from pipeline.cards.generate import Card


def _pick_one(**over):
    base = {
        "format": "pick_one",
        "archetype": "concept",
        "difficulty": "Easy",
        "prompt": "Which structure gives O(1) average lookup?",
        "answer": "A hash map, because keys spread across buckets.",
        "key_points": ["hashing spreads keys", "lookup is average O(1)"],
        "options": ["A linked list", "A hash map", "A sorted array", "A binary tree"],
        "picked": [1],
    }
    base.update(over)
    return Card.model_validate(base)


class _RecordingLLM:
    """Returns a scripted guess per call and records the user prompts."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.users = []

    def complete_json(self, system, user, schema, tier="smart", purpose=""):
        self.users.append(user)
        return self.replies.pop(0)


def test_the_model_sees_options_and_nothing_else():
    card = _pick_one(prompt="Per the lesson on hashing, which structure gives O(1) average lookup?")
    llm = _RecordingLLM([Guess(picked=[1])] * 3)
    blind_gate.judge_card(llm, card)
    assert len(llm.users) == 3
    for user in llm.users:
        assert "A hash map" in user, "the option the reader sees must be shown"
        assert "which structure gives O(1)" not in user.lower(), "the question must not be shown"
        assert "lesson" not in user.lower(), "the source text must not reach the model"
        assert "hashing" not in user.lower(), "the topic content must not reach the model"


def test_three_samples_are_taken():
    card = _pick_one()
    llm = _RecordingLLM([Guess(picked=[0]), Guess(picked=[0]), Guess(picked=[0])])
    assert blind_gate.judge_card(llm, card) == 0
    assert len(llm.users) == blind_gate.SAMPLES


def test_reject_at_two_or_more_correct():
    card = _pick_one()
    llm = _RecordingLLM([Guess(picked=[1]), Guess(picked=[1]), Guess(picked=[0])])
    assert blind_gate.judge_card(llm, card) == 2

    rejected = blind_gate.judge([card], [BlindVerdict(index=0, correct=2)])
    assert len(rejected) == 1
    assert rejected[0][0] is card
    assert rejected[0][1].startswith("guessable")


def test_one_correct_sample_is_not_guessable():
    card = _pick_one()
    rejected = blind_gate.judge([card], [BlindVerdict(index=0, correct=1)])
    assert rejected == []


def test_a_failed_sample_is_not_evidence():
    class _Failing:
        def complete_json(self, *args, **kwargs):
            raise blind_gate.LLMError("provider error")

    card = _pick_one()
    assert blind_gate.judge_card(_Failing(), card) == 0


def test_a_self_rate_card_is_not_judged():
    card = Card.model_validate({
        "format": "self_rate", "archetype": "flash", "difficulty": "Easy",
        "prompt": "Idempotency", "answer": "Repeating an operation has no further effect.",
        "key_points": ["same result", "no side effect"],
    })
    assert blind_gate.shape(card) is None
    assert blind_gate.judge_card(_RecordingLLM([]), card) == 0


def test_an_ordered_card_is_correct_only_when_constraints_hold():
    card = Card.model_validate({
        "format": "order", "archetype": "sequence", "difficulty": "Medium",
        "prompt": "Put these in order: 1. A  2. B  3. C",
        "answer": "A, then B, then C.", "key_points": ["a", "b"],
        "constraints": [[0, 1], [1, 2]],
    })
    assert blind_gate.correct(card, Guess(order=[0, 1, 2]))
    assert not blind_gate.correct(card, Guess(order=[2, 1, 0]))
    assert not blind_gate.correct(card, Guess(order=[0, 1]))  # not a full permutation


def test_a_number_card_checks_tolerance():
    card = Card.model_validate({
        "format": "numeric", "archetype": "estimate", "difficulty": "Easy",
        "prompt": "How many bytes in 2 GB?", "answer": "2 * 2^30 bytes.", "key_points": ["a", "b"],
        "value": 2_147_483_648, "tolerance": 0,
    })
    assert blind_gate.correct(card, Guess(value=2_147_483_648))
    assert not blind_gate.correct(card, Guess(value=1_000_000_000))


def test_a_mapping_card_checks_pairs():
    card = Card.model_validate({
        "format": "match", "archetype": "term-meaning", "difficulty": "Medium",
        "prompt": "Match A, C, I, D to their meanings.",
        "answer": "A is Atomicity.", "key_points": ["a", "b"],
        "pairs": [[0, 2], [1, 0], [2, 1], [3, 3]],
    })
    assert blind_gate.correct(card, Guess(pairs=[[0, 2], [1, 0], [2, 1], [3, 3]]))
    assert not blind_gate.correct(card, Guess(pairs=[[0, 0], [1, 1], [2, 2], [3, 3]]))
