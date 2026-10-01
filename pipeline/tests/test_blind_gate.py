"""The blind gate: three samples, options only, reject at two or more flags."""

from pipeline.cards import blind_gate
from pipeline.cards.blind_gate import BlindVerdict, Judgement
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
    """Returns a scripted verdict per call and records the user prompts."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.users = []

    def complete_json(self, system, user, schema, tier="smart", purpose="", thinking=False):
        self.users.append(user)
        return self.replies.pop(0)


def test_the_model_sees_options_and_nothing_else():
    card = _pick_one(prompt="Per the lesson on hashing, which structure gives O(1) average lookup?")
    llm = _RecordingLLM([Judgement(guessable=False)] * 3)
    blind_gate.judge_card(llm, card)
    assert len(llm.users) == 3
    for user in llm.users:
        assert "A hash map" in user, "the option the reader sees must be shown"
        assert "which structure gives O(1)" not in user.lower(), "the question must not be shown"
        assert "lesson" not in user.lower(), "the source text must not reach the model"
        assert "hashing" not in user.lower(), "the topic content must not reach the model"


def test_assemble_view_shows_prefilled_slots():
    card = Card.model_validate({
        "format": "assemble", "archetype": "fill-code-blank", "difficulty": "Medium",
        "prompt": "Assemble the SELECT clause.",
        "answer": "SELECT x FROM y WHERE z.", "key_points": ["a", "b"],
        "options": {"tokens": ["SELECT", "FROM", "WHERE"], "fixed": [0, 1, None]},
        "constraints": [[0, 1], [1, 2]],
    })
    shown = blind_gate.view(card)
    assert "SELECT" in shown and "FROM" in shown and "WHERE" in shown
    assert "slot 0 -> token 0" in shown and "slot 1 -> token 1" in shown
    assert "slot 2" not in shown, "a gap slot is not a pre-filled one"


def test_three_samples_are_taken():
    card = _pick_one()
    llm = _RecordingLLM([Judgement(guessable=False), Judgement(guessable=False), Judgement(guessable=False)])
    assert blind_gate.judge_card(llm, card) == 0
    assert len(llm.users) == blind_gate.SAMPLES


def test_reject_at_two_or_more_flags():
    card = _pick_one()
    llm = _RecordingLLM([Judgement(guessable=True), Judgement(guessable=True), Judgement(guessable=False)])
    assert blind_gate.judge_card(llm, card) == 2

    rejected = blind_gate.judge([card], [BlindVerdict(index=0, flags=2)])
    assert len(rejected) == 1
    assert rejected[0][0] is card
    assert rejected[0][1].startswith("guessable")


def test_one_flag_is_not_guessable():
    card = _pick_one()
    rejected = blind_gate.judge([card], [BlindVerdict(index=0, flags=1)])
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
