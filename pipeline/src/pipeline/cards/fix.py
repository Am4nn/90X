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
# A quoted fragment of the question, to pick one card out of a topic's ten.
MATCH = re.compile(r"^match:\s*(.+?)\s*$", re.MULTILINE)


class Objection:
    """One reviewer complaint, and which card it is about.

    The heading alone was not enough. It is a topic slug, and the first version
    took the topic's first card - but a topic has around ten, and the review
    sample shows one of them. So twelve of thirteen objections rewrote a card
    nobody had complained about and left the offending one live: the levelling
    ladder the reviewer called out by name was still publishable afterwards.

    A `match:` line carries a fragment of the question, which the review pack
    now prints beside each card so it can be copied.
    """

    def __init__(self, slug: str, body: str) -> None:
        self.slug = slug
        found = MATCH.search(body)
        self.match = found.group(1).strip().strip('"') if found else ""
        self.text = MATCH.sub("", body).strip()


def objections(path: Path = OBJECTIONS) -> dict[str, Objection]:
    """{key: Objection}, in file order. The key is the heading plus its match,
    so one topic can carry an objection about more than one of its cards."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    found: dict[str, Objection] = {}
    marks = list(HEADING.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[m.end():end].strip()
        if not body:
            continue
        item = Objection(m.group(1), body)
        found[f"{item.slug}|{item.match}"] = item
    return found


class Draft:
    """The shape `rewrite` and `gate` expect, loaded back out of staging."""

    def __init__(self, row) -> None:
        (self.id, self.topic_slug, self.format, self.difficulty, self.prompt,
         options, self.answer, key_points, quality) = row
        self.options = json.loads(options) if options else []
        self.key_points = json.loads(key_points or "[]")
        self.from_review = bool((json.loads(quality or "{}") or {}).get("from_review"))


def candidates_for(con, slugs: list[str]) -> dict[str, list[Draft]]:
    """Every card in these topics that an objection could be about.

    Rejected cards are in scope, not only drafts: "the gate was wrong to drop
    this, make it multiple choice" is a normal objection, and the reviewer named
    the Java equals() contract card as exactly that. Drafts come first, because
    a live card is the more likely subject of a complaint.
    """
    rows = con.execute(
        f"""select id, topic_slug, format, difficulty, prompt_md, options, answer_md, key_points, quality
            from cards where source = 'lesson' and status in ('draft', 'rejected')
              and topic_slug in ({', '.join('?' * len(slugs))})
            order by topic_slug, case status when 'draft' then 0 else 1 end, id""",
        slugs,
    ).fetchall()
    out: dict[str, list[Draft]] = {}
    for row in rows:
        out.setdefault(row[1], []).append(Draft(row))
    return out


def pick(cards: list[Draft], match: str) -> Draft | None:
    """The one card an objection is about, or None rather than a guess.

    Taking the topic's first card is what broke the first run: a topic has
    around ten and the review sample shows one, so twelve of thirteen
    objections rewrote a card nobody had complained about. With no `match:` line
    there is exactly one card to be sure about; otherwise refuse and say so,
    because rewriting the wrong card is worse than rewriting none.
    """
    if match:
        needle = " ".join(match.split()).casefold()
        hits = [c for c in cards if needle in " ".join(c.prompt.split()).casefold()]
        return hits[0] if len(hits) == 1 else None
    return cards[0] if len(cards) == 1 else None


def replace(con, old: Draft, card, topic: dict, reason: str | None, confidence: float = 0.5) -> None:
    """Swap the reviewed card for its replacement, or mark it rejected.

    The old row goes whatever happens: a card a human called false must not
    still be in the Feed because its rewrite also failed.

    What it becomes depends on the replacement. Marking it `repaired`
    unconditionally counted a failed fix as a success, because the review pack
    reads every repaired row as "rewritten and passed" - so one objection showed
    up as both a fix and a drop. It is only `repaired` when something replaced
    it; otherwise it is `rejected`, carrying the objection.
    """
    now = datetime.now(timezone.utc)
    # Re-keyed first: a rewrite that changes only the answer keeps the question,
    # so old and new share a prompt-derived id and `insert or replace` would
    # overwrite the record of what was objected to.
    con.execute(
        "update cards set id = ?, status = ?, kept = false, reject_reason = ? where id = ?",
        [
            card_id(topic["slug"], old.prompt, "repaired" if reason is None else "rejected"),
            "repaired" if reason is None else "rejected",
            f"a human reviewer objected: {old.prompt[:80]}",
            old.id,
        ],
    )
    refs = json.dumps([{"kind": "lesson", "id": topic["slug"], "title": topic["name"]}])
    con.execute(
        """insert or replace into cards
           (id, topic_slug, format, difficulty, prompt_md, options, answer_md, key_points,
            source_refs, quality, kept, status, source, reject_reason, created_at)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'lesson', ?, ?)""",
        [
            card_id(topic["slug"], card.prompt, "" if reason is None else "rejected-fix"),
            topic["slug"], card.format, card.difficulty, card.prompt,
            json.dumps(card.options) if card.options else None, card.answer,
            json.dumps(card.key_points), refs,
            # `from_review` marks only a replacement that passed. A rejected one
            # must stay retryable: marking it too meant the next run skipped the
            # objection as "already answered" and it could never be fixed.
            json.dumps({"gate_confidence": confidence, "from_review": reason is None}),
            reason is None, "rejected" if reason else "draft", reason, now,
        ],
    )


def run(con, llm: LLM | None = None, tier: str = "smart", path: Path = OBJECTIONS,
        only: list[str] | None = None) -> tuple[int, int]:
    """Returns (fixed, still_failing).

    Idempotent: a card already carrying `from_review` is the answer to this
    objection, not a new subject for it. Without that, a second run - to retry
    one whose rewrite returned bad JSON - would rewrite the replacements against
    the objections they had already satisfied.
    """
    llm = llm or LLM(con)
    notes = objections(path)
    if only:
        notes = {k: v for k, v in notes.items() if v.slug in set(only)}
    if not notes:
        print(f"no objections in {path}", flush=True)
        return 0, 0
    slugs = sorted({v.slug for v in notes.values()})
    candidates = candidates_for(con, slugs)
    topics = {
        r[0]: {"slug": r[0], "name": r[1], "domain": r[2], "lesson": r[3]}
        for r in con.execute(
            f"""select t.slug, t.name, t.domain, l.body_md from topics t join lessons l on l.topic_slug = t.slug
                where t.slug in ({', '.join('?' * len(slugs))})""",
            slugs,
        ).fetchall()
    }

    fixed = failed = 0
    print(f"{len(notes)} objections to apply", flush=True)
    for key, item in notes.items():
        topic = topics.get(item.slug)
        cards = candidates.get(item.slug, [])
        old = pick(cards, item.match) if topic else None
        if topic is None or old is None:
            why = ("no lesson for this topic" if topic is None
                   else f"{len(cards)} cards in this topic and `match:` picked "
                        f"{'none' if item.match else 'no single one'}")
            print(f"  {key}: skipped - {why}", flush=True)
            failed += 1
            continue
        if old.from_review:
            print(f"  {key}: already answered by a review rewrite", flush=True)
            continue
        # One objection the model cannot answer must not cost the others.
        try:
            replacements = rewrite(llm, topic, topic["lesson"], [(old, item.text)], tier=tier)
        except LLMError as e:
            print(f"  {key}: the rewrite failed, {e}", flush=True)
            failed += 1
            continue
        if not replacements:
            print(f"  {key}: the rewrite returned nothing", flush=True)
            failed += 1
            continue
        card = replacements[0]
        result = gate.review(llm, topic, [card])
        rejected = gate.judge([card], result)
        reason = rejected[0][1] if rejected else None
        replace(con, old, card, topic, reason,
                gate.confidence_by_card([card], result).get(id(card), 0.5))
        if reason:
            print(f"  {key}: replacement still rejected - {reason}", flush=True)
            failed += 1
        else:
            print(f"  {key}: fixed", flush=True)
            fixed += 1
    return fixed, failed
