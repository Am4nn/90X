"""The lesson contract. Each case is a failure the first content pass shipped."""

import json

import pytest

from pipeline.lessons import check as checks
from pipeline.lessons.context import rank, words
from pipeline.lessons import evidence as ev
from pipeline.lessons.write import FollowUp, Lesson, render

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
    problems = checks.check("word " * 1500, ["A?", "B?", "C?"])
    assert any("too long" in p for p in problems)


def test_accepts_an_imperative_follow_up():
    """"Walk me through the TLS handshake." is what an interviewer actually
    says; requiring a question mark rejected a perfectly good lesson."""
    assert checks.check(GOOD_BODY, ["Walk me through the TLS handshake.",
                                    "What breaks under load?",
                                    "Compare it with the alternative."]) == []


def test_rejects_a_follow_up_that_is_not_a_prompt():
    problems = checks.check(GOOD_BODY, ["What is a process?", "Processes are useful.", "Why?"])
    assert any("interviewer would say" in p for p in problems)


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
        core_idea=prose("charlie"),
        key_points=["first point", "second point", "third point"],
        sixty_second_answer=prose("echo"),
        follow_ups=[
            FollowUp(question="What is a process?", answer="A running program with its own memory."),
            FollowUp(question="Why does it matter?", answer="It is the unit the scheduler works with."),
            FollowUp(question="When does it break?", answer="When two processes need shared state."),
        ],
        worked_example=prose("delta"),
        traps=["first trap", "second trap"],
    )
    md = render(lesson)
    for fragment in (prose("alpha"), prose("bravo"), prose("charlie"), prose("delta"), prose("echo"),
                     "- first point", "- second trap", "**What is a process?**",
                     "A running program with its own memory."):
        assert fragment in md
    assert md.startswith("alpha"), "the definition opens the lesson, with no heading above it"
    assert checks.check(md, [f.question for f in lesson.follow_ups]) == []


def test_follow_ups_are_a_ladder_not_a_quiz():
    """The ladder carries answers, so the reader can rehearse the depth an
    interviewer pushes them to, not just recognise the question."""
    lesson_md = render(
        Lesson(
            summary="A process is a running program.",
            what_it_is=" ".join(["alpha"] * 80),
            why_asked=" ".join(["bravo"] * 40),
            core_idea=" ".join(["charlie"] * 40),
            key_points=["a", "b", "c"],
            sixty_second_answer=" ".join(["echo"] * 60),
            follow_ups=[
                FollowUp(question="Shallow one?", answer="The shallow answer goes here."),
                FollowUp(question="Deeper one?", answer="The deeper answer goes here."),
                FollowUp(question="Hardest one?", answer="The hardest answer goes here."),
            ],
            worked_example=" ".join(["delta"] * 40),
            traps=["x", "y"],
        )
    )
    assert lesson_md.index("Shallow one?") < lesson_md.index("Deeper one?") < lesson_md.index("Hardest one?")
    assert "The hardest answer goes here." in lesson_md


def test_evidence_names_only_companies_that_ask_often():
    """A company at 12% frequency is noise; naming it would be the kind of
    unsupported specificity the lesson is meant to avoid."""
    companies = json.dumps({"Google": 100.0, "Amazon": 87.0, "Tinybrand": 12.0})
    assert ev.top_companies(companies) == ["Google", "Amazon"]
    assert ev.top_companies(None) == []
    assert ev.top_companies("not json") == []


def test_only_two_domains_claim_real_evidence():
    assert ev.has_evidence({"domain": "dsa"})
    assert ev.has_evidence({"domain": "system_design"})
    assert not ev.has_evidence({"domain": "behavioral"})
    assert not ev.has_evidence({"domain": "java"})


def test_questions_match_on_topic_wording():
    questions = [
        {"slug": "sched", "title": "Design a Job Scheduler", "difficulty": "Medium",
         "follow_ups": ["How will you schedule jobs?"]},
        {"slug": "url", "title": "Design a URL Shortener", "difficulty": "Easy", "follow_ups": []},
    ]
    found = ev.questions_for({"name": "Job scheduling", "description": ""}, questions)
    assert [q["slug"] for q in found] == ["sched"]


def test_rank_prefers_the_closer_title():
    target = words("TCP three way handshake")
    items = rank(
        [(words("Deadlocks"), "deadlocks"), (words("TCP handshake"), "tcp"), (words("TCP flow control"), "flow")],
        target,
    )
    assert items[0] == "tcp"
    assert "deadlocks" not in items, "a title sharing no words is dropped, not ranked last"
