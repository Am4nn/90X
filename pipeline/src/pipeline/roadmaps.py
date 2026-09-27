"""Roadmap structure: the tree behind each roadmap.sh diagram.

The repo ships only node *content* (`roadmaps/<slug>/content/<name>@<id>.md`).
The shape - sections, topics, subtopics and the edges between them - comes
from `https://roadmap.sh/<slug>.json`, where each node id matches the `@<id>`
suffix on a content file. Joining the two gives a roadmap we can render with
our own lesson behind every node.
"""

import json
from pathlib import Path

import httpx

from .config import DATA_DIR

ROADMAP_DIR = DATA_DIR / "system_design" / "roadmap-sh"
STRUCTURE_DIR = ROADMAP_DIR / "structure"

# Which roadmap belongs in which 90x domain. A domain may show several.
DOMAIN_ROADMAPS: dict[str, tuple[str, ...]] = {
    "system_design": ("system-design", "software-architect", "api-design"),
    "cs": ("computer-science", "linux", "docker", "kubernetes", "devops"),
    "dsa": ("datastructures-and-algorithms",),
    "java": ("java", "spring-boot"),
    "sql": ("sql", "postgresql-dba"),
    "ai": ("ai-engineer", "machine-learning", "mlops", "prompt-engineering"),
    "lld": ("software-design-architecture",),
    "behavioral": ("engineering-manager",),
}

# Nodes that carry a lesson. The rest are layout: boxes, arrows, legends.
CONTENT_TYPES = {"topic", "subtopic"}


def all_slugs() -> list[str]:
    return sorted({slug for slugs in DOMAIN_ROADMAPS.values() for slug in slugs})


def fetch(slugs: list[str] | None = None, force: bool = False) -> dict[str, int]:
    """Download each roadmap's structure. Returns {slug: node count}."""
    STRUCTURE_DIR.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    with httpx.Client(follow_redirects=True, timeout=60, headers={"user-agent": "90x-pipeline"}) as client:
        for slug in slugs or all_slugs():
            path = STRUCTURE_DIR / f"{slug}.json"
            if force or not path.exists():
                r = client.get(f"https://roadmap.sh/{slug}.json")
                r.raise_for_status()
                path.write_text(r.text, encoding="utf-8")
            counts[slug] = len(nodes(slug))
    return counts


def _load(slug: str) -> dict:
    return json.loads((STRUCTURE_DIR / f"{slug}.json").read_text(encoding="utf-8"))


def nodes(slug: str) -> list[dict]:
    """Content nodes as {id, label, type, sort}, in reading order.

    Deliberately flat. A roadmap.sh node carries no parent: grouping exists
    only in the picture, as whitespace. Inferring it from geometry was tried
    both ways - nearest topic box, and last topic in reading order - and both
    land near 80%, putting "Event-Driven" under "Availability Patterns" when
    it belongs to "Background Jobs". A checklist in the diagram's own reading
    order is honest and is what the tracker needs; a fabricated tree is worse
    than no tree.

    `type` is "topic" for a main box and "subtopic" for a smaller one, which
    is enough to render two levels of emphasis without claiming parentage.
    """
    raw = _load(slug).get("nodes") or []
    placed = [n for n in raw if n.get("type") in CONTENT_TYPES and n.get("position") and (n.get("data") or {}).get("label")]
    # Rows first, then left to right: y is banded because boxes on one row
    # differ by a few pixels.
    placed.sort(key=lambda n: (round(n["position"]["y"] / 40), n["position"]["x"]))
    return [
        {"id": n["id"], "label": n["data"]["label"], "type": n["type"], "sort": i}
        for i, n in enumerate(placed)
    ]


def content_path(slug: str, node_id: str) -> Path | None:
    """The markdown file for a node, found by its id suffix."""
    matches = list((ROADMAP_DIR / "roadmaps" / slug / "content").glob(f"*@{node_id}.md"))
    return matches[0] if matches else None
