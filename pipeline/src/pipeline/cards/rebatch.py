"""Regroup draft cards into ~13 review batches (area x part), so the admin
reviews a handful of batches instead of one per generation run. Each card also
gets a risk score (the reviewer's lowest score, scaled 0-1) so the review
screen can show the riskiest cards first.

Works on staging and on Supabase in one go: cards are already published there
as drafts, so the new batches are inserted, cards are moved, and the old,
now-empty draft batches are removed."""

import json
import uuid

import psycopg

DSA_GROUPS = {
    "dsa-arrays": ("DSA · Arrays, strings, windows",
                   {"arrays-hashing", "two-pointers", "sliding-window", "prefix-sum", "string", "matrix-grid"}),
    "dsa-search": ("DSA · Search, stacks, heaps, lists",
                   {"binary-search", "stack", "heap-priority-queue", "linked-list", "intervals", "simulation"}),
    "dsa-graphs": ("DSA · Trees, graphs, backtracking",
                   {"trees", "tries", "graphs", "advanced-graphs", "backtracking"}),
    "dsa-dp": ("DSA · Dynamic programming, greedy",
               {"1-d-dynamic-programming", "2-d-dynamic-programming", "greedy"}),
}
DSA_REST = ("dsa-math", "DSA · Math, bits, design")

CS_NET = {"cs-osi-model", "cs-tcp-vs-udp", "cs-tcp-3-way-handshake", "cs-tcp-flow-and-congestion-control", "cs-http-https",
          "cs-dns", "cs-tls-ssl-handshake", "cs-socket-programming", "cs-subnetting-and-cidr"}
CS_DB = {"cs-acid-properties", "cs-normalization", "cs-transaction-isolation-levels", "cs-locking-mechanisms"}

CASE_STUDIES = "sd-design-case-studies"


def group_of(domain: str, topic: str | None, parent: str | None, sort: int, sd_split: int) -> tuple[str, str]:
    """Batch key and label for a card's topic. `sd_split` is the sort value
    that divides core system-design topics into two halves."""
    if domain == "dsa":
        for key, (label, patterns) in DSA_GROUPS.items():
            if topic in patterns:
                return key, label
        return DSA_REST
    if domain == "system_design":
        if topic == CASE_STUDIES or parent == CASE_STUDIES:
            return "sd-cases", "Design · Case studies"
        return ("sd-core-1", "Design · Core concepts I") if sort < sd_split else ("sd-core-2", "Design · Core concepts II")
    if domain == "cs":
        if topic in CS_NET:
            return "cs-net", "CS · Networks"
        if topic in CS_DB:
            return "cs-db", "CS · Databases"
        return "cs-os", "CS · Operating systems, OOP"
    return domain, {"java": "Java", "sql": "SQL"}.get(domain, domain)


def risk_of(quality) -> float | None:
    q = json.loads(quality) if isinstance(quality, str) else (quality or {})
    scores = [q[k] for k in ("correct", "clear", "relevant") if isinstance(q.get(k), (int, float))]
    return round(min(scores) / 5, 3) if scores else None


def plan(con) -> dict[str, dict]:
    """Group kept draft cards from staging: {key: {label, domain, topics, card_ids, risks, pass_rate}}."""
    split = con.execute(
        """select quantile_disc(sort, 0.5) from topics
           where domain = 'system_design' and slug <> ? and coalesce(parent_slug, '') <> ?""",
        [CASE_STUDIES, CASE_STUDIES],
    ).fetchone()[0] or 0
    rows = con.execute(
        """select c.id, c.kept, c.quality, t.domain, c.topic_slug, t.parent_slug, coalesce(t.sort, 0)
           from cards c join topics t on t.slug = c.topic_slug
           where coalesce(c.status, 'draft') = 'draft'"""
    ).fetchall()
    groups: dict[str, dict] = {}
    for card_id, kept, quality, domain, topic, parent, sort in rows:
        key, label = group_of(domain, topic, parent, sort, split)
        g = groups.setdefault(key, {"label": label, "domain": domain, "topics": set(), "card_ids": [], "risks": {},
                                    "generated": 0})
        g["generated"] += 1
        if kept:
            g["topics"].add(topic)
            g["card_ids"].append(card_id)
            g["risks"][card_id] = risk_of(quality)
    for g in groups.values():
        g["pass_rate"] = round(len(g["card_ids"]) / g["generated"], 3) if g["generated"] else None
    return groups


def run(con, database_url: str | None, dry_run: bool = False) -> dict[str, int]:
    groups = plan(con)
    ids = {key: str(uuid.uuid4()) for key in groups}
    summary = {groups[k]["label"]: len(groups[k]["card_ids"]) for k in groups}
    if dry_run:
        return summary

    old = [r[0] for r in con.execute("select id from card_batches").fetchall()]
    if database_url:
        with psycopg.connect(database_url, prepare_threshold=None) as pg, pg.cursor() as cur:
            for key, g in groups.items():
                cur.execute(
                    """insert into public.card_batches (id, domain, label, topic_slugs, ai_pass_rate, status)
                       values (%s, %s, %s, %s, %s, 'draft')""",
                    [ids[key], g["domain"], g["label"], sorted(g["topics"]), g["pass_rate"]],
                )
                cur.executemany(
                    "update public.cards set batch_id = %s, risk = %s where id = %s and status = 'draft'",
                    [[ids[key], g["risks"][c], c] for c in g["card_ids"]],
                )
            # Old draft batches that no longer hold any card.
            cur.execute(
                """delete from public.card_batches b where b.status = 'draft' and b.label is null
                   and not exists (select 1 from public.cards c where c.batch_id = b.id)""",
            )
    for key, g in groups.items():
        con.execute(
            """insert into card_batches (id, domain, topic_slugs, ai_pass_rate, status, published)
               values (?, ?, ?, ?, 'draft', true)""",
            [ids[key], g["domain"], sorted(g["topics"]), g["pass_rate"]],
        )
        con.executemany("update cards set batch_id = ? where id = ?", [[ids[key], c] for c in g["card_ids"]])
    # Dropped (not kept) cards move with their group too, so old batches empty out.
    con.execute(f"delete from card_batches where id in ({', '.join('?' * len(old))})", old) if old else None
    return summary
