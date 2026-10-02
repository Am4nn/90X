"""Final, free validation before a card reaches the reviewer or /admin/cards.

Two deterministic passes, no model calls, run after generation and gating:

1. Cross-topic dedupe. The per-topic dedupe never compares a card in one topic
   with a card in another, so the same question asked in two topics survives.
   This dedupes the whole draft corpus at once, keeping the card from the
   highest-importance topic.

2. Answer-definition consistency. The reader is graded by a pure function
   against `picked` / `constraints` / `pairs` / `value` / `why_step.correct`.
   An index out of range means the reader and the grader disagree, and no
   model check catches that.
"""

import json

from rapidfuzz import fuzz

from .archetypes import options_shape_of, shape_of
from .check import _norm


def _json(value):
    if value is None or value == "":
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None
    return value


def _index_range(n: int) -> str:
    return f"(0..{max(n - 1, 0)})"


def answer_problems(card: dict) -> list[str]:
    """The reasons a card's answer definition is inconsistent with its options.

    The option encoding is the registry's `optionsShape` (`list`, `match`,
    `bucket`, `assemble`, `grid`), so the indices are resolved against the
    correct list — a dict's `left`/`right`, `items`/`columns`, `tokens`, or
    `rows`×`columns` — rather than against the raw dict itself.
    """
    fmt = card["format"]
    shape = shape_of(fmt)
    opt_shape = options_shape_of(fmt)
    options = _json(card["options"])
    problems: list[str] = []

    if shape == "chosen":
        picked = _json(card["picked"]) or []
        if opt_shape == "grid":
            rows = (options or {}).get("rows") or []
            cols = (options or {}).get("columns") or []
            n = len(rows) * len(cols)
        else:
            n = len(options) if isinstance(options, list) else 0
        for i in picked:
            if not isinstance(i, int) or not (0 <= i < n):
                problems.append(f"picked index {i!r} out of range {_index_range(n)}")

    elif shape == "ordered":
        constraints = _json(card["constraints"]) or {}
        before = constraints.get("before") or []
        if opt_shape == "assemble":
            n = len((options or {}).get("tokens") or []) if isinstance(options, dict) else 0
        else:
            n = len(options) if isinstance(options, list) else 0
        for pair in before:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                for i in pair:
                    if not isinstance(i, int) or not (0 <= i < n):
                        problems.append(f"constraint index {i!r} out of range {_index_range(n)}")

    elif shape == "mapping":
        pairs = _json(card["pairs"]) or []
        if opt_shape == "list":
            # claim_grid: options is a flat list of statements; a pair is
            # [statement index, 0/1] (false/true), not two indices.
            left = options if isinstance(options, list) else []
            right = [0, 1]
        elif opt_shape == "match":
            left = (options or {}).get("left") or []
            right = (options or {}).get("right") or []
        elif opt_shape == "bucket":
            left = (options or {}).get("items") or []
            right = (options or {}).get("columns") or []
        else:
            left = right = []
        for pair in pairs:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                l, r = pair
                if not isinstance(l, int) or not (0 <= l < len(left)):
                    problems.append(f"pair left index {l!r} out of range {_index_range(len(left))}")
                if not isinstance(r, int) or not (0 <= r < len(right)):
                    problems.append(f"pair right index {r!r} out of range {_index_range(len(right))}")

    elif shape == "number":
        if card["value"] is None or card["tolerance"] is None:
            problems.append("numeric card is missing value or tolerance")

    why = _json(card["why_step"])
    if isinstance(why, dict):
        opts = why.get("options") or []
        correct = why.get("correct")
        if correct is None:
            problems.append("why-step is missing a correct index")
        elif not isinstance(correct, int) or not (0 <= correct < len(opts)):
            problems.append(f"why-step correct index {correct!r} out of range {_index_range(len(opts))}")

    return problems


def consistency(con) -> dict[str, list[str]]:
    """Every draft card whose answer definition is inconsistent, id -> problems."""
    rows = con.execute(
        """select id, format, options, picked, constraints, pairs, value, tolerance, why_step
           from cards where source = 'lesson' and status = 'draft'"""
    ).fetchall()
    cols = ["id", "format", "options", "picked", "constraints", "pairs", "value", "tolerance", "why_step"]
    out: dict[str, list[str]] = {}
    for r in rows:
        card = dict(zip(cols, r))
        problems = answer_problems(card)
        if problems:
            out[card["id"]] = problems
    return out


def cross_topic_dupes(con, threshold: int = 90) -> list[tuple[str, str]]:
    """Near-duplicate draft cards across topics, as (keep_id, dupe_id) pairs.

    Cards are visited in descending topic importance, so the card from the more
    important topic is the one kept. The `keep_id` side is empty for the very
    first card of a duplicate cluster only in the abstract; here every returned
    dupe names the kept card that absorbed it.
    """
    rows = con.execute(
        """select c.id, c.prompt_md, c.options from cards c
           join topics t on t.slug = c.topic_slug
           where c.source = 'lesson' and c.status = 'draft'
           order by t.importance desc, c.id"""
    ).fetchall()
    # Compared on prompt AND content. On the prompt alone every claim-grid card
    # matched every other at 100%, because their prompt is boilerplate - "Mark each
    # statement as true or false." - and the question itself lives in `options`. That
    # reported 239 near-duplicate pairs, of which a Java collections card and a
    # segment-tree card were one: not duplicates at all, just a shared stem. Acting
    # on that measurement would have deleted good, distinct cards.
    cards = [{"id": r[0], "prompt": _comparable(r[1], r[2])} for r in rows]

    # Same greedy first-wins dedupe as check.dedupe, but we record the pairs
    # rather than just the survivors.
    kept: list[dict] = []
    dupes: list[tuple[str, str]] = []
    for c in cards:
        for k in kept:
            if fuzz.token_sort_ratio(_norm(c["prompt"]), _norm(k["prompt"])) >= threshold:
                dupes.append((k["id"], c["id"]))
                break
        else:
            kept.append(c)
    return dupes


def report(con) -> str:
    """A printable summary: the consistency failures and the cross-topic dupes."""
    problems = consistency(con)
    dupes = cross_topic_dupes(con)
    lines = [
        f"{len(problems)} cards have an inconsistent answer definition; "
        f"{len(dupes)} near-duplicate pairs across topics.",
        "",
    ]
    for card_id, issues in sorted(problems.items()):
        lines.append(f"- {card_id}: " + "; ".join(issues))
    if dupes:
        lines.append("")
        lines.append("Cross-topic near-duplicates (kept <- dupe):")
        for keep_id, dupe_id in dupes:
            lines.append(f"- {keep_id} <- {dupe_id}")
    return "\n".join(lines)

def drop_dupes(con, threshold: int = 90, dry_run: bool = True) -> dict:
    """Reject the loser of every near-duplicate pair.

    `cross_topic_dupes` already decides which card to keep - the one from the
    more important topic - and this used to only print the pairs. 239 of them
    sat in a publishable corpus with nothing acting on them, which two reviewers
    independently named as the thing that would make the Feed feel repetitive.
    Detecting a problem and printing it is not fixing it.

    Free: the pairs come from embeddings already stored. A dropped card is
    rejected with its reason and the id of the card that absorbed it, so the
    decision stays auditable and reversible.
    """
    pairs = cross_topic_dupes(con, threshold=threshold)
    # One card can lose to several keepers; reject it once, naming the first.
    losers: dict[str, str] = {}
    for keep_id, dupe_id in pairs:
        losers.setdefault(dupe_id, keep_id)
    # Never drop a card that is itself a keeper for something else: that would
    # remove both halves of a pair and lose the question entirely.
    keepers = {keep_id for keep_id, _ in pairs}
    dropping = {d: k for d, k in losers.items() if d not in keepers}
    if not dry_run and dropping:
        con.executemany(
            """update cards set status = 'rejected', kept = false,
                      reject_reason = ? where id = ? and status = 'draft'
            """,
            [[f"near-duplicate of {keep}", dupe] for dupe, keep in dropping.items()],
        )
    return {
        "pairs": len(pairs),
        "dropped": len(dropping),
        "kept_as_keeper": len(losers) - len(dropping),
        "dry_run": dry_run,
    }

def _comparable(prompt: str, options) -> str:
    """What makes a card distinct: its prompt plus the content it shows.

    A generic stem is not the question. A claim grid asks its question through the
    statements in `options`, a bucket through its items, a match through its two
    sides - so those go into the comparison, or two unrelated cards that happen to
    share an instruction read as identical.
    """
    parts = [prompt or ""]
    parsed = _json(options)
    if isinstance(parsed, list):
        parts += [str(x) for x in parsed]
    elif isinstance(parsed, dict):
        for key in ("left", "right", "items", "columns", "rows", "tokens"):
            value = parsed.get(key)
            if isinstance(value, list):
                parts += [str(x) for x in value]
    return " ".join(parts)
