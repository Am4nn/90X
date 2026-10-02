"""Write every rejected card to a file, so a reject is a decision we can revisit.

Rejected cards already survive in `.data/staging.duckdb` - nothing in the publish
or swap path deletes them, and `publish` only ever reads `where kept`. But that is
implicit: it holds because `run_lessons.save` happens not to run, and it lives in a
binary nobody can grep. A regeneration of a topic would delete the lot.

This writes them out as JSONL plus a reason summary, grouped so the useful ones are
findable: a card turned down for the wrong archetype is a good question in the wrong
drawer, and those are worth coming back to. Run it before any destructive step.
"""

import json
import os
from collections import Counter
from datetime import datetime, timezone

import duckdb

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.data/review/rejected-cards.jsonl"))
SUMMARY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.data/review/rejected-cards.md"))

con = duckdb.connect(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.data/staging.duckdb")), read_only=True)

rows = con.execute("""
    select c.id, c.topic_slug, t.name, c.archetype, c.format, c.difficulty,
           c.prompt_md, c.options, c.answer_md, c.key_points, c.status, c.reject_reason,
           c.quality
      from cards c join topics t on t.slug = c.topic_slug
     where c.source = 'lesson' and c.kept = false
     order by t.importance desc, c.topic_slug, c.id
""").fetchall()
cols = ["id", "topic", "topic_name", "archetype", "format", "difficulty", "prompt",
        "options", "answer", "key_points", "status", "reject_reason", "quality"]


def family(reason: str) -> str:
    """The verdict that turned the card down, not its wording."""
    r = (reason or "").lower()
    for prefix, name in (
        ("wrong archetype", "wrong archetype - a good question in the wrong drawer"),
        ("guessable", "guessable - the shape of the options gives it away"),
        ("not well formed", "not well formed - limits, duplicates, unsatisfiable order"),
        ("not answerable", "not answerable"),
        ("refers to unseen", "refers to material the reader never sees"),
        ("more than one answer", "more than one defensible answer"),
        ("impossible premise", "the premise cannot hold"),
        ("wrong_format", "the answer does not fit the format"),
    ):
        if r.startswith(prefix):
            return name
    return "other" if reason else "superseded by a rewrite"


with open(OUT, "w", encoding="utf-8") as fh:
    for row in rows:
        card = dict(zip(cols, row))
        card["created_at"] = None
        card["family"] = family(card["reject_reason"])
        fh.write(json.dumps(card, default=str, ensure_ascii=False) + "\n")

families = Counter(family(r[11]) for r in rows)
by_topic = Counter(r[1] for r in rows)
archetypes = Counter(r[3] for r in rows if (r[11] or "").lower().startswith("wrong archetype"))

with open(SUMMARY, "w", encoding="utf-8") as fh:
    fh.write("# Rejected cards, kept for later\n\n")
    fh.write(f"{len(rows)} cards, written {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC. "
             f"Full rows in `rejected-cards.jsonl`, one JSON object per line.\n\n")
    fh.write("Nothing in the publish or swap path deletes these: `publish` reads only "
             "`where kept`. The one thing that would is re-running `cards` for a topic, "
             "which deletes that topic's rows before writing new ones.\n\n")
    fh.write("## Why they were turned down\n\n| cards | verdict |\n|---|---|\n")
    for name, n in families.most_common():
        fh.write(f"| {n} | {name} |\n")
    fh.write("\n## Worth coming back to first\n\n")
    fh.write("Cards rejected for the wrong archetype are not bad questions - they are "
             "filed under the wrong one. `pipeline refile` moves them to an archetype "
             "that fits, bounded by area, primitive, difficulty and the model answer.\n\n")
    fh.write("| cards | archetype they were filed under |\n|---|---|\n")
    for name, n in archetypes.most_common(12):
        fh.write(f"| {n} | {name} |\n")
    fh.write("\n## Topics losing the most\n\n| cards | topic |\n|---|---|\n")
    for name, n in by_topic.most_common(12):
        fh.write(f"| {n} | {name} |\n")

print(f"{len(rows)} rejected cards -> {OUT}")
for name, n in families.most_common():
    print(f"  {n:>5}  {name}")
