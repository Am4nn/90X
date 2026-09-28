from datetime import datetime, timezone

import pytest
from pydantic import BaseModel

from pipeline import llm, staging


class Answer(BaseModel):
    pattern: str
    confidence: float


def utc(*args):
    return datetime(*args, tzinfo=timezone.utc)


def test_off_peak_windows():
    # Peak: weekdays 01:00-04:00 and 06:00-10:00 UTC.
    assert not llm.is_off_peak(utc(2026, 9, 28, 2, 0))   # Monday 02:00
    assert not llm.is_off_peak(utc(2026, 9, 28, 9, 59))  # Monday 09:59
    assert llm.is_off_peak(utc(2026, 9, 28, 4, 0))       # Monday 04:00
    assert llm.is_off_peak(utc(2026, 9, 28, 12, 0))      # Monday noon
    assert llm.is_off_peak(utc(2026, 9, 27, 2, 0))       # Sunday 02:00


def test_cost_halves_off_peak():
    peak = llm.cost_usd("deepseek-flash", 1_000_000, 1_000_000, off_peak=False)
    off = llm.cost_usd("deepseek-flash", 1_000_000, 1_000_000, off_peak=True)
    assert peak == pytest.approx(0.30 + 1.20)
    assert off == pytest.approx(peak / 2)


class FakeUsage:
    def __init__(self):
        self.prompt_tokens, self.completion_tokens = 100, 20


class FakeChoice:
    def __init__(self, content):
        self.message = type("M", (), {"content": content})()


class FakeCompletions:
    def __init__(self, replies):
        self.replies, self.calls = list(replies), []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        reply = self.replies.pop(0)
        return type("R", (), {"choices": [FakeChoice(reply)], "usage": getattr(self, "usage", FakeUsage)()})()


def fake_client(replies):
    completions = FakeCompletions(replies)
    client = type("C", (), {"chat": type("Ch", (), {"completions": completions})()})()
    return client, completions


def test_complete_json_validates_and_logs(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    client, calls = fake_client(['{"pattern": "sliding window", "confidence": 0.9}'])
    ai = llm.LLM(client=client, con=con, models={"fast": "deepseek-flash", "smart": "deepseek-v4-pro"})
    out = ai.complete_json("system", "user", Answer, purpose="test")
    assert out == Answer(pattern="sliding window", confidence=0.9)
    assert calls.calls[0]["response_format"] == {"type": "json_object"}
    row = con.execute("select model, purpose, tokens_in, tokens_out from llm_calls").fetchone()
    assert row == ("deepseek-flash", "test", 100, 20)


def test_complete_json_retries_once_then_fails(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    client, calls = fake_client(["not json", '{"pattern": "dp", "confidence": 0.5}'])
    ai = llm.LLM(client=client, con=con, models={"fast": "deepseek-flash", "smart": "deepseek-v4-pro"})
    assert ai.complete_json("s", "u", Answer).pattern == "dp"
    assert len(calls.calls) == 2

    client, calls = fake_client(["nope", "still nope"])
    ai = llm.LLM(client=client, con=con, models={"fast": "deepseek-flash", "smart": "deepseek-v4-pro"})
    with pytest.raises(llm.LLMError):
        ai.complete_json("s", "u", Answer)


def test_budget_cap_stops_calls(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("insert into llm_calls (model, purpose, tokens_in, tokens_out, cost_usd, off_peak) values ('m', 'p', 1, 1, 5.0, true)")
    client, calls = fake_client(['{"pattern": "dp", "confidence": 0.5}'])
    ai = llm.LLM(client=client, con=con, models={"fast": "deepseek-flash", "smart": "deepseek-v4-pro"}, max_usd=5.0)
    with pytest.raises(llm.BudgetExceeded):
        ai.complete_json("s", "u", Answer)
    assert calls.calls == []  # never reached the API


def test_review_tier_uses_its_own_client(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    main, main_calls = fake_client(['{"pattern": "a", "confidence": 1}'])
    review, review_calls = fake_client(['{"pattern": "b", "confidence": 1}'])
    ai = llm.LLM(client=main, con=con, models={"fast": "deepseek-flash", "smart": "deepseek-v4-pro", "review": "gemini-3.5-flash"},
                 clients={"review": review})
    assert ai.complete_json("s", "u", Answer, tier="review").pattern == "b"
    assert main_calls.calls == [] and review_calls.calls[0]["model"] == "gemini-3.5-flash"


def test_off_peak_discount_is_deepseek_only():
    peak = llm.cost_usd("gemini-3.5-flash", 1_000_000, 1_000_000, off_peak=False)
    assert llm.cost_usd("gemini-3.5-flash", 1_000_000, 1_000_000, off_peak=True) == pytest.approx(peak)


class ThinkingUsage:
    def __init__(self):
        self.prompt_tokens, self.completion_tokens, self.total_tokens = 100, 20, 400


def test_hidden_thinking_tokens_are_billed_as_output(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    client, calls = fake_client(['{"pattern": "dp", "confidence": 0.5}'])
    calls.usage = ThinkingUsage
    ai = llm.LLM(client=client, con=con, models={"fast": "deepseek-flash", "smart": "x", "review": "gemini-3.8-flash"})
    ai.complete_json("s", "u", Answer, tier="review")
    row = con.execute("select tokens_out, tokens_reasoning, cost_usd from llm_calls").fetchone()
    assert row[0] == 20 and row[1] == 280
    assert row[2] == pytest.approx((100 * 0.75 + 300 * 3.75) / 1_000_000)
    assert ai.run_costs["gemini-3.8-flash"][1] == pytest.approx(row[2])


def test_gemini_calls_turn_thinking_off(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    client, calls = fake_client(['{"pattern": "dp", "confidence": 0.5}'] * 2)
    ai = llm.LLM(client=client, con=con, models={"fast": "deepseek-flash", "smart": "x", "review": "gemini-3.8-flash"})
    ai.complete_json("s", "u", Answer, tier="review")
    ai.complete_json("s", "u", Answer, tier="fast")
    assert calls.calls[0]["reasoning_effort"] == "none"
    assert "reasoning_effort" not in calls.calls[1]


def test_one_lock_per_connection(tmp_path):
    """A runner and the LLM must wait on the same lock.

    They used to hold one each over the same DuckDB connection, which is not
    thread-safe, so a worker's select and another worker's cost log were free
    to interleave. The select came back short, `dict(zip(cols, row))` dropped
    the keys it had no values for, and the topic died on `KeyError: 'title'`.
    """
    con = staging.connect(tmp_path / "s.duckdb")
    other = staging.connect(tmp_path / "t.duckdb")
    client, _ = fake_client(['{"pattern": "x", "confidence": 0.1}'])
    ai = llm.LLM(client=client, con=con, models={"fast": "deepseek-flash", "smart": "deepseek-v4-pro"})
    assert llm.lock_for(con) is ai.lock
    assert llm.lock_for(con) is not llm.lock_for(other)
