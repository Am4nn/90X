"""The short list of lessons worth a human's eyes.

Nobody reads 268 lessons. The automated gates read all of them; this picks
the ones where a person's judgement actually changes something:

- every lesson the fact-checker still objects to after its rewrites, because
  those are stored unpublished and someone has to rule on them, and
- the most important topic in each area, as a sample of the standard.

Everything else ships on the gates. If the samples are good and the
objections are fair, the gates are working; if a sample is bad, the problem
is the generator and the whole run needs another look.
"""

import json


def failures(con) -> list[dict]:
    rows = con.execute(
        """select topic_slug, title, words, problems, findings, body_md
           from lessons where status = 'failed' order by topic_slug"""
    ).fetchall()
    return [dict(zip(["slug", "title", "words", "problems", "findings", "body"], r)) for r in rows]


def samples(con) -> list[dict]:
    """The most important topic in each area that passed everything."""
    rows = con.execute(
        """select l.topic_slug, l.title, l.words, t.domain, t.importance, l.body_md, l.practice
           from lessons l join topics t on t.slug = l.topic_slug
           where l.status = 'ok'
           qualify row_number() over (partition by t.domain order by t.importance desc, t.slug) = 1
           order by t.domain"""
    ).fetchall()
    return [dict(zip(["slug", "title", "words", "domain", "importance", "body", "practice"], r)) for r in rows]


def report(con) -> str:
    failed, sampled = failures(con), samples(con)
    total, ok = con.execute("select count(*), count(*) filter (where status = 'ok') from lessons").fetchone()

    lines = [
        "# Lessons: what needs your eyes",
        "",
        f"{ok} of {total} lessons passed every gate. Below are the {len(failed)} the fact-checker "
        f"still objects to, then one sample from each of the {len(sampled)} areas.",
        "",
        "**What to do:** read two or three samples. If they are the standard you want, the rest ship. "
        "Then skim the objections - each one is a claim a second model says is wrong or half-true, "
        "and the lesson is held back until someone rules on it.",
        "",
        "---",
        "",
        "## Held back by the fact-checker",
        "",
    ]
    if not failed:
        lines.append("Nothing. Every lesson passed.")
    for lesson in failed:
        lines += [f"### {lesson['title']}  `{lesson['slug']}`", ""]
        for f in json.loads(lesson["findings"] or "[]"):
            lines += [
                f"- **{f['verdict']}**: {f['claim']}",
                f"  - Reviewer says: {f['correction']}",
            ]
        if not json.loads(lesson["findings"] or "[]"):
            lines.append(f"- Failed the contract: {lesson['problems']}")
        lines.append("")

    lines += ["---", "", "## One sample per area", ""]
    for lesson in sampled:
        practice = json.loads(lesson["practice"] or "{}")
        counts = f"{len(practice.get('problems') or [])} problems, {len(practice.get('questions') or [])} real questions"
        lines += [
            f"## {lesson['title']}  `{lesson['slug']}`",
            "",
            f"*{lesson['domain']} - {lesson['words']} words - {counts}*",
            "",
            lesson["body"],
            "",
            "---",
            "",
        ]
    return "\n".join(lines)
