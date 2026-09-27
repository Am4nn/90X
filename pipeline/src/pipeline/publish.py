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


def _source_rows(con) -> list[tuple]:
    """sources.py entries plus any source id used by staging rows."""
    rows = {s.name: (s.name, s.name, s.domain, f"https://github.com/{s.target}" if "/" in s.target and not s.target.startswith("http") else s.target,
                     None, s.role) for s in SOURCES}
    used = {r[0] for r in con.execute("select distinct source_id from problems").fetchall() if r[0]}
    for sid in used - rows.keys():
        rows[sid] = (sid, sid, "dsa", None, None, "reference")
    return list(rows.values())


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
        rows = con.execute(
            "select topic_slug, title, body_md, practice, source_refs, words, generated_at "
            "from lessons where status = 'ok'"
        ).fetchall()
        return [(slug, title, _first_sentence(body), _with_titles(practice), refs, words, at)
                for slug, title, body, practice, refs, words, at in rows]
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


def publish(con, pg: psycopg.Connection, dry_run: bool = False) -> dict:
    counts = {}
    with pg.transaction():
        cur = pg.cursor()
        for table, keys, columns in TABLES:
            rows = [tuple(_prepare(v, c) for v, c in zip(r, columns)) for r in _staging_rows(con, table, columns)]
            updates = [c for c in columns if c not in keys]
            conflict = f"on conflict ({', '.join(keys)}) " + (
                f"do update set {', '.join(f'{c} = excluded.{c}' for c in updates)}" if updates else "do nothing")
            placeholders = ", ".join(f"%s::jsonb" if c in JSON_COLUMNS else "%s" for c in columns)
            cur.executemany(f"insert into public.{table} ({', '.join(columns)}) values ({placeholders}) {conflict}", rows)
            # Remove rows that no longer exist in staging.
            cur.execute(f"create temp table _keep ({', '.join(f'{k} text' for k in keys)}) on commit drop")
            cur.executemany(f"insert into _keep values ({', '.join('%s' for _ in keys)})",
                            [tuple(str(r[columns.index(k)]) for k in keys) for r in rows])
            cur.execute(f"""delete from public.{table} t where not exists (
                select 1 from _keep k where {' and '.join(f't.{k}::text = k.{k}' for k in keys)})""")
            deleted = cur.rowcount
            cur.execute("drop table _keep")
            counts[table] = (len(rows), deleted)
        card_counts, published_batches = _publish_cards(con, cur)
        counts.update(card_counts)
        if dry_run:
            raise _DryRun(counts)
    # Only after Supabase committed: remember which batches went up.
    for bid in published_batches:
        con.execute("update card_batches set published = true where id = ?", [bid])
    return counts


def _publish_cards(con, cur) -> tuple[dict, list[str]]:
    """New batches only; cards already published keep their status (draft/live)."""
    batches = con.execute(
        "select id, domain, topic_slugs, created_at, ai_pass_rate from card_batches where not published").fetchall()
    n_cards = 0
    for bid, domain, topics, created, pass_rate in batches:
        cur.execute("""insert into public.card_batches (id, domain, topic_slugs, created_at, ai_pass_rate, status)
                       values (%s, %s, %s, %s, %s, 'draft') on conflict (id) do nothing""",
                    (bid, domain, list(topics or []), created, pass_rate))
        cards = con.execute(
            """select id, topic_slug, problem_slug, document_id, format, difficulty, prompt_md, options, answer_md,
                      key_points, source_refs, quality from cards where batch_id = ? and kept""", [bid]).fetchall()
        cur.executemany(
            """insert into public.cards (id, batch_id, topic_slug, problem_slug, document_id, format, difficulty, prompt_md,
                   options, answer_md, key_points, source_refs, quality, status)
               values (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s::jsonb, %s::jsonb, %s::jsonb, 'draft')
               on conflict (id) do nothing""",
            [(c[0], bid, *c[1:7], c[7] if c[7] is None else json.dumps(json.loads(c[7])), c[8],
              json.dumps(json.loads(c[9] or "[]")), json.dumps(json.loads(c[10] or "[]")), json.dumps(json.loads(c[11] or "{}")))
             for c in cards])
        n_cards += len(cards)
    return {"card_batches": (len(batches), 0), "cards": (n_cards, 0)}, [b[0] for b in batches]


class _DryRun(Exception):
    def __init__(self, counts):
        super().__init__("dry run")
        self.counts = counts


def run(con, url: str, dry_run: bool = False) -> dict:
    with psycopg.connect(url, prepare_threshold=None) as pg:
        try:
            return publish(con, pg, dry_run=dry_run)
        except _DryRun as d:
            return d.counts
