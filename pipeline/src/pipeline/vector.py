"""Upload chunks to Upstash Vector (it embeds the text itself) and delete
vectors whose chunk no longer exists. Only changed chunks are sent."""

import os

import httpx

from . import config  # noqa: F401  (loads pipeline/.env)

BATCH = 100
MAX_UPSERTS_PER_RUN = 9_000  # free tier: 10K updates per day


def plan(chunks: list[dict], embedded: dict[str, str]) -> tuple[list[dict], list[str]]:
    upsert = [c for c in chunks if embedded.get(c["id"]) != c["hash"]]
    live = {c["id"] for c in chunks}
    delete = [vid for vid in embedded if vid not in live]
    return upsert, delete


class VectorClient:
    def __init__(self):
        self.url = os.environ["UPSTASH_VECTOR_REST_URL"].rstrip("/")
        self.http = httpx.Client(headers={"Authorization": f"Bearer {os.environ['UPSTASH_VECTOR_REST_TOKEN']}"}, timeout=120)

    def upsert(self, items: list[dict]) -> None:
        r = self.http.post(f"{self.url}/upsert-data", json=items)
        r.raise_for_status()

    def delete(self, ids: list[str]) -> None:
        r = self.http.post(f"{self.url}/delete", json=ids)
        r.raise_for_status()

    def info(self) -> dict:
        return self.http.get(f"{self.url}/info").json()["result"]

    def query(self, text: str, top_k: int = 3) -> list[dict]:
        r = self.http.post(f"{self.url}/query-data", json={"data": text, "topK": top_k, "includeMetadata": True})
        r.raise_for_status()
        return r.json()["result"]


def run(con, client: VectorClient | None = None, limit: int = MAX_UPSERTS_PER_RUN) -> tuple[int, int, int]:
    """Returns (upserted, deleted, remaining)."""
    client = client or VectorClient()
    con.execute("create table if not exists embedded (id text primary key, hash text)")
    rows = con.execute(
        "select id, text, hash, owner_kind, owner_id, topic_slug, source_id, title, url from chunks"
    ).fetchall()
    chunks = [dict(zip(["id", "text", "hash", "owner_kind", "owner_id", "topic_slug", "source_id", "title", "url"], r)) for r in rows]
    embedded = dict(con.execute("select id, hash from embedded").fetchall())
    upsert, delete = plan(chunks, embedded)

    for i in range(0, len(delete), BATCH):
        batch = delete[i:i + BATCH]
        client.delete(batch)
        con.execute(f"delete from embedded where id in ({','.join('?' * len(batch))})", batch)

    todo, done = upsert[:limit], 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        client.upsert([{
            "id": c["id"], "data": c["text"],
            "metadata": {k: c[k] for k in ("owner_kind", "owner_id", "topic_slug", "source_id", "title", "url") if c[k]},
        } for c in batch])
        con.executemany("insert or replace into embedded (id, hash) values (?, ?)", [[c["id"], c["hash"]] for c in batch])
        done += len(batch)
        if done % 1000 == 0:
            print(f"  embedded {done}/{len(todo)}", flush=True)
    return done, len(delete), len(upsert) - done
