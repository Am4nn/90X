"""Assemble the source material for one topic's lesson.

Two hard cases decide the design. `cs-http-https` has 162 documents and
179K characters, far more than a prompt can hold, so documents are ranked by
how well they match the topic and each is truncated. `beh-teamwork` has none at
all - and a lesson with no material is not written, because `run.NoSource`
refuses rather than letting the model answer from memory. So the job here is to
find everything we actually downloaded that bears on a topic, which for a while
meant only the documents somebody had mapped to it.
"""

import re
from functools import lru_cache
from pathlib import Path

from ..config import DATA_DIR

ROADMAP_DIR = DATA_DIR / "system_design" / "roadmap-sh" / "roadmaps"

MAX_CHARS = 14_000
MAX_DOCS = 8
MAX_DOC_CHARS = 2_500
MAX_ROADMAP_NODES = 4
# Problem statements, for a DSA pattern. Shorter than a document because six of
# them should illustrate the pattern, not fill the whole prompt.
MAX_PROBLEMS = 6
MAX_PROBLEM_CHARS = 1_600
STOP = {"and", "or", "the", "a", "an", "of", "in", "to", "vs", "with", "for", "on"}


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 1}


@lru_cache(maxsize=1)
def roadmap_nodes() -> tuple[tuple[frozenset, Path], ...]:
    """Every roadmap.sh node as (title words, path). Each file is one node:
    a title, a short authoritative definition, then links we drop."""
    nodes = []
    for path in ROADMAP_DIR.glob("*/content/*.md"):
        title = path.stem.split("@")[0].replace("-", " ")
        nodes.append((frozenset(words(title)), path))
    return tuple(nodes)


def node_text(path: Path) -> str:
    """A node without its 'Visit the following resources' link list."""
    text = path.read_text(encoding="utf-8", errors="replace")
    return re.split(r"\n\s*(?:Visit the following resources|Learn more from the following)", text)[0].strip()


def rank(candidates: list[tuple[frozenset, object]], target: set[str]) -> list[object]:
    """Best overlap with the topic name first; ties broken by tighter match."""
    scored = []
    for keys, item in candidates:
        hit = len(keys & target)
        if hit:
            scored.append((hit, hit / len(keys or {1}), item))
    scored.sort(key=lambda s: (-s[0], -s[1]))
    return [item for _, _, item in scored]


def for_topic(
    topic: dict,
    documents: list[dict],
    spare: list[dict] | None = None,
    problems: list[dict] | None = None,
) -> tuple[str, list[str]]:
    """Returns the prompt context and the source ids that went into it.

    Four kinds of material, in the order they earn their place:

    1. Roadmap notes - short, clean and authoritative, so they anchor the lesson
       even when the scraped material around them is a mess.
    2. Documents assigned to this topic. Somebody mapped them on purpose.
    3. For a DSA pattern, the statements of the problems in it. These are the
       best material we hold for a pattern and no lesson read one until now:
       `sliding-window` was written from a single roadmap paragraph while 150
       real problem statements sat in the same database.
    4. Documents assigned to no topic at all, when the name overlaps. 2,346 of
       5,290 downloaded documents have no topic, so nearly half the corpus was
       invisible to every lesson. `rank` returns only what overlaps, so nothing
       lands here by coincidence.
    """
    target = words(topic["name"]) | words(topic.get("description") or "")
    parts: list[str] = []
    refs: list[str] = []

    for path in rank([(k, p) for k, p in roadmap_nodes()], target)[:MAX_ROADMAP_NODES]:
        parts.append(node_text(path))
        refs.append(f"roadmap-sh:{path.stem}")

    ranked = rank([(words(d["title"]), d) for d in documents], target)
    # A topic whose documents all miss the name still deserves its own material.
    chosen = (ranked or documents)[:MAX_DOCS]
    for doc in chosen:
        body = (doc["body_md"] or "").strip()
        parts.append(f"{doc['title']}\n{body[:MAX_DOC_CHARS]}")
        refs.append(doc["id"])

    for problem in (problems or [])[:MAX_PROBLEMS]:
        statement = (problem["statement_md"] or "").strip()
        if not statement:
            continue
        parts.append(f"Problem: {problem['title']} ({problem['difficulty']})\n{statement[:MAX_PROBLEM_CHARS]}")
        # Keyed by the problem's own source so `publish._sources_of` credits it;
        # a made-up prefix like "problem:" resolves to nothing and the reader's
        # "Written from" line silently loses the source.
        refs.append(f"{problem['source_id']}:{problem['slug']}")

    # Only ever filler: no fallback to unranked, so a topic with nothing
    # overlapping gets nothing rather than something arbitrary.
    for doc in rank([(words(d["title"]), d) for d in (spare or [])], target)[: MAX_DOCS - len(chosen)]:
        body = (doc["body_md"] or "").strip()
        parts.append(f"{doc['title']}\n{body[:MAX_DOC_CHARS]}")
        refs.append(doc["id"])

    context, used = "", 0
    for part in parts:
        if len(context) + len(part) > MAX_CHARS:
            break
        context += part + "\n\n---\n\n"
        used += 1
    # Count the parts we kept. Splitting on "---" also counts horizontal rules
    # inside a document body, which credited sources we never included.
    return context.strip(), refs[:used]
