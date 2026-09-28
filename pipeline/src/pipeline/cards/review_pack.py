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


def rejected(con, status: str = "rejected") -> list[dict]:
    rows = con.execute(
        """select topic_slug, format, prompt_md, reject_reason from cards
           where source = 'lesson' and status = ? order by topic_slug""",
        [status],
    ).fetchall()
    return [dict(zip(["slug", "format", "prompt", "reason"], r)) for r in rows]


def selector(con, slug: str, prompt: str) -> str:
    """The shortest leading fragment of `prompt` that no sibling card shares.

    A fixed 60 characters is not necessarily unique: two cards in a topic can
    open the same way, and `pick` refuses an ambiguous fragment - so the report
    would print an instruction that cannot be followed.
    """
    # Matched the way `pick` matches - case-insensitively, anywhere in the
    # question - because a selector tested any other way can still be ambiguous
    # to the code that has to use it.
    others = [
        " ".join(r[0].split()).casefold()
        for r in con.execute(
            """select prompt_md from cards where topic_slug = ? and source = 'lesson'
                 and status in ('draft', 'rejected') and prompt_md <> ?""",
            [slug, prompt],
        ).fetchall()
    ]
    mine = " ".join(prompt.split())
    for n in (60, 90, 120, 160, 200):
        head = mine[:n]
        if not any(head.casefold() in o for o in others):
            return head
    return mine


def report(con) -> str:
    kept, dropped, fixed = con.execute(
        """select count(*) filter (where status = 'draft'),
                  count(*) filter (where status = 'rejected'),
                  count(*) filter (where status = 'repaired')
           from cards where source = 'lesson'"""
    ).fetchone()
    mix = con.execute(
        """select format, count(*) from cards where source = 'lesson' and status = 'draft'
           group by 1 order by 2 desc"""
    ).fetchall()
    picked, refused = sample(con), rejected(con)
    sent_back = rejected(con, "repaired")

    seen = kept + dropped
    caught = dropped + fixed
    lines = [
        "# 90x card review",
        "",
        f"{kept} cards are ready to publish. An automated gate read {seen} and objected to "
        f"{caught} of them ({caught / max(1, seen):.0%}): {fixed} were rewritten and passed on the "
        f"second look, {dropped} could not be saved and were dropped "
        f"({dropped / max(1, seen):.0%}). Mix: " + ", ".join(f"{n} {f}" for f, n in mix) + "."
        + ("" if fixed else "\n\n*No card here is recorded as caught-and-rewritten. Card runs before "
           "2026-09-28 did not keep that record, so on an older run the rewrite pass is invisible "
           "rather than idle, and the drop rate is the only measured number above.*"),
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
        # The slug and a fragment of the question, so an objection can name this
        # exact card. Without it, an objection keyed on the topic alone hit
        # whichever of the topic's ten cards came first - which is how twelve of
        # thirteen reviewer objections rewrote a card nobody complained about.
        first_line = selector(con, card["slug"], card["prompt"])
        lines += [
            f"## {i}. {card['topic']} · {card['format']} · {card['difficulty']}",
            "",
            f"*{card['domain']} · gate confidence {confidence if confidence is not None else 'n/a'}*",
            "",
            f"<sub>to object to this card: `## {card['slug']}` then `match: {first_line}`</sub>",
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

    if sent_back:
        lines += [
            "## Cards the gate caught and the rewrite fixed",
            "",
            "These are the questions as first written. The gate objected, a rewrite pass "
            "replaced each one, and the replacement passed - so these are not in the app. "
            "They are here because the gate is on trial too: if its objections below look "
            "wrong, it is throwing away good work, and if they look right, it is earning "
            "its cost.",
            "",
        ]
        for card in sent_back:
            lines += [f"- **{card['slug']}** ({card['format']}): {card['prompt']}",
                      f"  - Gate said: {card['reason']}", ""]
    return "\n".join(lines)
