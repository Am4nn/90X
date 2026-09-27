"""Author one lesson per topic.

The model fills fields; we render the Markdown. Asking for prose back gives
you a different shape every time - headings that wander, stray link tables,
whatever the source happened to look like. A schema plus our own renderer
makes every lesson in the app read the same way.

The lesson is built for interview performance, not just comprehension: the
spoken 60-second answer and the follow-up ladder are what actually gets
tested, and where we have real data (company frequency, real interview
follow-ups) the lesson is grounded in it rather than in the model's guess.
"""

from pydantic import BaseModel, Field

SYSTEM = """You write one lesson for an interview-prep app used by working engineers preparing for SDE interviews in 90 days. They will read this lesson and nothing else on the topic, then be asked about it in an interview.

The source material below is scraped from books, repos and course notes. It is raw: it may be a whole book chapter, a list of questions, a table of links, or badly extracted PDF text. Use it for facts only. Never describe it, quote its structure, or refer to it.

ACCURACY IS THE FIRST PRIORITY. A confident wrong sentence is worse than no lesson: the reader will repeat it in an interview and be caught. Prefer a precise, narrower claim over a sweeping one. State conditions where a rule only holds sometimes ("on a single core", "for a hash map with good distribution"). If the source material conflicts with well-established knowledge, follow well-established knowledge. If you are unsure of a number, a complexity, or a protocol detail, leave it out rather than guess. Never invent a statistic, benchmark, company, date or result.

SAY WHICH VERSION OR ENGINE A CLAIM BELONGS TO whenever it is not universally true. "Java 8 added" or "since Java 17", "in PostgreSQL", "MySQL's InnoDB", "HTTP/2 onwards". A reader who repeats an engine-specific detail as a general rule gets corrected by the interviewer, and a reader who cannot tell which engine you meant cannot use the fact at all. Where behaviour genuinely differs between the common engines or versions, say so in one clause rather than picking one silently.

NEVER reproduce the source code of a real library, framework or standard implementation from memory - not a line of it, not a condition, not a field name. Recalling it feels reliable and is not: an exact-looking JDK condition written from memory came out as code that dereferences a null it just tested for. Describe what the implementation does and why, in prose, and give thresholds only when you are certain of them. Code in a lesson is for illustrating the idea in a few lines you write yourself, never for quoting a real codebase.

WRITE LIKE AN ENGINEER, NOT A CONTENT FARM:
- No analogy unless it genuinely earns its place. A forced metaphor is worse than a direct explanation. Most topics need none.
- Vary sentence length and structure. Do not open every section the same way.
- Banned: "in today's fast-paced world", "it's important to note", "let's dive in", "at the end of the day", "think of it like", "imagine you are", "in a nutshell", "the key takeaway is".
- No restating the question before answering it. No summarising what you just said.
- Be concrete. Name the real mechanism, the real data structure, the real failure.

Fields:
- summary: one sentence, under 140 characters, what this topic is. Shown in lists.
- what_it_is: 2-4 sentences defining the topic precisely. Lead with the mechanism, not the category.
- why_asked: 2-3 sentences on what the interviewer is really testing. If evidence below names companies or real questions, use it; otherwise describe the signal, not made-up popularity.
- core_idea: 3-6 sentences the reader should still have a month from now. Use an analogy only if it makes something genuinely clearer; otherwise explain it directly.
- key_points: 3-5 points a strong candidate must know. One sentence each, independently checkable, each stating a fact rather than a category.
- sixty_second_answer: what the reader should actually say out loud if asked this cold, written as speech, 90-150 words. It must stand on its own, open with the direct answer, then the reason, then one trade-off. No headings, no lists.
- follow_ups: 3-5 questions the interviewer asks NEXT, ordered from shallow to deep, each with the answer a strong candidate gives in 1-3 sentences. This is a depth ladder: the last one should be genuinely hard. If real follow-ups are given in the evidence below, use them and keep their escalation.
- worked_example: a concrete example with real mechanics - numbers, code, or a specific sequence of events. 3-8 sentences. Show the reasoning, not just the conclusion.
  Never write it as the reader's own experience, and never invent a statistic, a company or a result to make it sound real. The reader may repeat what you write in an actual interview, so a made-up "reduced errors by 30%" is a trap, not an example.
  For a behavioural topic the reader supplies their own story, so show the *shape* of a strong answer instead: open with "A strong answer sounds like:" and keep any placeholder obviously generic.
- traps: 2-4 specific mistakes candidates make. One sentence each. Name the mistake, not the virtue."""


class FollowUp(BaseModel):
    question: str = Field(min_length=10)
    answer: str = Field(min_length=20)


class Lesson(BaseModel):
    summary: str = Field(min_length=20, max_length=200)
    what_it_is: str = Field(min_length=60)
    why_asked: str = Field(min_length=40)
    core_idea: str = Field(min_length=80)
    key_points: list[str] = Field(min_length=3, max_length=5)
    sixty_second_answer: str = Field(min_length=200)
    follow_ups: list[FollowUp] = Field(min_length=3, max_length=5)
    worked_example: str = Field(min_length=80)
    traps: list[str] = Field(min_length=2, max_length=4)


def render(lesson: Lesson) -> str:
    """The one place a lesson becomes Markdown."""
    ladder = "\n\n".join(f"**{f.question.strip()}**\n\n{f.answer.strip()}" for f in lesson.follow_ups)
    parts = [
        lesson.what_it_is.strip(),
        "## Why interviewers ask this",
        lesson.why_asked.strip(),
        "## The core idea",
        lesson.core_idea.strip(),
        "## Key points",
        "\n".join(f"- {p.strip()}" for p in lesson.key_points),
        "## Your 60-second answer",
        lesson.sixty_second_answer.strip(),
        "## If they dig deeper",
        ladder,
        "## Worked example",
        lesson.worked_example.strip(),
        "## Common traps",
        "\n".join(f"- {t.strip()}" for t in lesson.traps),
    ]
    return "\n\n".join(parts)


def write(llm, topic: dict, context: str, evidence: str = "", notes: str = "", tier: str = "smart") -> Lesson:
    user = (
        f"Topic: {topic['name']}\n"
        f"Domain: {topic['domain']}\n"
        f"{'Part of: ' + topic['parent_name'] if topic.get('parent_name') else ''}\n"
        f"{'Description: ' + topic['description'] if topic.get('description') else ''}\n\n"
        + (f"EVIDENCE - real interview data for this topic. Ground the lesson in it:\n{evidence}\n\n" if evidence else "")
        + (f"CORRECTIONS from a reviewer of your previous attempt. Fix every one:\n{notes}\n\n" if notes else "")
        + f"Source material:\n{context if context.strip() else '(none - write from well-established knowledge)'}"
    )
    return llm.complete_json(SYSTEM, user, Lesson, tier=tier, purpose="lesson")
