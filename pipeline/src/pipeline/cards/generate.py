"""Generate feed cards grounded in one source: a problem or a document
section. Every card tests one concept, has 2-4 key points for grading, and
must be something an interviewer would plausibly ask."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

RULES = """Rules for every card:
- Test exactly one concept an interviewer would plausibly ask about. No trivia, no questions about the text itself ("according to the passage...").
- Everything in the answer must be supported by the source given. Don't invent facts.
- prompt: a question a candidate can answer in 1-3 sentences (typed/flash) or by picking an option (mcq).
- answer: the reference answer, 1-3 sentences.
- key_points: 2-4 short, independently checkable points a good answer must contain. They are used to grade typed answers.
- mcq: exactly 4 options, plausible distractors, `answer` must equal one option exactly.
- output: a short code snippet in the prompt (fenced), answer = exact output.
- difficulty: Easy, Medium or Hard for an interview candidate.
Write in plain, direct English."""


class Card(BaseModel):
    format: Literal["typed", "flash", "mcq", "output"]
    prompt: str = Field(min_length=10)
    answer: str = Field(min_length=1)
    key_points: list[str] = Field(min_length=2, max_length=4)
    options: list[str] | None = None
    difficulty: Literal["Easy", "Medium", "Hard"]

    @model_validator(mode="after")
    def _mcq(self):
        if self.format == "mcq":
            if not self.options or len(self.options) != 4:
                raise ValueError("mcq cards need exactly 4 options")
            if self.answer not in self.options:
                raise ValueError("mcq answer must be one of the options")
        return self


class CardSet(BaseModel):
    cards: list[Card] = Field(min_length=1, max_length=5)


PROBLEM_SYSTEM = f"""You write interview-prep flashcards from a LeetCode problem and its reference solution.
Write 2-3 cards:
1. typed: "Which pattern / approach fits this problem, and why?" (describe the problem briefly in the prompt; never name it by its title).
2. typed or flash: the key insight or invariant that makes the optimal solution work, or its time/space complexity with the reason.
3. optionally mcq: a common wrong approach vs the right one.
{RULES}"""

DOC_SYSTEM = f"""You write interview-prep flashcards from one section of study material.
Write 2-4 cards on the most interview-relevant ideas in the section. Prefer "why" and trade-off questions over definitions.
Use a mix of formats: typed for explanations, flash for crisp facts, mcq when there are clear wrong alternatives,
output only for a code snippet whose output follows from the section.
If the section has nothing interview-relevant, return one flash card on its most useful fact.
{RULES}"""


def for_problem(llm, problem: dict, tier: str = "smart") -> list[dict]:
    user = (
        f"Problem: {problem['title']} ({problem['difficulty']}), pattern: {problem.get('pattern') or 'unknown'}\n\n"
        f"Statement:\n{problem['statement'][:4000]}\n\nReference solution:\n{(problem.get('solution') or '')[:3000]}"
    )
    result = llm.complete_json(PROBLEM_SYSTEM, user, CardSet, tier=tier, purpose="cards-problem")
    return [{**c.model_dump(), "problem_slug": problem["slug"], "document_id": None,
             "topic_slug": problem.get("pattern_slug")} for c in result.cards]


def for_document(llm, doc: dict, tier: str = "smart") -> list[dict]:
    user = f"Area: {doc['domain']}\nSection: {doc['title']}\n\n{doc['body'][:6000]}"
    result = llm.complete_json(DOC_SYSTEM, user, CardSet, tier=tier, purpose="cards-doc")
    return [{**c.model_dump(), "problem_slug": None, "document_id": doc["id"],
             "topic_slug": doc.get("topic_slug")} for c in result.cards]
