"""What real interviews actually ask, pulled from our own data.

A lesson that says "interviewers often ask about X" is the model guessing.
A lesson that says "Two Sum is asked at Google, Amazon and Bloomberg" is a
fact we hold: 3,088 problems carry per-company frequency, and 55 system
design questions carry the follow-ups a real interviewer probes with.

Only two domains have this evidence today - dsa through `pattern_slug`, and
system_design through systemdesign.io. `problems.topic_slugs` joins to no
topic, so it is not a path. Everywhere else returns nothing rather than
inventing something, and `has_evidence` says which is which.
"""

import json

from ..normalize.interview_questions import parse_all
from .context import words

MAX_PROBLEMS = 10
MAX_COMPANIES = 6
MAX_QUESTIONS = 3
# A company is worth naming when it asks the problem often, not rarely.
MIN_FREQUENCY = 60.0


def top_companies(companies_json: str | None) -> list[str]:
    if not companies_json:
        return []
    try:
        companies = json.loads(companies_json)
    except (ValueError, TypeError):
        return []
    ranked = sorted(
        ((name, freq) for name, freq in companies.items() if freq >= MIN_FREQUENCY),
        key=lambda c: -c[1],
    )
    return [name for name, _ in ranked[:MAX_COMPANIES]]


def problems_for(con, topic_slug: str) -> list[dict]:
    """DSA topics are pattern buckets: every problem tagged with the pattern.

    Interview problems only. The catalog also holds 268 contest problems with
    stdin/stdout and huge hidden test suites; they are a different sport, and
    four of them turned up in the sliding-window practice list, which is not
    what someone with 90 days before an SDE loop should be spending time on.
    A NeetCode 150 or Blind 75 problem outranks a merely important one.
    """
    rows = con.execute(
        """select slug, title, difficulty, companies, importance
           from problems where pattern_slug = ? and kind = 'leetcode'
           order by (nc150 or blind75) desc, importance desc limit ?""",
        [topic_slug, MAX_PROBLEMS],
    ).fetchall()
    return [
        {"slug": s, "title": t, "difficulty": d, "companies": top_companies(c), "importance": i}
        for s, t, d, c, i in rows
    ]


def questions_for(topic: dict, questions: list[dict] | None = None) -> list[dict]:
    """Real system design questions whose wording overlaps this topic."""
    target = words(topic["name"]) | words(topic.get("description") or "")
    scored = []
    for q in questions if questions is not None else parse_all():
        text = words(q["title"]) | words(" ".join(q["follow_ups"]))
        hit = len(target & text)
        if hit:
            scored.append((hit, q))
    scored.sort(key=lambda s: -s[0])
    return [q for _, q in scored[:MAX_QUESTIONS]]


def for_topic(con, topic: dict, questions: list[dict] | None = None) -> tuple[str, dict]:
    """Returns (prompt text, what was linked). Empty text means no evidence."""
    linked: dict = {"problems": [], "questions": []}
    parts: list[str] = []

    if topic["domain"] == "dsa":
        problems = problems_for(con, topic["slug"])
        if problems:
            linked["problems"] = [p["slug"] for p in problems]
            lines = [
                f"- {p['title']} ({p['difficulty']})"
                + (f" - asked at {', '.join(p['companies'])}" if p["companies"] else "")
                for p in problems
            ]
            parts.append(
                "Problems in this pattern, with the companies that ask them most "
                "(real frequency data, use it instead of guessing):\n" + "\n".join(lines)
            )

    if topic["domain"] == "system_design":
        found = questions_for(topic, questions)
        if found:
            linked["questions"] = [q["slug"] for q in found]
            for q in found:
                ladder = "\n".join(f"    {i}. {f}" for i, f in enumerate(q["follow_ups"], 1))
                asked_at = ", ".join(q.get("companies") or [])
                parts.append(
                    f"A real interview question on this topic: \"{q['title']}\" ({q['difficulty']})"
                    + (f", asked at {asked_at}" if asked_at else "")
                    + ".\n  The follow-ups interviewers actually probe with, in the order they escalate:\n"
                    + ladder
                )

    return "\n\n".join(parts), linked


def has_evidence(topic: dict) -> bool:
    return topic["domain"] in {"dsa", "system_design"}
