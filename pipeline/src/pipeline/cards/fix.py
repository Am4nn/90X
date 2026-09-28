"""Apply a human reviewer's objections to specific cards.

A review round produces two kinds of finding. The first is about the gate -
it let something through, or threw something good away - and that is fixed in
the gate. The second is about one card: this claim is false, this question is
too broad to grade, these distractors give the answer away. Those need the
objection itself, because no gate reading the question alone can know that
NOT NULL is a SQL constraint.

So the objections live in `.planning/card-objections.md` as data, and this
pushes each one through the same rewrite-and-re-gate path the gate's own
rejections use. Nothing hand-patches a row: a corrected card is gated like any
other, and one that cannot pass is marked rejected with the reviewer's words on
it rather than quietly replaced with something worse.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from ..config import REPO_DIR
from ..llm import LLM, LLMError
from . import gate
from .from_lessons import rewrite
from .run_lessons import card_id

OBJECTIONS = Path(REPO_DIR) / ".planning" / "card-objections.md"
HEADING = re.compile(r"^## ([a-z0-9][a-z0-9-]*)\s*$", re.MULTILINE)


def objections(path: Path = OBJECTIONS) -> dict[str, str]:
    """{topic_slug: objection}, in file order.

    The heading is a topic slug because the review sample carries at most one
    card per topic, so the slug identifies the card a reviewer is talking about
    without them having to copy a uuid out of a markdown file.
    """
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    found: dict[str, str] = {}
    marks = list(HEADING.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[m.end():end].strip()
        if body:
            found[m.group(1)] = body
    return found


class Draft:
    """The shape `rewrite` and `gate` expect, loaded back out of staging."""

    def __init__(self, row) -> None:
        (self.id, self.topic_slug, self.format, self.difficulty, self.prompt,
         options, self.answer, key_points, quality) = row
        self.options = json.loads(options) if options else []
        self.key_points = json.loads(key_points or "[]")
        self.from_review = bool((json.loads(quality or "{}") or {}).get("from_review"))


def drafts_for(con, slugs: list[str]) -> dict[str, Draft]:
    """The card a reviewer is talking about, per topic.

    Rejected cards are in scope, not only drafts: "the gate was wrong to drop
    this, make it multiple choice" is a normal objection, and the reviewer
    named the Java equals() contract card as exactly that. Drafts are preferred
    when a topic has both, because a live card is the one being complained
    about.
    """
    rows = con.execute(
        f"""select id, topic_slug, format, difficulty, prompt_md, options, answer_md, key_points, quality
            from cards where source = 'lesson' and status in ('draft', 'rejected')
              and topic_slug in ({', '.join('?' * len(slugs))})
            order by topic_slug, case status when 'draft' then 0 else 1 end, id""",
        slugs,
    ).fetchall()
    # One card per topic in the sample, so the first is the one reviewed. If a
    # topic ever carries two objections this is where that shows up.
    out: dict[str, Draft] = {}
    for row in rows:
        out.setdefault(row[1], Draft(row))
    return out


def replace(con, old: Draft, card, topic: dict, reason: str | None) -> None:
    """Swap the reviewed card for its replacement, or mark it rejected.

    The old row goes whatever happens: a card a human called false must not
    still be in the Feed because its rewrite also failed. It is kept as the
    record, with the objection on it, the way the gate's own rejects are.
    """
    now = datetime.now(timezone.utc)
    con.execute(
        "update cards set status = 'repaired', kept = false, reject_reason = ? where id = ?",
        [f"a human reviewer objected: {old.prompt[:80]}", old.id],
    )
    refs = json.dumps([{"kind": "lesson", "id": topic["slug"], "title": topic["name"]}])
    con.execute(
        """insert or replace into cards
           (id, topic_slug, format, difficulty, prompt_md, options, answer_md, key_points,
            source_refs, quality, kept, status, source, reject_reason, created_at)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'lesson', ?, ?)""",
        [
            card_id(topic["slug"], card.prompt, "" if reason is None else "rejected"),
            topic["slug"], card.format, card.difficulty, card.prompt,
            json.dumps(card.options) if card.options else None, card.answer,
            json.dumps(card.key_points), refs,
            json.dumps({"gate_confidence": 0.5, "from_review": True}),
            reason is None, "rejected" if reason else "draft", reason, now,
        ],
    )


def run(con, llm: LLM | None = None, tier: str = "smart", path: Path = OBJECTIONS,
        only: list[str] | None = None) -> tuple[int, int]:
    """Returns (fixed, still_failing).

    Idempotent: a card already carrying `from_review` is the answer to this
    objection, not a new subject for it. Without that, a second run - to retry
    the one topic whose rewrite returned bad JSON - would rewrite the twelve
    good replacements against the objections they had already satisfied.
    """
    llm = llm or LLM(con)
    notes = objections(path)
    if only:
        notes = {k: v for k, v in notes.items() if k in set(only)}
    if not notes:
        print(f"no objections in {path}", flush=True)
        return 0, 0
    drafts = drafts_for(con, list(notes))
    topics = {
        r[0]: {"slug": r[0], "name": r[1], "domain": r[2], "lesson": r[3]}
        for r in con.execute(
            f"""select t.slug, t.name, t.domain, l.body_md from topics t join lessons l on l.topic_slug = t.slug
                where t.slug in ({', '.join('?' * len(notes))})""",
            list(notes),
        ).fetchall()
    }

    fixed = failed = 0
    print(f"{len(notes)} objections to apply", flush=True)
    for slug, objection in notes.items():
        old, topic = drafts.get(slug), topics.get(slug)
        if old is None or topic is None:
            print(f"  {slug}: no draft card to fix", flush=True)
            continue
        if old.from_review:
            print(f"  {slug}: already answered by a review rewrite", flush=True)
            continue
        # One objection the model cannot answer must not cost the other twelve.
        try:
            replacements = rewrite(llm, topic, topic["lesson"], [(old, objection)], tier=tier)
        except LLMError as e:
            print(f"  {slug}: the rewrite failed, {e}", flush=True)
            failed += 1
            continue
        if not replacements:
            print(f"  {slug}: the rewrite returned nothing", flush=True)
            failed += 1
            continue
        card = replacements[0]
        rejected = gate.judge([card], gate.review(llm, topic, [card]))
        reason = rejected[0][1] if rejected else None
        replace(con, old, card, topic, reason)
        if reason:
            print(f"  {slug}: replacement still rejected - {reason}", flush=True)
            failed += 1
        else:
            print(f"  {slug}: fixed", flush=True)
            fixed += 1
    return fixed, failed
