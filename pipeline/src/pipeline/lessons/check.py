"""Structural checks a lesson must pass before it is stored.

Every rule here exists because the first content pass shipped the opposite:
raw HTML, PDF ligatures, link tables, book chapters, and cards that referred
to text the reader never saw. A prompt asking nicely was not enough - the
card generator already said "no questions about the text itself" and the
drafts leaked anyway. So the rules are enforced, not requested.
"""

import re

# "the passage", "the reference solution": the reader cannot see any of it.
REFERS_TO_SOURCE = re.compile(
    r"\b(?:the|this|that|above|below)\s+"
    r"(?:passage|excerpt|snippet|chapter|article|document|extract|"
    r"reference\s+solution|given\s+solution|source\s+material)\b"
    # "the section of memory" is ordinary English; "this section covers" is not.
    r"|\b(?:this|the)\s+(?:section|text)\s+(?:covers|describes|explains|shows|above|below)\b"
    r"|\b(?:as|which)\s+(?:the\s+)?(?:author|text|passage|article)\s+"
    r"(?:states|says|notes|mentions|explains|writes)\b"
    r"|\baccording\s+to\s+the\s+(?:passage|text|author|article|section|chapter)\b"
    # The lesson talking about itself: "according to this lesson" turns a
    # practice question into a reading-comprehension question.
    r"|\b(?:this|the)\s+(?:lesson|write-?up|explainer)\b"
    r"|\baccording\s+to\s+this\b",
    re.IGNORECASE,
)
HTML_TAG = re.compile(r"<(?:/?[a-zA-Z][a-zA-Z0-9]*)(?:\s[^<>]*)?/?>")
LIGATURE = re.compile(r"[ﬀ-ﬆ]")  # ﬀ ﬁ ﬂ ﬃ ﬄ ﬅ from bad PDF extraction
URL = re.compile(r"https?://|\]\(")
PIPE_TABLE = re.compile(r"^\s*\|.*\|\s*$", re.MULTILINE)
# "cat  ching" and "infor- mally": PDF text extraction splitting words.
BROKEN_WORD = re.compile(r"\b[a-z]{2,}-\s+[a-z]{2,}\b")

MIN_WORDS = 250
MAX_WORDS = 1400

# An interviewer's follow-up is often an instruction, not a question:
# "Walk me through the TLS handshake." is exactly what gets asked.
IMPERATIVE = re.compile(
    r"^(walk|explain|describe|compare|contrast|design|sketch|derive|show|"
    r"tell|give|name|estimate|trace|implement|justify|defend)\b",
    re.IGNORECASE,
)


def is_interviewer_prompt(text: str) -> bool:
    text = text.strip()
    return text.endswith("?") or bool(IMPERATIVE.match(text))


def word_count(text: str) -> int:
    return len(text.split())


def check(body_md: str, follow_ups: list[str]) -> list[str]:
    """Returns the reasons this lesson is not publishable. Empty means it is."""
    problems: list[str] = []
    words = word_count(body_md)
    if words < MIN_WORDS:
        problems.append(f"too short ({words} words, minimum {MIN_WORDS})")
    if words > MAX_WORDS:
        problems.append(f"too long ({words} words, maximum {MAX_WORDS})")
    if m := REFERS_TO_SOURCE.search(body_md):
        problems.append(f"refers to source the reader cannot see: {m.group(0)!r}")
    if m := HTML_TAG.search(body_md):
        problems.append(f"raw HTML: {m.group(0)!r}")
    if LIGATURE.search(body_md):
        problems.append("PDF ligature characters")
    if m := URL.search(body_md):
        problems.append(f"contains a link: {m.group(0)!r}")
    if PIPE_TABLE.search(body_md):
        problems.append("contains a table")
    if m := BROKEN_WORD.search(body_md):
        problems.append(f"word broken by PDF extraction: {m.group(0)!r}")
    bad_prompts = [q for q in follow_ups if not is_interviewer_prompt(q)]
    if bad_prompts:
        problems.append(f"follow-up is not something an interviewer would say: {bad_prompts[0]!r}")
    return problems
