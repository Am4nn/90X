"""Real interview questions with the follow-ups an interviewer probes with.

systemdesign.io publishes 55 system design questions asked in real interviews,
each with difficulty, company tags and - the valuable part - a list of
follow-ups ("How will you do this on a single machine first?"). It has no
solutions; the site says it is still writing them. So this is not lesson
material. It is evidence of what gets asked, and it grades a candidate's
depth, which is exactly what a lesson's follow-up ladder should be built on.

The pages are Tailwind with no semantic markup, so parsing anchors on the
marker sentence rather than on class names, which would break on any redesign.
"""

import html
import re
from pathlib import Path

from ..config import DATA_DIR

SOURCE_DIR = DATA_DIR / "system_design" / "systemdesign-io"
FOLLOW_UPS_MARKER = "details you should know about this question"
DIFFICULTIES = ("Very Easy", "Very Hard", "Easy", "Medium", "Hard")


def _text(fragment: str) -> str:
    fragment = re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", fragment))).strip()


def title_of(page: str) -> str:
    m = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", page)
    return _text(m.group(1)) if m else ""


def follow_ups(page: str) -> list[str]:
    """The probing questions, in the order the site lists them."""
    body = _text(page)
    i = body.lower().find(FOLLOW_UPS_MARKER)
    if i < 0:
        return []
    tail = body[i + len(FOLLOW_UPS_MARKER):]
    # Every follow-up is a question; anything after the last one is footer.
    return [q.strip() for q in re.findall(r"([A-Z][^?]{15,300}\?)", tail)]


def links(page: str) -> list[str]:
    """Where the site points for solutions: LeetCode discuss, talks, blogs."""
    return sorted({u for u in re.findall(r"https?://[^\s\"'<>]+", _text(page)) if "systemdesign.io" not in u})


def difficulty_by_slug(index_page: str) -> dict[str, str]:
    """Difficulty per question, read from its own table row.

    Matching difficulty words across the whole page and zipping them to the
    links silently shifts every answer: the complexity filter at the top of
    the page lists all five words before the table starts, so "Design an API
    Rate Limiter" came out Medium when the site says Hard. Read each row.
    """
    out: dict[str, str] = {}
    for row in re.split(r"(?i)<tr\b", index_page)[1:]:
        m = re.search(r'href="/question/([a-z0-9-]+)"', row)
        if not m:
            continue
        found = re.search("|".join(DIFFICULTIES), _text(row))
        if found:
            out.setdefault(m.group(1), found.group(0))
    return out


def parse_all(source_dir: Path = SOURCE_DIR) -> list[dict]:
    index = (source_dir / "_index.html").read_text(encoding="utf-8", errors="replace")
    levels = difficulty_by_slug(index)
    out = []
    for path in sorted(source_dir.glob("*.html")):
        if path.name == "_index.html":
            continue
        page = path.read_text(encoding="utf-8", errors="replace")
        slug = path.stem
        out.append({
            "id": f"systemdesign-io:{slug}",
            "slug": slug,
            "kind": "system_design",
            "title": title_of(page),
            "difficulty": levels.get(slug),
            "follow_ups": follow_ups(page),
            "links": links(page),
            "source_id": "systemdesign-io",
        })
    return out
