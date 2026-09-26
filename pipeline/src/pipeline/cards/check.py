"""Second AI pass: score each card against its source and drop weak ones;
remove near-duplicate prompts."""

import re

from pydantic import BaseModel, Field
from rapidfuzz import fuzz

SYSTEM = """You review interview-prep flashcards against their source material.
Score 1-5:
- correct: the answer and every key point are right and supported by the source.
- clear: the prompt is unambiguous and answerable in 1-3 sentences.
- relevant: an interviewer would plausibly ask this.
List concrete issues in one sentence, or leave empty."""

KEEP_MIN = 4


class Verdict(BaseModel):
    correct: int = Field(ge=1, le=5)
    clear: int = Field(ge=1, le=5)
    relevant: int = Field(ge=1, le=5)
    issues: str = ""


def review(llm, card: dict, source: str, tier: str = "smart") -> dict:
    user = (
        f"Source:\n{source[:5000]}\n\nCard ({card['format']}, {card['difficulty']}):\n"
        f"Prompt: {card['prompt']}\nOptions: {card.get('options')}\nAnswer: {card['answer']}\n"
        f"Key points: {card['key_points']}"
    )
    v = llm.complete_json(SYSTEM, user, Verdict, tier=tier, purpose="cards-check")
    return {**v.model_dump(), "keep": min(v.correct, v.clear, v.relevant) >= KEEP_MIN}


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", text.lower().replace("what's", "what is"))


def dedupe(cards: list[dict], threshold: int = 90) -> list[dict]:
    kept: list[dict] = []
    for c in cards:
        if all(fuzz.token_sort_ratio(_norm(c["prompt"]), _norm(k["prompt"])) < threshold for k in kept):
            kept.append(c)
    return kept
