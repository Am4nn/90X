"""A second model checks the lesson for things that are simply not true.

The writer cannot catch its own confident errors - that is what makes them
confident. So a different model, on a different provider where one is
configured, reads the finished lesson and rules on each claim. A `wrong`
verdict sends the lesson back to the writer with the corrections attached;
`oversimplified` does too, because a half-truth repeated in an interview
gets picked apart by the follow-up question.

The reviewer is told to rule on the claim, not on the writing. Style
complaints from a reviewer are how lessons get rewritten forever.
"""

from typing import Literal

from pydantic import BaseModel, Field

SYSTEM = """You are a staff engineer fact-checking an interview-prep lesson. A candidate will repeat these claims in a real interview, so a wrong or half-true statement costs them the offer.

Check every factual claim: definitions, mechanisms, complexities, protocol details, guarantees, and anything stated as always/never. Check the 60-second answer and the follow-up answers with the same care as the body.

Verdicts:
- "wrong": the claim is false, or true only in a case the lesson does not state. Include what is actually true.
- "oversimplified": the claim is directionally right but a competent interviewer would push back on it, or it omits a condition that matters. Include what is missing.
- Do not report style, tone, wording, structure, or things you would have written differently. Only correctness.
- Do not report a claim as wrong because the lesson omits something unrelated. Missing breadth is not an error.

If everything checks out, return an empty list. That is a normal outcome; do not invent problems to look useful."""


class Finding(BaseModel):
    claim: str = Field(min_length=10, description="the sentence or phrase from the lesson")
    verdict: Literal["wrong", "oversimplified"]
    correction: str = Field(min_length=10, description="what is actually true")


class Review(BaseModel):
    findings: list[Finding] = Field(default_factory=list, max_length=12)


def review(llm, topic: dict, body_md: str, tier: str = "review") -> Review:
    user = f"Topic: {topic['name']} ({topic['domain']})\n\nLesson:\n{body_md}"
    if tier not in llm.models:
        tier = "smart"
    return llm.complete_json(SYSTEM, user, Review, tier=tier, purpose="lesson-review")


def blocking(rev: Review) -> list[Finding]:
    """Both verdicts block: a half-truth fails the first follow-up question."""
    return list(rev.findings)


def notes(findings: list[Finding]) -> str:
    return "\n".join(f"- [{f.verdict}] {f.claim}\n  -> {f.correction}" for f in findings)
