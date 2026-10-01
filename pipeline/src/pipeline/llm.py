"""AI calls for the pipeline: any OpenAI-compatible endpoint (DeepSeek by
default), JSON output validated against a pydantic model, cost logged to the
staging database."""

import json
import os
import threading
import time
from datetime import datetime, timezone
from typing import TypeVar

import duckdb
from pydantic import BaseModel, ValidationError

from . import config  # noqa: F401  (loads pipeline/.env)

T = TypeVar("T", bound=BaseModel)

# USD per 1M tokens at peak (input cache miss, output). Off-peak is half.
PRICES = {
    "deepseek-flash": (0.30, 1.20),
    "deepseek-v4-pro": (1.32, 3.96),
    # Google paid tier; thinking tokens bill as output (ai.google.dev/gemini-api/docs/pricing).
    "gemini-3.5-flash": (1.50, 9.00),
    "gemini-3.8-flash": (0.75, 3.75),
    "gemini-3.5-flash-lite": (0.30, 2.50),
}
DEFAULT_PRICE = (1.0, 5.0)  # unknown model: count it conservatively

# DeepSeek thinks by default and bills the reasoning tokens as output. Most
# pipeline steps turn it off (a JSON verdict or a card does not need it), but
# the repair pass leaves it on so the model can diagnose *why* a card failed.
# Thinking is therefore a per-call choice, not a global switch — see
# `.planning/feed-v2/DECISIONS.md` (Model tiers and thinking). This mirrors
# web/src/lib/ai.ts NO_THINKING ({ deepseek: { thinking: { type: "disabled" } } }
# through the AI SDK's providerOptions); the OpenAI SDK puts the same body field
# under `extra_body`, where the `deepseek` namespace is already implied by the
# endpoint.
NO_THINKING = {"thinking": {"type": "disabled"}}

# DeepSeek peak hours, UTC, Monday-Friday.
PEAK_WINDOWS = ((1, 4), (6, 10))


# One lock per connection, shared by everything that touches it.
#
# A DuckDB connection is not thread-safe, and the lock belongs to the
# connection rather than to whoever happens to be using it. A worker pool
# holding its own lock while LLM held a second one over the same connection
# left the two of them free to interleave: a select's rows came back short,
# `dict(zip(cols, row))` quietly dropped the missing keys, and the topic died
# on `KeyError: 'title'` - twice in 274, never in the same place.
#
# Reentrant, so a caller that already holds it and reaches code that takes it
# again stalls nothing. A 40-minute run deadlocking on its own lock is a worse
# outcome than a nested acquire nobody notices.
_LOCKS: dict[int, threading.RLock] = {}
_LOCKS_GUARD = threading.Lock()


def lock_for(con: duckdb.DuckDBPyConnection) -> threading.RLock:
    with _LOCKS_GUARD:
        return _LOCKS.setdefault(id(con), threading.RLock())


class LLMError(RuntimeError):
    pass


class BudgetExceeded(LLMError):
    pass


# Hard stop for the whole pipeline's AI spend (override with PIPELINE_MAX_USD).
DEFAULT_MAX_USD = 20.0


def is_off_peak(now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    if now.weekday() >= 5:
        return True
    return not any(start <= now.hour < end for start, end in PEAK_WINDOWS)


def wait_for_off_peak(poll_seconds: int = 300) -> None:
    while not is_off_peak():
        print("Peak hours: waiting for DeepSeek off-peak pricing...", flush=True)
        time.sleep(poll_seconds)


def cost_usd(model: str, tokens_in: int, tokens_out: int, off_peak: bool) -> float:
    price_in, price_out = PRICES.get(model, DEFAULT_PRICE)
    cost = (tokens_in * price_in + tokens_out * price_out) / 1_000_000
    # Only DeepSeek has the off-peak discount.
    return cost / 2 if off_peak and model.startswith("deepseek") else cost


# Without these the SDK waits 600s per attempt and retries twice, so one
# stalled request blocks a whole run for half an hour. A consistency run lost
# 28 minutes to a single hung call that never returned.
REQUEST_TIMEOUT = 120.0
MAX_RETRIES = 2


def _default_client():
    from openai import OpenAI

    return OpenAI(api_key=os.environ["AI_API_KEY"], base_url=os.environ.get("AI_BASE_URL") or None,
                  timeout=REQUEST_TIMEOUT, max_retries=MAX_RETRIES)


def _review_client():
    """Optional independent reviewer on a different provider (REVIEW_* env)."""
    if not os.environ.get("REVIEW_API_KEY"):
        return None
    from openai import OpenAI

    return OpenAI(api_key=os.environ["REVIEW_API_KEY"], base_url=os.environ.get("REVIEW_BASE_URL") or None,
                  timeout=REQUEST_TIMEOUT, max_retries=MAX_RETRIES)


class LLM:
    def __init__(self, con: duckdb.DuckDBPyConnection, client=None, models: dict | None = None,
                 max_usd: float | None = None, clients: dict | None = None,
                 run_id: str | None = None):
        self.con = con
        # Which run this instance's calls belong to. None is the ad-hoc/legacy
        # case: the spend cap then covers the whole table, as it always has. A
        # named run (e.g. the Feed v2 full run) scopes the cap to its own rows.
        self.run_id = run_id
        self.max_usd = max_usd if max_usd is not None else float(os.environ.get("PIPELINE_MAX_USD", DEFAULT_MAX_USD))
        self.client = client or _default_client()
        # DuckDB connections aren't thread-safe; calls may run in a thread pool.
        # The lock is the connection's, so a runner that also reads it in
        # workers waits on the same one rather than on a lock of its own.
        self.lock = lock_for(con)
        # This process's calls per model: {model: [calls, cost_usd]}, for live progress lines.
        self.run_costs: dict[str, list] = {}
        # Calls started but not yet charged, so the cap accounts for them.
        self.in_flight = 0
        self.typical_call_usd = 0.02
        self.models = models or {"fast": os.environ["AI_MODEL_FAST"], "smart": os.environ["AI_MODEL_SMART"]}
        # Per-tier clients; tiers without one use the main client.
        self.clients = dict(clients or {})
        if models is None and os.environ.get("REVIEW_MODEL"):
            self.models["review"] = os.environ["REVIEW_MODEL"]
            if "review" not in self.clients and (review := _review_client()):
                self.clients["review"] = review

    def complete_json(self, system: str, user: str, schema: type[T], tier: str = "fast", purpose: str = "",
                      thinking: bool = False) -> T:
        """Ask for JSON matching `schema`. Retries once with the validation
        error; raises LLMError if the second answer is also invalid.

        `thinking` turns DeepSeek's reasoning on for this one call (off by
        default). Only the repair pass sets it on — diagnosing *why* a card
        failed wants the model to think; classification and generation do not.
        """
        with self.lock:
            spent = spend_usd(self.con, self.run_id)
            in_flight = self.in_flight
            self.in_flight += 1
        try:
            # Every worker reads the same total before any of them records a
            # cost, so with 14 in flight the cap could be passed by a dozen
            # calls. Charging the calls already running against it closes most
            # of that gap without pretending to know their exact cost.
            if spent + in_flight * self.typical_call_usd >= self.max_usd:
                raise BudgetExceeded(f"AI spend ${spent:.2f} plus {in_flight} in flight reached the ${self.max_usd:.2f} cap")
            return self._complete_json(system, user, schema, tier, purpose, thinking)
        finally:
            with self.lock:
                self.in_flight -= 1

    def _complete_json(self, system: str, user: str, schema: type[T], tier: str = "fast", purpose: str = "",
                       thinking: bool = False) -> T:
        model = self.models[tier]
        system_full = (
            f"{system}\n\nReply with a single JSON object matching this JSON Schema, and nothing else:\n"
            f"{json.dumps(schema.model_json_schema())}"
        )
        messages = [{"role": "system", "content": system_full}, {"role": "user", "content": user}]
        last_error = ""
        for attempt in range(2):
            if attempt:
                messages.append({"role": "user", "content": f"That reply was invalid ({last_error}). Reply again with valid JSON only."})
            client = self.clients.get(tier, self.client)
            # Gemini thinks by default and bills it; a JSON verdict doesn't need
            # it, so reasoning_effort is always none for Gemini. DeepSeek's
            # thinking is per-call: off unless `thinking` is set (the repair pass).
            extra = {"reasoning_effort": "none"} if model.startswith("gemini") else {}
            extra_body = NO_THINKING if model.startswith("deepseek") and not thinking else None
            response = client.chat.completions.create(
                model=model, messages=messages, response_format={"type": "json_object"}, temperature=0.2,
                extra_body=extra_body, **extra,
            )
            self._log(model, purpose, response.usage)
            content = response.choices[0].message.content or ""
            try:
                return schema.model_validate_json(content)
            except ValidationError as e:
                last_error = str(e).splitlines()[0][:300]
                messages.append({"role": "assistant", "content": content})
        raise LLMError(f"{purpose or 'llm'}: invalid JSON after retry: {last_error}")

    def _log(self, model: str, purpose: str, usage) -> None:
        tokens_in = getattr(usage, "prompt_tokens", 0) or 0
        tokens_out = getattr(usage, "completion_tokens", 0) or 0
        # OpenAI-compatible endpoints may leave thinking out of completion_tokens
        # but still bill it; whatever total_tokens has beyond in + out is thinking.
        total = getattr(usage, "total_tokens", 0) or 0
        tokens_reasoning = max(0, total - tokens_in - tokens_out)
        off_peak = is_off_peak()
        with self.lock:
            self._insert(model, purpose, tokens_in, tokens_out, off_peak, tokens_reasoning)

    def _insert(self, model, purpose, tokens_in, tokens_out, off_peak, tokens_reasoning=0) -> None:
        cost = cost_usd(model, tokens_in, tokens_out + tokens_reasoning, off_peak)
        self.con.execute(
            """insert into llm_calls (model, purpose, tokens_in, tokens_out, tokens_reasoning, cost_usd, off_peak, run_id)
               values (?, ?, ?, ?, ?, ?, ?, ?)""",
            [model, purpose, tokens_in, tokens_out, tokens_reasoning, cost, off_peak, self.run_id],
        )
        entry = self.run_costs.setdefault(model, [0, 0.0])
        entry[0] += 1
        entry[1] += cost


def spend_usd(con: duckdb.DuckDBPyConnection, run_id: str | None = None) -> float:
    """Total logged AI spend in USD.

    With `run_id` set, only that run's rows count — the per-run cap relies on
    this. With `run_id` None (the legacy behaviour) the whole table counts, so
    ad-hoc invocations and progress lines that diff `spend_usd(con)` before and
    after a step keep working unchanged."""
    if run_id is None:
        return con.execute("select coalesce(sum(cost_usd), 0) from llm_calls").fetchone()[0]
    return con.execute(
        "select coalesce(sum(cost_usd), 0) from llm_calls where run_id = ?", [run_id]
    ).fetchone()[0]
