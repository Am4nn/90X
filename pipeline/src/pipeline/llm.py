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
}
DEFAULT_PRICE = (1.0, 5.0)  # unknown model: count it conservatively

# DeepSeek peak hours, UTC, Monday-Friday.
PEAK_WINDOWS = ((1, 4), (6, 10))


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
    return cost / 2 if off_peak else cost


def _default_client():
    from openai import OpenAI

    return OpenAI(api_key=os.environ["AI_API_KEY"], base_url=os.environ.get("AI_BASE_URL") or None)


def _review_client():
    """Optional independent reviewer on a different provider (REVIEW_* env)."""
    if not os.environ.get("REVIEW_API_KEY"):
        return None
    from openai import OpenAI

    return OpenAI(api_key=os.environ["REVIEW_API_KEY"], base_url=os.environ.get("REVIEW_BASE_URL") or None)


class LLM:
    def __init__(self, con: duckdb.DuckDBPyConnection, client=None, models: dict | None = None,
                 max_usd: float | None = None, clients: dict | None = None):
        self.con = con
        self.max_usd = max_usd if max_usd is not None else float(os.environ.get("PIPELINE_MAX_USD", DEFAULT_MAX_USD))
        self.client = client or _default_client()
        # DuckDB connections aren't thread-safe; calls may run in a thread pool.
        self.lock = threading.Lock()
        self.models = models or {"fast": os.environ["AI_MODEL_FAST"], "smart": os.environ["AI_MODEL_SMART"]}
        # Per-tier clients; tiers without one use the main client.
        self.clients = dict(clients or {})
        if models is None and os.environ.get("REVIEW_MODEL"):
            self.models["review"] = os.environ["REVIEW_MODEL"]
            if "review" not in self.clients and (review := _review_client()):
                self.clients["review"] = review

    def complete_json(self, system: str, user: str, schema: type[T], tier: str = "fast", purpose: str = "") -> T:
        """Ask for JSON matching `schema`. Retries once with the validation
        error; raises LLMError if the second answer is also invalid."""
        with self.lock:
            spent = spend_usd(self.con)
        if spent >= self.max_usd:
            raise BudgetExceeded(f"AI spend ${spent:.2f} reached the ${self.max_usd:.2f} cap")
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
            response = client.chat.completions.create(
                model=model, messages=messages, response_format={"type": "json_object"}, temperature=0.2,
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
        off_peak = is_off_peak()
        with self.lock:
            self._insert(model, purpose, tokens_in, tokens_out, off_peak)

    def _insert(self, model, purpose, tokens_in, tokens_out, off_peak) -> None:
        self.con.execute(
            "insert into llm_calls (model, purpose, tokens_in, tokens_out, cost_usd, off_peak) values (?, ?, ?, ?, ?, ?)",
            [model, purpose, tokens_in, tokens_out, cost_usd(model, tokens_in, tokens_out, off_peak), off_peak],
        )


def spend_usd(con: duckdb.DuckDBPyConnection) -> float:
    return con.execute("select coalesce(sum(cost_usd), 0) from llm_calls").fetchone()[0]
