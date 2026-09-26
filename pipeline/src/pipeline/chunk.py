"""Split documents and problem statements into ~300-450-word chunks for the
coach's semantic search. Each chunk starts with its title for context."""

import hashlib
import json


def split_text(text: str, max_words: int = 450, min_words: int = 60) -> list[str]:
    pieces: list[list[str]] = []
    for para in text.split("\n\n"):
        tokens = para.split()
        while len(tokens) > max_words:  # a single giant paragraph
            pieces.append(tokens[:max_words])
            tokens = tokens[max_words:]
        if tokens:
            pieces.append(tokens)

    chunks: list[list[str]] = []
    current: list[str] = []
    for tokens in pieces:
        if current and len(current) + len(tokens) > max_words:
            chunks.append(current)
            current = []
        current = current + tokens
    if current:
        if chunks and len(current) < min_words and len(chunks[-1]) + len(current) <= max_words + min_words:
            chunks[-1] = chunks[-1] + current
        else:
            chunks.append(current)
    return [" ".join(c) for c in chunks]


def build_chunks(owner_kind: str, owner_id: str, title: str, text: str, meta: dict) -> list[dict]:
    rows = []
    for n, part in enumerate(split_text(text)):
        body = f"{title}\n\n{part}"
        digest = hashlib.sha1((body + json.dumps(meta, sort_keys=True)).encode()).hexdigest()
        rows.append({"id": f"{owner_kind}:{owner_id}:{n}", "owner_kind": owner_kind, "owner_id": owner_id,
                     "n": n, "text": body, "hash": digest, **meta})
    return rows


def run(con) -> int:
    rows: list[dict] = []
    for doc_id, title, body, domain, topic, source, url in con.execute(
        "select id, title, body_md, domain, topic_slug, source_id, url from documents"
    ).fetchall():
        rows += build_chunks("doc", doc_id, title, body, {"domain": domain, "topic_slug": topic,
                                                          "source_id": source, "title": title, "url": url})
    for slug, title, statement, pattern, source, url, kind in con.execute(
        "select slug, title, statement_md, pattern_slug, source_id, url, kind from problems where statement_md is not null"
    ).fetchall():
        rows += build_chunks("prob", slug, title, statement, {"domain": "competitive" if kind == "competitive" else "dsa",
                                                              "topic_slug": pattern, "source_id": source,
                                                              "title": title, "url": url})
    # Keep what was already embedded; replace the chunk list.
    con.execute("create temp table if not exists _keep as select id, embedded_hash from chunks where embedded_hash is not null")
    con.execute("delete from _keep")
    con.execute("insert into _keep select id, embedded_hash from chunks where embedded_hash is not null")
    con.execute("delete from chunks")
    con.executemany(
        """insert into chunks (id, owner_kind, owner_id, n, text, hash, topic_slug, source_id, title, url)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [[r["id"], r["owner_kind"], r["owner_id"], r["n"], r["text"], r["hash"], r["topic_slug"],
          r["source_id"], r["title"], r["url"]] for r in rows],
    )
    # Remember embedded state per id so `embed` can skip unchanged chunks and delete stale ones.
    con.execute("create table if not exists embedded (id text primary key, hash text)")
    con.execute("insert into embedded select id, embedded_hash from _keep on conflict do nothing")
    con.execute("drop table _keep")
    return len(rows)
