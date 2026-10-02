"""The card sample Aman reads, and hands to an outside reviewer.

The review question is "does this archetype earn a place", not "is this card
correct" - the gates answer correctness. So the sample is **two cards per
archetype, grouped by archetype, not shuffled**: a reviewer judges a *kind* of
question, not 94 individual cards. 47 archetypes x 2 = 94.

Each card is shown with the answer definition the reader is judged against (the
correct indices, the ordering constraints, the mapping pairs, the number and its
tolerance, and the why-step with its distractors), so the owner can see whether
a wrong reason is genuinely plausible before the right-answer-wrong-reason rule
punishes a reader for a writing failure.

Every rejected card is listed too, with the gate's reason. The gate is as much
on trial as the cards.
"""

import json

from . import archetypes

# 47 archetypes, two each. A flat 100 would over-represent pick-one (20 of 47)
# and under-represent the new primitives, which is the bias the review exists to
# catch.
PER_ARCHETYPE = 2
SAMPLE = PER_ARCHETYPE * len(archetypes.registry().archetypes)


def _json(value):
    """A jsonb column value as its Python form, or None. DuckDB stores jsonb as
    text, so the columns arrive as strings and the `??` columns as real None."""
    if value is None or value == "":
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None
    return value


def sample(con, size: int = SAMPLE) -> list[dict]:
    """Two cards per archetype, grouped by archetype, least-confident first.

    Grouping in Python rather than SQL: the registry is the order to read in,
    and taking the two least-confident cards per archetype is a per-group slice
    that SQL's window functions make harder to read than it is worth."""
    cols = [
        "id", "slug", "domain", "topic", "format", "difficulty", "prompt", "options",
        "answer", "key_points", "quality", "archetype", "picked", "constraints", "pairs",
        "value", "tolerance", "why_step", "lesson",
    ]
    rows = con.execute(
        """
        select c.id, c.topic_slug, t.domain, t.name, c.format, c.difficulty, c.prompt_md,
               c.options, c.answer_md, c.key_points, c.quality, c.archetype,
               c.picked, c.constraints, c.pairs, c.value, c.tolerance, c.why_step, l.body_md
        from cards c
        join topics t on t.slug = c.topic_slug
        join lessons l on l.topic_slug = c.topic_slug
        where c.source = 'lesson' and c.status = 'draft'
        order by coalesce(cast(json_extract(c.quality, '$.gate_confidence') as double), 0.5), c.id
        """
    ).fetchall()
    cards = [dict(zip(cols, r)) for r in rows]

    order = [a.id for a in archetypes.registry().archetypes]
    labels = {a.id: a.label for a in archetypes.registry().archetypes}
    by_archetype: dict[str, list[dict]] = {aid: [] for aid in order}
    for card in cards:
        aid = card["archetype"]
        if aid in by_archetype and len(by_archetype[aid]) < PER_ARCHETYPE:
            card["archetype_label"] = labels.get(aid, aid)
            by_archetype[aid].append(card)
    return [card for aid in order for card in by_archetype[aid]][:size]


def rejected(con, status: str = "rejected") -> list[dict]:
    rows = con.execute(
        """select topic_slug, format, prompt_md, reject_reason from cards
           where source = 'lesson' and status = ? and archetype is not null order by topic_slug""",
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


# --- Rendering the card the reviewer sees ------------------------------------

def _text(index, texts: list[str]) -> str:
    if texts and isinstance(index, int) and 0 <= index < len(texts):
        return texts[index]
    return str(index)


def _letter(index, texts: list[str]) -> str:
    if texts and isinstance(index, int) and 0 <= index < len(texts):
        return f"{chr(65 + index)}. {texts[index]}"
    return str(index)


def _flat_options(card) -> list[str]:
    """The option/item texts as a flat list, for resolving answer indices. The
    structured shapes (match/bucket/assemble/grid) store indices in separate
    spaces, so a flat list does not apply and the caller resolves per shape."""
    options = _json(card["options"])
    if isinstance(options, list):
        return [str(o) for o in options]
    return []


def _grid(card) -> tuple[list[str], list[str]]:
    options = _json(card["options"])
    if isinstance(options, dict):
        rows = [str(r) for r in (options.get("rows") or [])]
        columns = [str(c) for c in (options.get("columns") or [])]
        return rows, columns
    return [], []


def _options_lines(card) -> list[str]:
    """The card's options, in the reader's vocabulary: a lettered list for the
    list shapes, the two sides of a match, the items and columns of a bucket, the
    tokens and fixed slots of an assemble, or the rows and columns of a grid."""
    options = _json(card["options"])
    if isinstance(options, list):
        return [f"{chr(65 + i)}. {o}" for i, o in enumerate(options)]
    if isinstance(options, dict):
        lines = []
        for key, label in (
            ("left", "Left"),
            ("right", "Right"),
            ("items", "Items"),
            ("columns", "Columns"),
            ("tokens", "Tokens"),
            ("rows", "Rows"),
        ):
            value = options.get(key)
            if value:
                lines.append(f"**{label}**: " + ", ".join(str(x) for x in value))
        if options.get("fixed"):
            lines.append("**Fixed slots**: " + ", ".join("·" if x is None else str(x) for x in options["fixed"]))
        return lines
    return []


def _answer_lines(card) -> list[str]:
    """The answer definition the reader is graded against, in the reader's own
    vocabulary: the correct option(s), the ordering constraints, the mapping
    pairs, or the number and its tolerance."""
    fmt = card["format"]
    shape = archetypes.shape_of(fmt)
    texts = _flat_options(card)

    if shape == "chosen":
        picked = _json(card["picked"]) or []
        if fmt == "grid_toggle":
            rows, columns = _grid(card)
            cells = []
            for i in picked:
                if isinstance(i, int) and columns and 0 <= i < len(rows) * len(columns):
                    cells.append(f"{rows[i // len(columns)]} · {columns[i % len(columns)]}")
                else:
                    cells.append(str(i))
            return ["- Ticked: " + (", ".join(cells) if cells else "none")]
        shown = [_letter(i, texts) for i in picked if isinstance(i, int)]
        return ["- Correct: " + (", ".join(shown) if shown else "none")]

    if shape == "ordered":
        before = (_json(card["constraints"]) or {}).get("before") or []
        parts = []
        for pair in before:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                parts.append(f"{_text(pair[0], texts)} → {_text(pair[1], texts)}")
        return ["- before: " + (" · ".join(parts) if parts else "none")]

    if shape == "mapping":
        pairs = _json(card["pairs"]) or []
        parts = []
        for pair in pairs:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                left, right = pair
                if fmt == "claim_grid":
                    parts.append(f"{_text(left, texts)} → {'true' if right == 1 else 'false'}")
                else:
                    parts.append(f"{_text(left, texts)} ↔ {_text(right, texts)}")
        return ["- " + " · ".join(parts)] if parts else []

    if shape == "number":
        if card["value"] is not None and card["tolerance"] is not None:
            return [f"- {card['value']} ± {card['tolerance']}"]
        return []

    if fmt == "compose":
        # A written answer has no answer-shape column: what it is marked against
        # is `key_points`, one boolean per point. Those are shown under "Graded
        # on" like every other card's, but here they are the answer definition
        # rather than a summary of it, and the reviewer has to judge them as such
        # - an unanswerable requirement is this archetype's version of an
        # implausible distractor.
        points = _json(card["key_points"]) or []
        return ["- Marked against each of these, by a model, one at a time:"] + [
            f"  {i + 1}. {p}" for i, p in enumerate(points)
        ]

    return []


def _why_lines(card) -> list[str]:
    """The why-step, with the correct reason marked and the distractors shown
    plainly - the owner judges whether a wrong reason is plausible, so burying
    them in JSON would hide exactly the failure this review exists to catch."""
    why = _json(card["why_step"])
    if not isinstance(why, dict):
        return []
    options = [str(o) for o in (why.get("options") or [])]
    correct = why.get("correct")
    if not options:
        return []
    lines = ["**Why (right answer, wrong reason is wrong)**", ""]
    for i, option in enumerate(options):
        marker = "→ **" if i == correct else "  "
        suffix = "**" if i == correct else ""
        lines.append(f"{marker}{_letter(i, options)}{suffix}")
    return lines


def report(con) -> str:
    kept, dropped, fixed = con.execute(
        """select count(*) filter (where status = 'draft'),
                  count(*) filter (where status = 'rejected'),
                  count(*) filter (where status = 'repaired')
           from cards where source = 'lesson' and archetype is not null"""
    ).fetchone()
    mix = con.execute(
        """select format, count(*) from cards where source = 'lesson' and status = 'draft'
              and archetype is not null group by 1 order by 2 desc"""
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
        f"({dropped / max(1, seen):.0%}). Mix by answer screen: "
        + ", ".join(f"{n} {f}" for f, n in mix) + "."
        + ("" if fixed else "\n\n*No card here is recorded as caught-and-rewritten. Card runs before "
           "2026-09-28 did not keep that record, so on an older run the rewrite pass is invisible "
           "rather than idle, and the drop rate is the only measured number above.*"),
        "",
        "## What these are",
        "",
        # Counted from the registry rather than written down. The last version of
        # this paragraph said "47 archetypes over ten answer screens" while the
        # catalogue held 56 over 11.
        f"90x is an interview-prep app. The Feed is being rebuilt around {len(archetypes.registry().archetypes)} "
        f"question archetypes over {len(archetypes.registry().shapes)} answer screens (primitives). Every card "
        "names its archetype and its screen, and almost every answer is marked by a pure function "
        "against the answer definition shown below - no model, no typing. The one exception is the "
        "`compose` screen, used by behavioural cards only: the reader writes two or three sentences "
        "and a model marks them against the card's listed requirements, one at a time. A reader "
        "answers without the lesson in front of them.",
        "",
        "## What to judge",
        "",
        "The gates already checked whether each card is correct, guessable and well-formed. This "
        "review asks the one question the gates cannot: **does this archetype earn a place in the "
        "Feed?** Judge each *kind* of question, not each individual card. For each archetype below, "
        "ask:",
        "",
        "1. **Could a competent engineer who studied this topic answer it, with nothing else open?** "
        "A card that needs the lesson open is broken, however good it looks beside it.",
        "2. **Does the answer screen fit the question?** Order for sequences, match for pairs, a "
        "number for a calculation, tap for a point inside a snippet.",
        "3. **Are the why-step's wrong reasons plausible mistakes?** A right answer with an "
        "implausible reason is marked wrong, which punishes the reader for a writing failure.",
        "4. **On a `compose` card, could a short answer actually satisfy every requirement?** They "
        "are the rubric, graded one at a time, so a requirement nobody could meet in three sentences "
        "marks a good answer wrong - the same failure as an implausible distractor.",
        "5. **Was the gate right?** The rejected cards are at the end with its reasons.",
        "",
        f"Below: {len(picked)} cards, two per archetype, grouped by archetype so a *kind* of "
        "question can be judged as a whole. The two least-confident cards per archetype are shown, "
        "each with the lesson it came from and the answer definition the reader is graded against.",
        "",
        "---",
        "",
    ]

    last_archetype = None
    for i, card in enumerate(picked, 1):
        confidence = (json.loads(card["quality"] or "{}") or {}).get("gate_confidence")
        first_line = selector(con, card["slug"], card["prompt"])

        if card["archetype"] != last_archetype:
            lines += [
                f"## {card['archetype_label']} (`{card['archetype']}` · {card['format']})",
                "",
            ]
            last_archetype = card["archetype"]

        lines += [
            f"### {i}. {card['topic']} · {card['difficulty']}",
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
        options = _options_lines(card)
        if options:
            lines += ["**Options**", ""] + options + [""]
        answer = _answer_lines(card)
        if answer:
            lines += ["**Answer (the reader is graded on)**", ""] + answer + [""]
        why = _why_lines(card)
        if why:
            lines += why + [""]
        lines += [
            "**Reference answer**",
            "",
            card["answer"],
            "",
        ]
        # On a compose card the key points ARE the answer definition and were
        # already printed as such, so repeating them under a second heading just
        # pads a document the owner reads 112 cards of.
        if card["format"] != "compose":
            lines += ["**Graded on**", ""]
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
