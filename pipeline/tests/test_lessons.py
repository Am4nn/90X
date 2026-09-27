"""The lesson contract. Each case is a failure the first content pass shipped."""

import pytest

from pipeline.lessons import check as checks
from pipeline.lessons.context import rank, words
from pipeline.lessons.write import Lesson, render

GOOD_BODY = " ".join(["A process is a running program with its own address space."] * 40)


def body_with(extra: str) -> str:
    return f"{GOOD_BODY}\n\n{extra}"


def test_clean_lesson_passes():
    assert checks.check(GOOD_BODY, ["What is a process?", "Why does it matter?", "How is it scheduled?"]) == []


@pytest.mark.parametrize(
    "text, expected",
    [
        ("As the passage states, a process has its own address space.", "refers to source"),
        ("The reference solution sets d[x] = d[y] + y - x.", "refers to source"),
        ("According to the text, paging is transparent.", "refers to source"),
        ("This section covers scheduling.", "refers to source"),
        ("How should you handle disagreement, according to this lesson?", "refers to source"),
        ("The lesson explains why paging is transparent.", "refers to source"),
        ("<div class='note'>Careful</div>", "raw HTML"),
        ("The deﬁnition of a process is simple.", "ligature"),
        ("Read more at https://example.com/paging", "link"),
        ("See [the guide](https://example.com)", "link"),
        ("| Pattern | Use |\n| --- | --- |", "table"),
        ("A process is defined infor- mally as a running program.", "broken by PDF"),
    ],
)
def test_rejects(text, expected):
    problems = checks.check(body_with(text), ["Is this fine?", "And this?", "And that?"])
    assert any(expected in p for p in problems), problems


def test_rejects_too_short():
    problems = checks.check("Three words only", ["A?", "B?", "C?"])
    assert any("too short" in p for p in problems)


def test_rejects_too_long():
    problems = checks.check("word " * 1300, ["A?", "B?", "C?"])
    assert any("too long" in p for p in problems)


def test_rejects_non_question_in_should_answer():
    problems = checks.check(GOOD_BODY, ["What is a process?", "Explain scheduling.", "Why?"])
    assert any("not a question" in p for p in problems)


def test_postcard_metaphor_is_not_a_false_positive():
    """A lesson comparing HTTP to a postcard says "the card" about the postcard,
    not about a flashcard."""
    fine = body_with("Every response has a status code telling you whether the card was delivered or rejected.")
    assert checks.check(fine, ["A?", "B?", "C?"]) == []


def test_ordinary_prose_is_not_a_false_positive():
    """"the section of memory" and "the article number" are normal English."""
    fine = body_with("The section of memory holding the stack grows downward, and the text segment is read-only.")
    problems = checks.check(fine, ["A?", "B?", "C?"])
    assert problems == [], problems


def test_render_puts_every_field_in_the_markdown():
    def prose(word: str) -> str:
        return " ".join([word] * 70)

    lesson = Lesson(
        summary="A process is a running program.",
        what_it_is=prose("alpha"),
        why_asked=prose("bravo"),
        mental_model=prose("charlie"),
        key_points=["first point", "second point", "third point"],
        worked_example=prose("delta"),
        traps=["first trap", "second trap"],
        should_answer=["What is it?", "Why does it matter?", "When does it break?"],
    )
    md = render(lesson)
    for fragment in (prose("alpha"), prose("bravo"), prose("charlie"), prose("delta"),
                     "- first point", "- second trap", "- What is it?"):
        assert fragment in md
    assert md.startswith("alpha"), "the definition opens the lesson, with no heading above it"
    assert checks.check(md, lesson.should_answer) == []


def test_rank_prefers_the_closer_title():
    target = words("TCP three way handshake")
    items = rank(
        [(words("Deadlocks"), "deadlocks"), (words("TCP handshake"), "tcp"), (words("TCP flow control"), "flow")],
        target,
    )
    assert items[0] == "tcp"
    assert "deadlocks" not in items, "a title sharing no words is dropped, not ranked last"
