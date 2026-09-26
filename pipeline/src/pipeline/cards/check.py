"""Second AI pass: score each card against its source and drop weak ones;
remove near-duplicate prompts."""

import re

from pydantic import BaseModel, Field
from rapidfuzz import fuzz

SYSTEM = """You review interview-prep flashcards against their source material.
Score 1-5:
- correct: the answer and every key point are right. Anything specific to the source (its numbers, names,
  design choices) must match the source; well-established general knowledge (e.g. objects live on the heap)
  is allowed even if the passage doesn't state it. Anything wrong or invented scores 1-2.
- clear: the prompt is unambiguous and answerable in 1-3 sentences.
- relevant: an interviewer would plausibly ask this.
List concrete issues in one sentence, or leave empty."""

KEEP_MIN = 4


class Verdict(BaseModel):
    correct: int = Field(ge=1, le=5)
    clear: int = Field(ge=1, le=5)
    relevant: int = Field(ge=1, le=5)
    issues: str = ""


def review(llm, card: dict, source: str, tier: str = "review") -> dict:
    user = (
        f"Source:\n{source[:5000]}\n\nCard ({card['format']}, {card['difficulty']}):\n"
        f"Prompt: {card['prompt']}\nOptions: {card.get('options')}\nAnswer: {card['answer']}\n"
        f"Key points: {card['key_points']}"
    )
    v = llm.complete_json(SYSTEM, user, Verdict, tier=tier, purpose="cards-check")
    return {**v.model_dump(), "keep": min(v.correct, v.clear, v.relevant) >= KEEP_MIN}


class IndexedVerdict(Verdict):
    index: int = Field(ge=0)


class SetVerdict(BaseModel):
    verdicts: list[IndexedVerdict]


def review_set(llm, cards: list[dict], source: str, tier: str = "review") -> list[dict]:
    """Review all cards from one source in a single call (the source is sent
    once). A card with no verdict is dropped."""
    listing = "\n\n".join(
        f"[{i}] ({c['format']}, {c['difficulty']})\nPrompt: {c['prompt']}\nOptions: {c.get('options')}\n"
        f"Answer: {c['answer']}\nKey points: {c['key_points']}"
        for i, c in enumerate(cards)
    )
    user = f"Source:\n{source[:5000]}\n\nCards:\n{listing}\n\nReturn one verdict per card, with its index."
    result = llm.complete_json(SYSTEM, user, SetVerdict, tier=tier, purpose="cards-check")
    by_index = {v.index: v for v in result.verdicts}
    out = []
    for i in range(len(cards)):
        v = by_index.get(i)
        if v is None:
            out.append({"correct": 1, "clear": 1, "relevant": 1, "issues": "no verdict", "keep": False})
        else:
            d = v.model_dump(exclude={"index"})
            out.append({**d, "keep": min(v.correct, v.clear, v.relevant) >= KEEP_MIN})
    return out


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", text.lower().replace("what's", "what is"))


def dedupe(cards: list[dict], threshold: int = 90) -> list[dict]:
    kept: list[dict] = []
    for c in cards:
        if all(fuzz.token_sort_ratio(_norm(c["prompt"]), _norm(k["prompt"])) < threshold for k in kept):
            kept.append(c)
    return kept
