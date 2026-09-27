"""The card sample Aman reads, and hands to an outside reviewer.

One sample gates every batch, because reviewing 20 cards from each of 16
batches is 320 cards and he will not do that - and a review nobody finishes
is worse than a smaller one that gets done.

So: 25 cards, spread across areas and formats, weighted toward the ones the
gate was least sure about, each shown with the lesson it came from. An
outside reviewer can only judge "could someone answer this?" if they can see
what the reader was taught, and a card that quietly needs unseen context is
the exact failure that started this rebuild.

Every rejected card is listed too, with the gate's reason. The gate is as
much on trial as the cards: its first run rejected 40 good cards out of 42.
"""

import json

SAMPLE = 25
FORMATS = ("typed", "flash", "mcq", "output")


def sample(con, size: int = SAMPLE) -> list[dict]:
    """Least-confident first, one card per topic at most.

    Partitioning only by area and format let a single shaky topic take several
    of the 25 places while other topics got none, which narrows exactly the
    range the reviewer is there to cover."""
    rows = con.execute(
        """
        select c.id, c.topic_slug, t.domain, t.name, c.format, c.difficulty, c.prompt_md,
               c.options, c.answer_md, c.key_points, c.quality, l.body_md
        from cards c
        join topics t on t.slug = c.topic_slug
        join lessons l on l.topic_slug = c.topic_slug
        where c.source = 'lesson' and c.status = 'draft'
        qualify row_number() over (
            partition by c.topic_slug
            order by coalesce(cast(json_extract(c.quality, '$.gate_confidence') as double), 0.5), c.id
        ) = 1
        order by coalesce(cast(json_extract(c.quality, '$.gate_confidence') as double), 0.5), t.domain, c.id
        """
    ).fetchall()
    cols = ["id", "slug", "domain", "topic", "format", "difficulty", "prompt", "options",
            "answer", "key_points", "quality", "lesson"]
    candidates = [dict(zip(cols, r)) for r in rows]

    # One per topic, then spread across area and format by taking turns. Doing
    # the spread in SQL capped each group at four and left those places empty
    # when the topic filter removed them, so the sample shrank instead of
    # drawing from elsewhere.
    picked: list[dict] = []
    seen_groups: dict[tuple, int] = {}
    for allowed in (1, 2, 3, 4, 99):
        for card in candidates:
            if len(picked) >= size:
                break
            if card in picked:
                continue
            group = (card["domain"], card["format"])
            if seen_groups.get(group, 0) >= allowed:
                continue
            seen_groups[group] = seen_groups.get(group, 0) + 1
            picked.append(card)
        if len(picked) >= size:
            break
    return picked[:size]


def rejected(con) -> list[dict]:
    rows = con.execute(
        """select topic_slug, format, prompt_md, reject_reason from cards
           where source = 'lesson' and status = 'rejected' order by topic_slug"""
    ).fetchall()
    return [dict(zip(["slug", "format", "prompt", "reason"], r)) for r in rows]


def report(con) -> str:
    kept, dropped = con.execute(
        """select count(*) filter (where status = 'draft'), count(*) filter (where status = 'rejected')
           from cards where source = 'lesson'"""
    ).fetchone()
    mix = con.execute(
        """select format, count(*) from cards where source = 'lesson' and status = 'draft'
           group by 1 order by 2 desc"""
    ).fetchall()
    picked, refused = sample(con), rejected(con)

    lines = [
        "# 90x card review",
        "",
        f"{kept} cards were generated and {dropped} rejected by an automated gate "
        f"({dropped / max(1, kept + dropped):.0%}). Mix: " + ", ".join(f"{n} {f}" for f, n in mix) + ".",
        "",
        "## What these are",
        "",
        "90x is an interview-prep app. Each topic has one authored lesson, and cards are generated "
        "from that lesson to test recall. A reader answers a card **without** the lesson in front of "
        "them: typed answers are graded by a model against the listed key points, multiple choice by "
        "the marked option, and output cards by exact match.",
        "",
        "## What to judge",
        "",
        "1. **Could a competent engineer who studied this lesson answer this, with nothing else in front of them?** "
        "A card that needs the lesson open is broken, however good it looks beside it.",
        "2. **Is the format right?** Typed for explanation and trade-offs, flash for one crisp fact, "
        "multiple choice where the options matter, output where a snippet has one unambiguous result.",
        "3. **Are the key points gradable?** They are what a model checks a typed answer against.",
        "4. **Are the wrong options real mistakes?** A distractor nobody would pick makes the card a reading test.",
        "5. **Was the gate right?** The rejected cards are at the end with its reasons. It has been wrong before: "
        "an earlier version rejected 40 good cards out of 42 because it misread conceptual questions as malformed.",
        "",
        f"Below: {len(picked)} cards, spread across areas and formats, weighted toward the ones the gate was "
        "least sure about. Each is shown with the lesson it came from.",
        "",
        "---",
        "",
    ]

    for i, card in enumerate(picked, 1):
        confidence = (json.loads(card["quality"] or "{}") or {}).get("gate_confidence")
        lines += [
            f"## {i}. {card['topic']} · {card['format']} · {card['difficulty']}",
            "",
            f"*{card['domain']} · gate confidence {confidence if confidence is not None else 'n/a'}*",
            "",
            "**Question**",
            "",
            card["prompt"],
            "",
        ]
        if card["options"]:
            lines += ["**Options**", ""] + [f"- {o}" for o in json.loads(card["options"])] + [""]
        lines += [
            "**Reference answer**",
            "",
            card["answer"],
            "",
            "**Graded on**",
            "",
        ]
        lines += [f"- {p}" for p in json.loads(card["key_points"] or "[]")]
        lines += [
            "",
            "<details><summary>The lesson this came from</summary>",
            "",
            card["lesson"],
            "",
            "</details>",
            "",
            "---",
            "",
        ]

    lines += ["## Cards the gate rejected", "",
              "Judge whether it was right. Each was thrown away." if refused else "None.", ""]
    for card in refused:
        lines += [f"- **{card['slug']}** ({card['format']}): {card['prompt']}", f"  - Gate said: {card['reason']}", ""]
    return "\n".join(lines)
