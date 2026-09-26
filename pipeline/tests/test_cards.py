import pytest
from pydantic import ValidationError

from pipeline.cards import generate, check


def card(**over):
    base = {"format": "typed", "prompt": "Which pattern?", "answer": "Sliding window",
            "key_points": ["contiguous range", "shrink when invalid"], "options": None, "difficulty": "Medium"}
    base.update(over)
    return base


def test_card_rules():
    generate.Card(**card())
    with pytest.raises(ValidationError):
        generate.Card(**card(key_points=["only one"]))            # 2-4 key points
    with pytest.raises(ValidationError):
        generate.Card(**card(format="mcq", options=["a", "b"]))    # mcq needs 4 options
    with pytest.raises(ValidationError):
        generate.Card(**card(format="mcq", options=["a", "b", "c", "d"], answer="e"))  # answer must be an option
    generate.Card(**card(format="mcq", options=["a", "b", "c", "Sliding window"]))


class FakeLLM:
    def __init__(self, reply):
        self.reply, self.calls = reply, []

    def complete_json(self, system, user, schema, tier="fast", purpose=""):
        self.calls.append({"system": system, "user": user, "tier": tier, "purpose": purpose})
        return schema(**self.reply)


def test_problem_prompt_is_grounded_in_the_source():
    llm = FakeLLM({"cards": [card()]})
    problem = {"slug": "min-window", "title": "Minimum Window Substring", "difficulty": "Hard",
               "pattern": "Sliding Window", "statement": "Given s and t...", "solution": "def f(): ..."}
    cards = generate.for_problem(llm, problem, tier="smart")
    assert len(cards) == 1 and cards[0]["problem_slug"] == "min-window"
    call = llm.calls[0]
    assert call["tier"] == "smart" and "Given s and t..." in call["user"] and "def f(): ..." in call["user"]


def test_check_keeps_only_high_scores():
    good = FakeLLM({"correct": 5, "clear": 4, "relevant": 5, "issues": ""})
    bad = FakeLLM({"correct": 3, "clear": 5, "relevant": 5, "issues": "answer is wrong"})
    assert check.review(good, card(), "source")["keep"] is True
    verdict = check.review(bad, card(), "source")
    assert verdict["keep"] is False and verdict["issues"] == "answer is wrong"


def test_dedupe_drops_near_identical_prompts():
    cards = [card(prompt="What is the time complexity of binary search?"),
             card(prompt="What's the time complexity of binary search?"),
             card(prompt="Why does quicksort degrade to O(n^2)?")]
    assert len(check.dedupe(cards)) == 2


def test_skips_non_interview_sections():
    assert generate.is_card_worthy({"title": "Lab Projects", "body": "x" * 2000}) is False
    assert generate.is_card_worthy({"title": "Homework (Simulation)", "body": "x" * 2000}) is False
    assert generate.is_card_worthy({"title": "Preface", "body": "x" * 2000}) is False
    assert generate.is_card_worthy({"title": "Caching › Cache eviction", "body": "x" * 2000}) is True
    assert generate.is_card_worthy({"title": "Caching", "body": "too short"}) is False


def test_reviewer_prompt_allows_standard_knowledge():
    assert "well-established" in check.SYSTEM


class SetReviewer:
    def __init__(self, verdicts):
        self.verdicts, self.calls = verdicts, []

    def complete_json(self, system, user, schema, tier="fast", purpose=""):
        self.calls.append(purpose)
        return schema(verdicts=self.verdicts)


def test_review_set_checks_all_cards_in_one_call():
    cards = [{"format": "typed", "difficulty": "Easy", "prompt": f"Q{i}", "answer": "A", "key_points": ["k"]} for i in range(3)]
    llm = SetReviewer([
        {"index": 0, "correct": 5, "clear": 5, "relevant": 5},
        {"index": 1, "correct": 2, "clear": 5, "relevant": 5, "issues": "wrong"},
    ])
    out = check.review_set(llm, cards, "source text")
    assert llm.calls == ["cards-check"]
    assert [v["keep"] for v in out] == [True, False, False]  # index 2 missing → dropped
    assert out[2]["issues"] == "no verdict"
