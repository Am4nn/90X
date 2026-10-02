"""Publish staging content to Supabase (direct connection, bypasses RLS).

Idempotent: every table is upserted on its natural key, and rows that no
longer exist in staging are deleted, all in one transaction so the app never
sees a half-published state. Cards go up as drafts; `/admin` makes them live."""

import json

import psycopg

from .sources import SOURCES

# (table, key columns, columns) in dependency order.
TABLES = [
    ("sources", ["id"], ["id", "name", "domain", "url", "license", "role"]),
    ("topics", ["slug"], ["slug", "parent_slug", "domain", "name", "description", "importance", "sort"]),
    ("topic_links", ["from_slug", "to_slug"], ["from_slug", "to_slug"]),
    ("problems", ["slug"], ["slug", "kind", "lc_number", "title", "difficulty", "pattern_slug", "topic_slugs", "tags",
                            "techniques", "importance", "premium", "nc150", "blind75", "companies", "statement_md",
                            "solutions", "video_id", "url", "source_id"]),
    ("pattern_tricks", ["id"], ["id", "pattern_slug", "name", "idea_md", "snippets", "problem_slugs", "sort"]),
    ("roadmap_nodes", ["id"], ["id", "roadmap", "domain", "label", "kind", "sort", "topic_slug"]),
    ("lessons", ["topic_slug"], ["topic_slug", "title", "summary", "body_md", "practice", "source_refs",
                                 "words", "generated_at"]),
]
JSON_COLUMNS = {"companies", "solutions", "snippets", "practice", "source_refs"}
ARRAY_COLUMNS = {"topic_slugs", "tags", "techniques", "problem_slugs"}

# Publishing converges: whatever staging no longer has is deleted. That is right
# for every row the pipeline owns and wrong for the rows it does not. A lesson
# the Coach wrote on demand was never in staging, so to that delete it looks
# like an orphan, and the next publish would quietly remove it. Extra predicates
# that spare rows this pipeline did not write.
#
# `topics` needs one too, and for a less obvious reason: lessons.topic_slug is
# `on delete cascade`, so dropping a topic the taxonomy no longer lists takes its
# Coach-written lesson with it and the lessons exemption never gets a say. A
# topic somebody is reading a lesson on stays until that lesson is dealt with;
# keeping a stale taxonomy row is visible and recoverable, and silently deleting
# someone's lesson is neither.
NOT_OURS = {
    "lessons": "and t.written_by is null",
    "topics": ("and not exists (select 1 from public.lessons l "
               "where l.topic_slug = t.slug and l.written_by is not null)"),
}

# On the way back in, the pipeline takes ownership again. Without this, a Coach
# lesson written for a topic whose staging lesson had not yet been published
# would be overwritten by pipeline text that kept `written_by` set - so the
# pipeline's own words would be credited to a user and, worse, exempted from
# every future delete by the rule above.
RECLAIM = {"lessons": ["written_by = null"]}


def _source_rows(con) -> list[tuple]:
    """sources.py entries plus any source id used by staging rows."""
    rows = {s.name: (s.name, s.name, s.domain, f"https://github.com/{s.target}" if "/" in s.target and not s.target.startswith("http") else s.target,
                     None, s.role) for s in SOURCES}
    used = {r[0] for r in con.execute("select distinct source_id from problems").fetchall() if r[0]}
    for sid in used - rows.keys():
        rows[sid] = (sid, sid, "dsa", None, None, "reference")
    return list(rows.values())


def _sources_of(refs, by_id: dict) -> str:
    """Turn a lesson's chunk references into the books and repos behind it.

    A ref is "<source id>:<document id>", so the prefix names the source.
    Documents no longer exist in Supabase, so a lesson that kept raw ids would
    point at nothing; what the reader wants is the original anyway.
    """
    ids, seen = [], set()
    for ref in json.loads(refs) if isinstance(refs, str) else (refs or []):
        source_id = str(ref).split(":", 1)[0]
        if source_id in by_id and source_id not in seen:
            seen.add(source_id)
            ids.append(source_id)
    return json.dumps([{"id": i, "name": by_id[i][1], "url": by_id[i][3]} for i in ids])


def _with_titles(practice) -> str:
    """Practice holds slugs; the app needs something to display.

    Problem slugs resolve against our own `problems` table, but the real
    interview questions live only in the scraped pages, so their titles are
    folded in here rather than making the app parse HTML."""
    data = json.loads(practice) if isinstance(practice, str) else (practice or {})
    slugs = data.get("questions") or []
    if slugs:
        from .normalize.interview_questions import parse_all

        by_slug = {q["slug"]: q for q in parse_all()}
        data["questions"] = [
            {
                "slug": s,
                "title": by_slug[s]["title"],
                "difficulty": by_slug[s]["difficulty"],
                "url": f"https://systemdesign.io/question/{s}",
            }
            for s in slugs
            if s in by_slug
        ]
    return json.dumps(data)


def _first_sentence(text: str, limit: int = 200) -> str:
    """A lesson opens with its definition, so its first sentence is its summary."""
    head = text.strip().splitlines()[0] if text.strip() else ""
    cut = head.find(". ")
    sentence = head[: cut + 1] if cut > 0 else head
    return sentence[:limit].strip()


def _staging_rows(con, table: str, columns: list[str]) -> list[tuple]:
    if table == "sources":
        return _source_rows(con)
    if table == "lessons":
        # Only lessons that passed the contract and the fact check are published.
        by_id = {r[0]: r for r in _source_rows(con)}
        rows = con.execute(
            "select topic_slug, title, summary, body_md, practice, source_refs, words, generated_at "
            "from lessons where status = 'ok'"
        ).fetchall()
        # Column order must match TABLES: topic_slug, title, summary, body_md, ...
        # The writer's own summary is what lists and search show; the opening
        # sentence is only a fallback for lessons written before it was stored.
        return [(slug, title, summary or _first_sentence(body), body, _with_titles(practice),
                 _sources_of(refs, by_id), words, at)
                for slug, title, summary, body, practice, refs, words, at in rows]
    if table == "topics":  # parents before children
        rows = con.execute(f"select {', '.join(columns)} from topics order by parent_slug is not null, sort").fetchall()
        return rows
    return con.execute(f"select {', '.join(columns)} from {table}").fetchall()


def _prepare(value, column):
    if column in JSON_COLUMNS:
        return json.dumps(json.loads(value) if isinstance(value, str) else (value or {}))
    if column in ARRAY_COLUMNS:
        return list(value or [])
    return value


def _json(value):
    """Serialize a staging JSON string for a jsonb upsert, or None.

    Staging stores the Feed v2 answer columns (`picked`, `constraints`,
    `pairs`, `why_step`) as JSON strings, the same way `options` is stored;
    this round-trips one for a `%s::jsonb` cast the way `_publish_cards` already
    does for its other JSON columns.
    """
    return None if value is None else json.dumps(json.loads(value))


def publish(con, pg: psycopg.Connection, dry_run: bool = False, force: bool = False) -> dict:
    counts = {}
    with pg.transaction():
        cur = pg.cursor()
        for table, keys, columns in TABLES:
            rows = [tuple(_prepare(v, c) for v, c in zip(r, columns)) for r in _staging_rows(con, table, columns)]
            updates = [f"{c} = excluded.{c}" for c in columns if c not in keys] + RECLAIM.get(table, [])
            conflict = f"on conflict ({', '.join(keys)}) " + (
                f"do update set {', '.join(updates)}" if updates else "do nothing")
            placeholders = ", ".join(f"%s::jsonb" if c in JSON_COLUMNS else "%s" for c in columns)
            cur.executemany(f"insert into public.{table} ({', '.join(columns)}) values ({placeholders}) {conflict}", rows)
            # Remove rows that no longer exist in staging.
            cur.execute(f"create temp table _keep ({', '.join(f'{k} text' for k in keys)}) on commit drop")
            cur.executemany(f"insert into _keep values ({', '.join('%s' for _ in keys)})",
                            [tuple(str(r[columns.index(k)]) for k in keys) for r in rows])
            cur.execute(f"""delete from public.{table} t where not exists (
                select 1 from _keep k where {' and '.join(f't.{k}::text = k.{k}' for k in keys)})
                {NOT_OURS.get(table, '')}""")
            deleted = cur.rowcount
            cur.execute("drop table _keep")
            counts[table] = (len(rows), deleted)
        card_counts = _publish_cards(con, cur)
        counts["cards_retired"] = (0, _retire_superseded_cards(con, cur, force))
        counts["batches_retired"] = (0, _retire_empty_batches(cur))
        counts.update(card_counts)
        if dry_run:
            raise _DryRun(counts)
    return counts


def _publish_cards(con, cur) -> dict:
    """Every batch staging holds, every time.

    Publishing only the batches staging had not sent yet made the result depend
    on bookkeeping instead of on the data: a regrouped card kept the batch and
    risk it was published with, because its row already existed. So this
    converges instead - a card's group and risk are whatever staging says, and
    `status` and `hidden` are left alone, because those are the admin's.

    The conflict clause updates every content column, not just the answer ones.
    A card's id is a hash of its topic and its question, so a regenerated card
    with the same question keeps its id - and the clause used to write its new
    `picked`/`pairs`/`value` while keeping the old `format` and `options`. A live
    card could then render one primitive's interaction over another's answer
    definition: a pick_one card showing four stale options against a mapping
    answer, ungradeable by any reader. Everything except `id`, `status` and
    `hidden` therefore converges on what staging holds.
    """
    batches = con.execute(
        "select id, domain, topic_slugs, created_at, ai_pass_rate, label from card_batches").fetchall()
    n_cards = 0
    for bid, domain, topics, created, pass_rate, label in batches:
        cur.execute("""insert into public.card_batches (id, domain, topic_slugs, created_at, ai_pass_rate, label, status)
                       values (%s, %s, %s, %s, %s, %s, 'draft')
                       on conflict (id) do update set
                         topic_slugs = excluded.topic_slugs,
                         ai_pass_rate = excluded.ai_pass_rate,
                         label = excluded.label""",
                    (bid, domain, list(topics or []), created, pass_rate, label))
        # `risk` comes with the card. It is the review screen's sort key, and it
        # sorts ascending, so a card that arrives without one looks safest.
        cards = con.execute(
            """select id, topic_slug, problem_slug, format, difficulty, prompt_md, options, answer_md,
                      key_points, source_refs, quality, risk, archetype, picked, constraints, pairs,
                      value, tolerance, why_step from cards where batch_id = ? and kept""", [bid]).fetchall()
        cur.executemany(
            """insert into public.cards (id, batch_id, topic_slug, problem_slug, format, difficulty, prompt_md,
                   options, answer_md, key_points, source_refs, quality, risk, archetype, picked,
                   constraints, pairs, value, tolerance, why_step, status)
               values (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s::jsonb, %s::jsonb, %s::jsonb, %s, %s,
                       %s::jsonb, %s::jsonb, %s::jsonb, %s, %s, %s::jsonb, 'draft')
               on conflict (id) do update set
                 batch_id = excluded.batch_id, topic_slug = excluded.topic_slug,
                 problem_slug = excluded.problem_slug, format = excluded.format,
                 difficulty = excluded.difficulty, prompt_md = excluded.prompt_md,
                 options = excluded.options, answer_md = excluded.answer_md,
                 key_points = excluded.key_points, source_refs = excluded.source_refs,
                 quality = excluded.quality, risk = excluded.risk, archetype = excluded.archetype,
                 picked = excluded.picked, constraints = excluded.constraints, pairs = excluded.pairs,
                 value = excluded.value, tolerance = excluded.tolerance, why_step = excluded.why_step""",
            [(c[0], bid, *c[1:6], c[6] if c[6] is None else json.dumps(json.loads(c[6])), c[7],
              json.dumps(json.loads(c[8] or "[]")), json.dumps(json.loads(c[9] or "[]")),
              json.dumps(json.loads(c[10] or "{}")), c[11],
              c[12], _json(c[13]), _json(c[14]), _json(c[15]), c[16], c[17], _json(c[18]))
             for c in cards])
        n_cards += len(cards)
    return {"card_batches": (len(batches), 0), "cards": (n_cards, 0)}


class StudyHistoryAtRisk(RuntimeError):
    """Raised rather than cascade away someone's spaced repetition."""


def staged_card_ids(con) -> list[str]:
    """The cards staging still stands behind: `kept`, not every row.

    Staging keeps a rejected card with the gate's reason on it, and a card
    published before a later run rejected it still has its id here. Matching on
    presence alone left that card live in the Feed for good, which is the one
    thing rejecting it was meant to prevent.

    A null `kept` counts as staged, so only an explicit rejection retires a
    card and an older row with the column unset is never deleted by surprise.
    """
    return [r[0] for r in con.execute("select id from cards where kept is not false").fetchall()]


def _retire_superseded_cards(con, cur, force: bool) -> int:
    """Delete **draft** cards that staging no longer has. Never a live one.

    This used to delete every published card staging had dropped, on the premise
    that doing so was "free while the Feed is unused". That premise expired: the
    Feed has answers and spaced-repetition schedules in it now, and card_reviews,
    card_state, card_flags and batch_review_items all cascade from a card.

    Two reasons the scope is drafts alone, not one:

    1. A card a reader could have seen is retired, not deleted - `status` goes to
       `retired` and `card_state` stays, so nobody's readiness dial drops on
       release day (DECISIONS round 4). Retiring is `cards/swap.py`'s job.
    2. Publish must not retire them either. Between publish and the flip the old
       corpus is the only thing live; standing it down here would leave the Feed
       with nothing to serve until the swap ran, which is the shape of the
       2026-09-29 outage.

    So a regenerated corpus leaves every live card in place, and the flip - one
    statement, after the deploy - is what stands the old ones down. Without this
    scope, publishing a regenerated corpus raises `StudyHistoryAtRisk` over the
    entire old corpus and the whole transaction rolls back, which is to say
    production step 3 could not complete at all.
    """
    staged = staged_card_ids(con)
    cur.execute("create temp table _staged_cards (id uuid) on commit drop")
    if staged:
        cur.executemany("insert into _staged_cards values (%s)", [[i] for i in staged])
    # Still guarded, now where it can actually fire: a draft card is invisible to
    # readers, but a card that was live earlier and was set back to draft by hand
    # can carry answers. What a person cannot get back is those answers and the
    # schedule they earned. Flags and batch verdicts cascade too and are not
    # guarded - they are bookkeeping about the card, meaningless once it is gone,
    # and blocking on them would mean every publish needs --force, which is how a
    # guard stops being read.
    at_risk = {}
    for table, label in (("card_reviews", "answers"), ("card_state", "review schedules")):
        cur.execute(
            f"""select count(*) from public.{table} t
                join public.cards c on c.id = t.card_id
                where c.status = 'draft'
                  and not exists (select 1 from _staged_cards s where s.id = t.card_id)"""
        )
        if found := cur.fetchone()[0]:
            at_risk[label] = found
    if at_risk and not force:
        detail = ", ".join(f"{n} {label}" for label, n in at_risk.items())
        raise StudyHistoryAtRisk(
            f"{detail} belong to draft cards staging no longer has. Deleting them would erase "
            "that history. Re-run with force=True only if you mean it."
        )
    cur.execute(
        """delete from public.cards c
           where c.status = 'draft'
             and not exists (select 1 from _staged_cards s where s.id = c.id)"""
    )
    return cur.rowcount


def _retire_empty_batches(cur) -> int:
    """Drop draft batches that hold no card.

    Regrouping every card into new batches leaves the old ones behind, and
    retiring the cards they held empties them without removing them, so
    /admin/cards would list 13 batches with nothing in them. Only draft
    batches holding no verdict: a batch someone has started reviewing is the
    record of that review, empty or not.
    """
    cur.execute(
        """delete from public.card_batches b
           where b.status = 'draft'
             and not exists (select 1 from public.cards c where c.batch_id = b.id)
             and not exists (select 1 from public.batch_review_items i where i.batch_id = b.id)"""
    )
    return cur.rowcount


class _DryRun(Exception):
    def __init__(self, counts):
        super().__init__("dry run")
        self.counts = counts


def run(con, url: str, dry_run: bool = False, force: bool = False) -> dict:
    with psycopg.connect(url, prepare_threshold=None) as pg:
        try:
            return publish(con, pg, dry_run=dry_run, force=force)
        except _DryRun as d:
            return d.counts
