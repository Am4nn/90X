"""Topic lists for the non-DSA areas.

draft:  DeepSeek Pro proposes an interview-oriented topic list per area from
        the section headings of our documents → pipeline/topics/<area>.yaml.
        A human edits and approves the file (rename, delete, add, re-weight).
apply:  loads the approved file into `topics`, then sorts every document of
        the area into a topic (Flash, in batches of titles + openings)."""

import re
from collections import Counter
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from ..config import PIPELINE_DIR

TOPICS_DIR = PIPELINE_DIR / "topics"
PREFIX = {"system_design": "sd", "cs": "cs", "java": "java", "sql": "sql", "lld": "lld", "ai": "ai", "behavioral": "beh"}
AREA_NAMES = {"system_design": "system design", "cs": "CS fundamentals (OS, DBMS, networks, OOP, concurrency)",
              "java": "Java", "sql": "SQL and databases", "lld": "low-level / object-oriented design",
              "ai": "AI / ML engineering", "behavioral": "behavioral interviews"}

DRAFT_SYSTEM = """You design the topic list for one area of a software-engineering interview-prep app.
From the section headings you are given (they come from open study material), propose 15-40 topics that an
interviewer actually tests. Merge duplicates, skip book-structure headings (preface, exercises, lab projects,
contributing), and use short, standard names ("Consistent hashing", "Deadlocks", "HashMap internals").
Use at most two levels: an optional parent (by exact name of another topic you list) for grouping.
importance: 0-1, how often it comes up in interviews for a backend engineer.
description: one short line."""

CLASSIFY_SYSTEM = """Assign each numbered study-material section to the single best topic slug from the list,
or "none" if it fits no topic or isn't interview material (book structure, exercises, contributing notes)."""


class DraftTopic(BaseModel):
    name: str
    parent: str | None = None
    importance: float = Field(ge=0, le=1)
    description: str = ""


class Draft(BaseModel):
    topics: list[DraftTopic] = Field(min_length=3, max_length=60)


class Assignment(BaseModel):
    doc: int
    topic: str


class Assignments(BaseModel):
    assignments: list[Assignment]


def slugify(domain: str, name: str) -> str:
    return f"{PREFIX[domain]}-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _path(domain: str, out_dir: Path | None) -> Path:
    return (out_dir or TOPICS_DIR) / f"{domain}.yaml"


def draft(con, llm, domain: str, out_dir: Path | None = None, max_headings: int = 600) -> str:
    titles = [t for (t,) in con.execute("select title from documents where domain = ?", [domain]).fetchall()]
    heads = Counter(t.split(" › ")[-1].strip() for t in titles)
    headings = [h for h, _ in heads.most_common(max_headings)]
    user = f"Area: {AREA_NAMES[domain]}\n\nSection headings ({len(headings)}):\n" + "\n".join(f"- {h}" for h in headings)
    result = llm.complete_json(DRAFT_SYSTEM, user, Draft, tier="smart", purpose=f"topics-draft-{domain}")

    by_name = {t.name: slugify(domain, t.name) for t in result.topics}
    rows = [{"name": t.name, "slug": by_name[t.name], "parent": by_name.get(t.parent) if t.parent else None,
             "importance": round(t.importance, 2), "description": t.description} for t in result.topics]
    path = _path(domain, out_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (f"# Topic list for {AREA_NAMES[domain]} (drafted by AI from {len(titles)} note sections).\n"
              "# Edit freely: rename, delete, add topics, change importance (0-1) or parent (a slug from this file).\n"
              "# Keep slugs unique. Then run: uv run pipeline topics apply " + domain + "\n")
    path.write_text(header + yaml.safe_dump({"domain": domain, "topics": rows}, sort_keys=False, allow_unicode=True),
                    encoding="utf-8")
    return str(path)


def load(domain: str, out_dir: Path | None = None) -> list[dict]:
    data = yaml.safe_load(_path(domain, out_dir).read_text(encoding="utf-8"))
    topics = data["topics"]
    slugs = [t["slug"] for t in topics]
    if len(slugs) != len(set(slugs)):
        raise ValueError(f"{domain}: duplicate slugs")
    for t in topics:
        if t.get("parent") and t["parent"] not in slugs:
            raise ValueError(f"{domain}: topic {t['slug']} has unknown parent {t['parent']}")
    return topics


def apply(con, llm, domain: str, out_dir: Path | None = None, batch: int = 40) -> int:
    topics = load(domain, out_dir)
    con.execute("update documents set topic_slug = null where domain = ?", [domain])
    con.execute("delete from topics where domain = ?", [domain])
    con.executemany(
        "insert into topics (slug, parent_slug, domain, name, description, importance, sort) values (?, ?, ?, ?, ?, ?, ?)",
        [[t["slug"], t.get("parent"), domain, t["name"], t.get("description"), float(t.get("importance", 0.5)), i]
         for i, t in enumerate(topics)],
    )
    valid = {t["slug"] for t in topics}
    topic_list = "\n".join(f"- {t['slug']}: {t['name']}" for t in topics)
    docs = con.execute("select id, title, body_md from documents where domain = ? order by id", [domain]).fetchall()
    assigned = 0
    for start in range(0, len(docs), batch):
        chunk = docs[start:start + batch]
        numbered = "\n".join(f"{i + 1}. {title} — {' '.join(body.split())[:240]}" for i, (_, title, body) in enumerate(chunk))
        result = llm.complete_json(CLASSIFY_SYSTEM, f"Topics:\n{topic_list}\n\nSections:\n{numbered}", Assignments,
                                   tier="fast", purpose=f"topics-classify-{domain}")
        for a in result.assignments:
            if 1 <= a.doc <= len(chunk) and a.topic in valid:
                con.execute("update documents set topic_slug = ? where id = ?", [a.topic, chunk[a.doc - 1][0]])
                assigned += 1
    return assigned
