"""Author one lesson per topic.

The model fills fields; we render the Markdown. Asking for prose back gives
you a different shape every time - headings that wander, stray link tables,
whatever the source happened to look like. A schema plus our own renderer
makes every lesson in the app read the same way.
"""

from pydantic import BaseModel, Field

SYSTEM = """You write one lesson for an interview-prep app. The reader is an experienced engineer preparing for interviews in 90 days. They will read this lesson and nothing else on the topic.

The source material below is scraped from books, repos and course notes. It is raw: it may be a whole book chapter, a list of questions, a table of links, or badly extracted PDF text. Use it for facts only. Never describe it, quote its structure, or refer to it.

Hard rules:
- The lesson must stand alone. A reader who has never seen the source must understand every sentence.
- Never write "the passage", "the text", "the above", "this section", "the chapter", "the author", or "the reference solution". The reader cannot see any of those.
- Write plain, direct English. No filler, no "in today's fast-paced world", no restating the question.
- Facts must come from the source material where it covers the topic. Where it does not, use well-established knowledge and stay conservative.
- No URLs, no markdown links, no tables. Links belong nowhere in a lesson.
- Explain, don't list definitions. Prefer why and trade-offs over vocabulary.

Fields:
- summary: one sentence, under 140 characters, what this topic is. Shown in lists.
- what_it_is: 2-4 sentences defining the topic concretely.
- why_asked: 2-3 sentences on what an interviewer is really testing.
- mental_model: 3-6 sentences giving the reader one way to hold the idea in their head. This is the part they should remember a month later.
- key_points: 3-5 points a strong candidate must know. One sentence each, independently checkable.
- worked_example: a concrete example with real numbers, names or code. 3-8 sentences. Show the reasoning, not just the conclusion.
  Never write it as the reader's own experience, and never invent a statistic, a company or a result to make it sound real. The reader may repeat what you write in an actual interview, so a made-up "reduced errors by 30%" is a trap, not an example.
  For a behavioural topic the reader supplies their own story, so show the *shape* of a strong answer instead: open with "A strong answer sounds like:" and keep any placeholder obviously generic.
- traps: 2-4 specific mistakes candidates make. One sentence each. Name the mistake, not the virtue.
- should_answer: 3-5 questions the reader should be able to answer after reading. Each ends with a question mark. These become practice cards, so make them answerable from this lesson alone."""


class Lesson(BaseModel):
    summary: str = Field(min_length=20, max_length=200)
    what_it_is: str = Field(min_length=60)
    why_asked: str = Field(min_length=40)
    mental_model: str = Field(min_length=80)
    key_points: list[str] = Field(min_length=3, max_length=5)
    worked_example: str = Field(min_length=80)
    traps: list[str] = Field(min_length=2, max_length=4)
    should_answer: list[str] = Field(min_length=3, max_length=5)


def render(lesson: Lesson) -> str:
    """The one place a lesson becomes Markdown."""
    parts = [
        lesson.what_it_is.strip(),
        "## Why interviewers ask this",
        lesson.why_asked.strip(),
        "## The mental model",
        lesson.mental_model.strip(),
        "## Key points",
        "\n".join(f"- {p.strip()}" for p in lesson.key_points),
        "## Worked example",
        lesson.worked_example.strip(),
        "## Common traps",
        "\n".join(f"- {t.strip()}" for t in lesson.traps),
        "## You should be able to answer",
        "\n".join(f"- {q.strip()}" for q in lesson.should_answer),
    ]
    return "\n\n".join(parts)


def write(llm, topic: dict, context: str, tier: str = "smart") -> Lesson:
    user = (
        f"Topic: {topic['name']}\n"
        f"Domain: {topic['domain']}\n"
        f"{'Part of: ' + topic['parent_name'] if topic.get('parent_name') else ''}\n"
        f"{'Description: ' + topic['description'] if topic.get('description') else ''}\n\n"
        f"Source material:\n{context if context.strip() else '(none - write from well-established knowledge)'}"
    )
    return llm.complete_json(SYSTEM, user, Lesson, tier=tier, purpose="lesson")
