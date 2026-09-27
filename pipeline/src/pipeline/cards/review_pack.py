"""The card sample Aman reads before a bulk run.

One card of each format per topic, plus everything the gate rejected with its
reason. The rejections matter as much as the keeps: a gate that rejects the
wrong things is worse than no gate, and the first pilot did exactly that -
50% rejected, and 40 of 42 were good cards the gate misread.
"""

import json

FORMATS = ("typed", "flash", "mcq", "output")


def report(con) -> str:
    kept, rejected = con.execute(
        """select count(*) filter (where status = 'draft'), count(*) filter (where status = 'rejected')
           from cards where source = 'lesson'"""
    ).fetchone()
    mix = con.execute(
        """select format, count(*) from cards where source = 'lesson' and status = 'draft'
           group by 1 order by 2 desc"""
    ).fetchall()

    lines = [
        "# Cards: the sample before a bulk run",
        "",
        f"{kept} kept, {rejected} rejected by the gate ({rejected / max(1, kept + rejected):.0%}). "
        + "Format mix: " + ", ".join(f"{n} {f}" for f, n in mix) + ".",
        "",
        "**What to check:** could you answer each one having read the lesson and nothing else? "
        "Is the format right - typed for explanation, flash for a fact, mcq where the options matter? "
        "Then skim the rejections and tell me whether the gate threw away anything good.",
        "",
        "---",
        "",
    ]

    topics = [r[0] for r in con.execute(
        "select distinct topic_slug from cards where source = 'lesson' and status = 'draft' order by 1"
    ).fetchall()]
    for slug in topics:
        lines += [f"## {slug}", ""]
        for fmt in FORMATS:
            row = con.execute(
                """select prompt_md, answer_md, options, key_points, difficulty from cards
                   where source = 'lesson' and status = 'draft' and topic_slug = ? and format = ? limit 1""",
                [slug, fmt],
            ).fetchone()
            if not row:
                continue
            prompt, answer, options, key_points, difficulty = row
            lines += [f"**{fmt}** ({difficulty}) - {prompt}", ""]
            if options:
                lines += [f"- {o}" for o in json.loads(options)] + [""]
            lines += [f"> {answer}", "", f"*Graded on: {', '.join(json.loads(key_points or '[]'))}*", ""]
        lines.append("---")
        lines.append("")

    dropped = con.execute(
        """select topic_slug, format, prompt_md, reject_reason from cards
           where source = 'lesson' and status = 'rejected' order by topic_slug"""
    ).fetchall()
    lines += ["## What the gate rejected", ""]
    if not dropped:
        lines.append("Nothing.")
    for slug, fmt, prompt, reason in dropped:
        lines += [f"- **{slug}** ({fmt}): {prompt}", f"  - {reason}"]
    return "\n".join(lines)
