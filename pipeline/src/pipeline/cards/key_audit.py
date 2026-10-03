"""Does a card's answer key say what its own explanation says?

Nothing checked. The gate answers a card "blind" and compares its pick with the key,
but only for the legacy `mcq` format (`gate.judge` guards it with `card.format ==
"mcq"`, the same guard that once hid every primitive's options from the gate). For
`pick_one` and every other primitive the key was written by the model that wrote the
question, passed `wellformed` (which asks only whether a key is *well formed*, not
whether it is *right*), and shipped.

A key and an explanation are written together, so they should agree, and a flash card
whose key contradicts its explanation is the worst defect there is: the reader is
marked wrong for knowing the answer. A repaired grid showed it plainly - ticked
"interface inheritance inherits implementation" under an explanation that says the
opposite - and rebuilding its original from the archive showed the original already
disagreed with its prose before any repair touched it.

This renders each key as plain sentences, which is the part that was invisible: a grid
stores flat cell indices, an order stores rules, an assemble stores constraints over
tokens. A reviewer cannot compare `[0, 1, 4, 5, 8, 11]` with a paragraph. It can
compare "Interface inheritance: ticked Inherits implementation".

The verdict is three-valued on purpose. An explanation that is silent about part of a
key is not a contradiction, and rejecting on silence would throw away good cards. Only
`contradicts` counts, and the caller should want two independent passes to say so.
"""

import json
from typing import Literal

from pydantic import BaseModel, Field

from . import archetypes, gate


def _load(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return None
    return value


def _pairs(value) -> list[list[int]] | None:
    """`constraints` arrives wrapped as {"before": [...]}; `pairs` arrives flat."""
    value = _load(value)
    if isinstance(value, dict):
        value = value.get("before")
    if not isinstance(value, list):
        return None
    out = []
    for item in value:
        if not (isinstance(item, (list, tuple)) and len(item) == 2):
            return None
        if not all(isinstance(n, int) and not isinstance(n, bool) for n in item):
            return None
        out.append([int(item[0]), int(item[1])])
    return out


def _ints(value) -> list[int] | None:
    value = _load(value)
    if not isinstance(value, list) or not all(isinstance(n, int) and not isinstance(n, bool) for n in value):
        return None
    return [int(n) for n in value]


def _at(items: list, index: int) -> str | None:
    return str(items[index]) if isinstance(index, int) and 0 <= index < len(items) else None


def _sequence(count: int, before: list[list[int]]) -> list[int] | None:
    """The one order the rules allow, or None if there is not exactly one.

    Kahn's algorithm, refusing to guess: if two items are ready at once the rules do
    not fix their order, and an assemble card whose line is not fixed is not a card we
    can read a sentence off.
    """
    incoming = {i: 0 for i in range(count)}
    after: dict[int, list[int]] = {i: [] for i in range(count)}
    for a, b in before:
        if a not in incoming or b not in incoming:
            return None
        after[a].append(b)
        incoming[b] += 1
    ready = [i for i, n in incoming.items() if n == 0]
    out: list[int] = []
    while ready:
        if len(ready) > 1:
            return None
        node = ready.pop()
        out.append(node)
        for nxt in after[node]:
            incoming[nxt] -= 1
            if incoming[nxt] == 0:
                ready.append(nxt)
    return out if len(out) == count else None


def key_text(card) -> list[str] | None:
    """The card's answer key as plain sentences.

    None when the primitive has no stored key (`self_rate` is marked by the reader,
    `compose` by a model). An empty list would mean "a key that says nothing", which is
    itself a defect, so an unreadable key comes back as a line saying so rather than as
    silence the audit could mistake for agreement.
    """
    primitive = getattr(card, "format", None)
    if primitive in (None, "self_rate", "compose"):
        return None
    options = _load(getattr(card, "options", None))
    unreadable = ["The stored answer key could not be read."]
    lines: list[str] = []

    if primitive in ("pick_one", "tap_in_place"):
        picked = _ints(getattr(card, "picked", None))
        if not isinstance(options, list) or not picked:
            return unreadable
        for i in picked:
            text = _at(options, i)
            if text is None:
                return unreadable
            if primitive == "tap_in_place":
                # "Marked correct" read as "this line is correct code", so a card whose
                # key is the BUG line and whose explanation calls that line the bug looked
                # like a contradiction. The line is the answer, not an endorsement.
                lines.append(f"The line the reader must tap to be right (the answer itself): {text}")
            else:
                lines.append(f"Marked correct: {text}")

    elif primitive == "grid_toggle":
        picked = _ints(getattr(card, "picked", None))
        if not (isinstance(options, dict) and isinstance(options.get("rows"), list)
                and isinstance(options.get("columns"), list)) or picked is None:
            return unreadable
        rows, cols = options["rows"], options["columns"]
        # Nothing ticked, or no rows or columns to tick, is not a key. Reading it as
        # "row: ticked nothing" lines would give the auditor something plausible to agree with.
        if not rows or not cols or not picked:
            return unreadable
        if any(not 0 <= i < len(rows) * len(cols) for i in picked):
            return unreadable
        for r, row in enumerate(rows):
            ticked = [str(cols[i % len(cols)]) for i in picked if i // len(cols) == r]
            lines.append(f"{row}: ticked {', '.join(ticked) if ticked else 'nothing'}")

    elif primitive == "claim_grid":
        verdicts = _pairs(getattr(card, "pairs", None))
        if not isinstance(options, list) or verdicts is None:
            return unreadable
        for i, v in verdicts:
            text = _at(options, i)
            if text is None or v not in (0, 1):
                return unreadable
            lines.append(f"{'TRUE' if v else 'FALSE'}: {text}")

    elif primitive == "match":
        pairs = _pairs(getattr(card, "pairs", None))
        if not (isinstance(options, dict) and isinstance(options.get("left"), list)
                and isinstance(options.get("right"), list)) or pairs is None:
            return unreadable
        for a, b in pairs:
            left, right = _at(options["left"], a), _at(options["right"], b)
            if left is None or right is None:
                return unreadable
            lines.append(f"{left} -> {right}")

    elif primitive == "bucket":
        pairs = _pairs(getattr(card, "pairs", None))
        if not (isinstance(options, dict) and isinstance(options.get("items"), list)
                and isinstance(options.get("columns"), list)) or pairs is None:
            return unreadable
        for a, b in pairs:
            item, column = _at(options["items"], a), _at(options["columns"], b)
            if item is None or column is None:
                return unreadable
            lines.append(f"{item} -> {column}")

    elif primitive == "order":
        rules = _pairs(getattr(card, "constraints", None))
        if not isinstance(options, list) or rules is None:
            return unreadable
        for a, b in rules:
            first, second = _at(options, a), _at(options, b)
            if first is None or second is None:
                return unreadable
            lines.append(f"'{first}' must come before '{second}'")

    elif primitive == "assemble":
        rules = _pairs(getattr(card, "constraints", None))
        tokens = options.get("tokens") if isinstance(options, dict) else None
        if not isinstance(tokens, list) or rules is None:
            return unreadable
        order = _sequence(len(tokens), rules)
        if order is None:
            return unreadable
        lines.append("The line built is: " + " ".join(str(tokens[i]) for i in order))

    elif primitive == "numeric":
        value = getattr(card, "value", None)
        if value is None:
            return unreadable
        tolerance = getattr(card, "tolerance", None)
        lines.append(f"Expected value: {value}" + (f" (accepted within {tolerance})" if tolerance else ""))

    else:
        return None

    why = _load(getattr(card, "why_step", None))
    if isinstance(why, dict) and isinstance(why.get("options"), list):
        reason = _at(why["options"], why.get("correct"))
        if reason is not None:
            lines.append(f"Reason marked correct (second question): {reason}")
    return lines


class KeyVerdict(BaseModel):
    index: int = Field(description="the card's position in the list, starting at 0")
    # Required, no default. An omitted verdict must be a schema error that gets the
    # request retried, not a quiet "agrees".
    verdict: Literal["agrees", "contradicts", "unclear"] = Field(
        description="whether the explanation agrees with the marked answer key"
    )
    reason: str = Field(default="", description="when it contradicts: which part of the key, and what the explanation says instead")


class KeyAudit(BaseModel):
    verdicts: list[KeyVerdict]


SYSTEM = """You check study cards for one defect: an answer key that contradicts the card's own explanation.

For each card you get the question, what it puts on screen, the explanation shown to the reader after they answer, and the answer key the card will be marked against, written out as plain sentences.

Set `verdict` to:
- "contradicts" when the key marks something the explanation says is wrong, or leaves out or marks wrongly something the explanation says is right. Name the part of the key and what the explanation says instead.
- "agrees" when the key is what the explanation describes.
- "unclear" when the explanation does not say enough to tell, or you cannot work out what the key is claiming.

Be careful with the difference between contradicting and being silent. An explanation that says nothing about part of the key does not contradict it, so that part is "agrees" or "unclear", never "contradicts". Judge only the match between key and explanation. Do not judge whether the question is good, whether the explanation is correct in the real world, or how hard the card is.

How to read each kind of key, because most wrong "contradicts" verdicts come from misreading the key's shape:
- A line the reader must tap (a bug, a bottleneck, an insertion point) IS the answer. It is supposed to be the line the explanation calls the problem, so they agree when the explanation points at that same line. Do not read it as an endorsement that the line is good code.
- A rebuilt line joins the tokens with single spaces for display only. Ignore spacing and the spacing around punctuation or operators: `-XX: MaxMetaspaceSize = 256m` and `-XX:MaxMetaspaceSize=256m` are the same. Compare the words and their order, and whether any token is missing.
- A number may be written by the explanation in other terms: an exponent, a count, a ratio, a complexity class. It agrees if they mean the same thing, so a key of `2.0` agrees with "O(n^2)" when the question asks for the exponent.
- A grid lists, row by row, the columns ticked. Compare each row with what the explanation says about that row.
- An explanation that numbers statements ("statements 1 and 3 are true") may be numbered differently from the key's order. Compare by the statement's content, not its number, and say "unclear" if you cannot match them.

Say "contradicts" only when you can name a specific claim in the explanation that is incompatible with a specific part of the key. When you are unsure, say "unclear". Judge the key against the explanation only, never against your own knowledge of the subject.

Reply with JSON only: {"verdicts":[{"index":0,"verdict":"agrees","reason":""}]}, one entry per card, using the card's number as `index`."""


def prompt_for(card) -> str:
    """One card as the auditor sees it: content, explanation, and the key in words."""
    key = key_text(card)
    shown = gate._shown(card)
    parts = [f"format: {card.format}", f"question: {card.prompt}"]
    parts += shown
    parts.append("answer key:")
    parts += [f"  {line}" for line in (key or [])]
    parts.append("explanation shown after answering:")
    parts.append(f"  {(getattr(card, 'answer', None) or getattr(card, 'answer_md', '') or '').strip()}")
    return "\n".join(parts)


def audit(llm, topic: dict, cards: list, tier: str = "fast") -> KeyAudit:
    body = "\n\n".join(f"[{i}]\n{prompt_for(c)}" for i, c in enumerate(cards))
    user = f"Topic: {topic['name']}\n\n{body}"
    return llm.complete_json(SYSTEM, user, KeyAudit, tier=tier, purpose="key-audit")


def contradictions(cards: list, result: KeyAudit) -> dict[int, str]:
    """Card position -> the reviewer's reason, for each card judged to contradict.

    A card the reviewer did not mention is not in the result, and silence is not
    agreement, but it is not a contradiction either: the caller decides what to do
    with unmentioned cards, this reports only what was actually claimed.
    """
    return {
        v.index: v.reason or "the key contradicts the explanation"
        for v in result.verdicts
        if v.verdict == "contradicts" and 0 <= v.index < len(cards)
    }


def has_key(card) -> bool:
    """Whether there is a key to audit, so callers can skip self_rate and compose."""
    return key_text(card) is not None and archetypes.options_shape_of(card.format) is not None
