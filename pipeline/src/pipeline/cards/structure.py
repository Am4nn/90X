"""The free structural rules: catch elimination by shape before any model call.

The blind gate shows a model the answer choices and asks it to guess. But the
most common giveaway is one the model cannot see from inside a single option
set: an option that is the only number among prose, the only code block, three
lines longer than the rest, or a lazy "all of the above". A reader eliminates
by shape rather than by thinking, and no amount of reasoning catches it because
there was no reasoning to catch.

These run in code, before the reviewer and the blind gate, and cost nothing.
They add rejections the repair pass fixes, so a structurally guessable card is
rewritten with genuinely competitive options rather than shipped.
"""

import re

# "all of the above" / "none of the above", with or without a trailing full stop.
ALL_OR_NONE = re.compile(r"^\s*(?:all|none)\s+of\s+the\s+above\s*[.!]?\s*$", re.IGNORECASE)

# An option that is nothing but a number: the one numeric answer among prose.
BARE_NUMBER = re.compile(r"^[-+]?(?:\d+(?:\.\d*)?|\.\d+)\s*%?\s*$")

# An option that carries code: a fenced block or an inline backtick span.
CODE = re.compile(r"```|`[^`\n]+`")

# An option more than this many times the median length is out of band. Three
# is "absurdly longer", matching the plan's wording, and never fires on the
# normal spread of option lengths.
LENGTH_BAND = 3.0


def _all_or_none(options: list[str]) -> str | None:
    for option in options:
        if ALL_OR_NONE.match(option.strip()):
            return f"an option is {option.strip()!r}"
    return None


def _sole_of_kind(options: list[str]) -> str | None:
    """The one number, the one code block: a kind with a single member lets a
    reader eliminate it (or be drawn to it) without reading the rest."""
    numbers = [o for o in options if BARE_NUMBER.match(o.strip())]
    if len(numbers) == 1:
        return f"one option is the only bare number: {numbers[0].strip()!r}"
    code = [o for o in options if CODE.search(o)]
    if len(code) == 1:
        return f"one option is the only one carrying code: {code[0].strip()!r}"
    return None


def _length_outlier(options: list[str]) -> str | None:
    """An option far longer or shorter than the rest gives itself away by size."""
    if len(options) < 2:
        return None
    lengths = [len(o.strip()) for o in options]
    median = sorted(lengths)[len(lengths) // 2]
    if median < 1:
        return None
    for option, n in zip(options, lengths):
        if n > median * LENGTH_BAND or n * LENGTH_BAND < median:
            side = "longer" if n > median else "shorter"
            return f"an option is far {side} than the rest: {option.strip()!r}"
    return None


_CHECKS = (_all_or_none, _sole_of_kind, _length_outlier)


def problems(card) -> list[str]:
    """The structural reasons a card is guessable by shape. Empty means it is not.

    A card with no option list (typed, flash, order, numeric, ...) has no options
    to eliminate by shape and is not checked.
    """
    options = getattr(card, "options", None) or []
    if not options:
        return []
    return [msg for check in _CHECKS if (msg := check(options))]
