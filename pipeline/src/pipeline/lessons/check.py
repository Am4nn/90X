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
    r"(?:passage|excerpt|snippet|chapter|article|extract|"
    r"reference\s+solution|given\s+solution|source\s+material)\b"
    # "the section of memory" is ordinary English; "this section covers" is not.
    # "the document store" is the entire subject of sd-nosql-types, which the
    # bare noun rejected - the same mistake as reading List<Integer> as markup.
    r"|\b(?:this|the)\s+(?:section|text|document)\s+(?:covers|describes|explains|shows|above|below)\b"
    r"|\b(?:as|which)\s+(?:the\s+)?(?:author|text|passage|article|document)\s+"
    r"(?:states|says|notes|mentions|explains|writes)\b"
    r"|\baccording\s+to\s+the\s+(?:passage|text|author|article|section|chapter|document)\b"
    # The lesson talking about itself: "according to this lesson" turns a
    # practice question into a reading-comprehension question.
    r"|\b(?:this|the)\s+(?:lesson|write-?up|explainer)\b"
    r"|\baccording\s+to\s+this\b",
    re.IGNORECASE,
)
# Only real HTML tag names. Matching any <word> read Java generics as markup
# and failed a lesson for writing List<Integer>, which is how you write Java.
HTML_TAG = re.compile(
    r"</?(?:div|span|p|a|img|br|hr|table|thead|tbody|tr|td|th|ul|ol|li|h[1-6]|b|i|u|"
    r"strong|em|code|pre|blockquote|section|article|nav|header|footer|main|aside|"
    r"form|input|label|button|select|option|script|style|link|meta|iframe|svg|path|"
    r"figure|figcaption|details|summary|font|center|small|sup|sub)\b[^<>]*>",
    re.IGNORECASE,
)
CODE = re.compile(r"```.*?```|`[^`]+`", re.DOTALL)
MARKDOWN_LINK = re.compile(r"\]\(")
# A reference list is URLs standing alone on their own lines. Counting URLs
# instead failed the URL shortener lesson three times for writing URLs, which
# is the entire subject. Inline examples are prose; a bare line is a citation.
REFERENCE_LINE = re.compile(r"^\s*[-*]?\s*<?https?://\S+>?\s*$", re.MULTILINE)


def without_code(text: str) -> str:
    """Code is where angle brackets and URLs legitimately live."""
    return CODE.sub(" ", text)
LIGATURE = re.compile(r"[ﬀ-ﬆ]")  # ﬀ ﬁ ﬂ ﬃ ﬄ ﬅ from bad PDF extraction
URL = re.compile(r"https?://|\]\(")
PIPE_TABLE = re.compile(r"^\s*\|.*\|\s*$", re.MULTILINE)
# "cat  ching" and "infor- mally": PDF text extraction splitting words.
BROKEN_WORD = re.compile(r"\b[a-z]{2,}-\s+([a-z]{3,})\b")
# "pre- and post-conditions" is ordinary English; "infor- mally" is a PDF break.
CONNECTIVES = {"and", "but", "for", "nor", "the", "then", "with", "not", "yet", "plus", "versus", "post", "pre"}

MIN_WORDS = 250
MAX_WORDS = 1400

# An interviewer's follow-up is often an instruction, not a question:
# "Walk me through the TLS handshake." is exactly what gets asked.
IMPERATIVE = re.compile(
    r"^(walk|explain|describe|compare|contrast|design|sketch|derive|show|"
    r"tell|give|name|estimate|trace|implement|justify|defend|use|outline|"
    r"list|propose|argue|critique|identify|rank|prove|quantify|evaluate|"
    r"state|write)\b",
    re.IGNORECASE,
)


def is_interviewer_prompt(text: str) -> bool:
    """True if it sets up and then asks, and never answers itself.

    Testing only the whole string rejected "Can a table violate both 2NF and
    3NF at the same time? Give an example." - a question and then an
    instruction, which is how people actually talk, and it cost a correct
    lesson a full rewrite.

    Requiring every sentence to be a prompt then overshot the other way. It
    rejected "Your team has a method with a long chain of instanceof checks.
    How would you refactor it?" - a line of setup and then the ask, which is
    how interviewers talk far more often than they open with the question.

    So the shape is setup, then asking: statements may lead, and once a
    sentence prompts, every sentence after it must prompt too. The whole field
    is rendered as what the interviewer says, and the thing that must never
    happen is answering it in place - "What breaks under load? The lock
    serializes every request." hands the reader the answer beside the question.
    A statement before any prompt cannot do that: there is nothing yet to
    answer.
    """
    parts = [p.strip() for p in re.split(r"(?<=[.?!])\s+", text.strip()) if p.strip()]
    prompts = [p.endswith("?") or bool(IMPERATIVE.match(p)) for p in parts]
    if not any(prompts):
        return False
    return all(prompts[prompts.index(True) :])


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
    prose = without_code(body_md)
    if m := HTML_TAG.search(prose):
        problems.append(f"raw HTML: {m.group(0)!r}")
    if LIGATURE.search(body_md):
        problems.append("PDF ligature characters")
    if m := MARKDOWN_LINK.search(prose):
        problems.append(f"contains a link: {m.group(0)!r}")
    if REFERENCE_LINE.search(prose):
        problems.append("reads like a list of references, not a lesson")
    if PIPE_TABLE.search(body_md):
        problems.append("contains a table")
    broken = next((m for m in BROKEN_WORD.finditer(body_md) if m.group(1) not in CONNECTIVES), None)
    if broken:
        problems.append(f"word broken by PDF extraction: {broken.group(0)!r}")
    bad_prompts = [q for q in follow_ups if not is_interviewer_prompt(q)]
    if bad_prompts:
        problems.append(f"follow-up is not something an interviewer would say: {bad_prompts[0]!r}")
    return problems
