"""The local staging database (.data/staging.duckdb): the master copy of all
content. Supabase and Upstash Vector are rebuilt from here by `publish` and
`embed`. Tables mirror the Supabase content tables, plus pipeline-only ones."""

from pathlib import Path

import duckdb

from .config import DATA_DIR

DB_PATH = DATA_DIR / "staging.duckdb"

DDL = """
create table if not exists sources (
    id text primary key, name text not null, domain text not null,
    url text, license text, role text not null
);
create table if not exists topics (
    slug text primary key, parent_slug text, domain text not null, name text not null,
    description text, importance double default 0.5, sort int default 0
);
create table if not exists topic_links (
    from_slug text, to_slug text, primary key (from_slug, to_slug)
);
create table if not exists problems (
    slug text primary key, kind text not null, lc_number int, title text not null,
    difficulty text not null, pattern_slug text, topic_slugs text[], tags text[],
    importance double default 0, nc150 boolean default false, blind75 boolean default false,
    companies json, statement_md text, solutions json, video_id text, url text, source_id text,
    -- pipeline-only enrichment inputs
    ac_rate double, total_accepted bigint, similar_slugs text[], pattern_source text
);
alter table problems add column if not exists premium boolean default false;
alter table problems add column if not exists techniques text[];
create table if not exists documents (
    id text primary key, topic_slug text, domain text not null, title text not null,
    body_md text not null, url text, source_id text, sort int default 0, path text
);
create table if not exists chunks (
    id text primary key, owner_kind text not null, owner_id text not null, n int not null,
    text text not null, hash text not null, topic_slug text, source_id text, title text,
    url text, embedded_hash text
);
create table if not exists card_batches (
    id text primary key, domain text not null, topic_slugs text[], created_at timestamp default now(),
    ai_pass_rate double, sample_pass_rate double, status text default 'draft', published boolean default false
);
create table if not exists cards (
    id text primary key, batch_id text, topic_slug text, problem_slug text, document_id text,
    format text not null, difficulty text, prompt_md text not null, options json,
    answer_md text not null, key_points json, source_refs json, quality json,
    status text default 'draft', kept boolean
);
create table if not exists lessons (
    topic_slug text primary key, title text not null, body_md text not null,
    source_refs json, words int, status text default 'draft', problems text,
    generated_at timestamp
);
-- practice: problems and real interview questions this lesson unlocks.
-- findings: what the fact-checker still objected to, when status is 'failed'.
alter table lessons add column if not exists practice json;
alter table lessons add column if not exists findings json;
alter table lessons add column if not exists summary text;
alter table cards add column if not exists source text default 'chunk';
alter table cards add column if not exists reject_reason text;
alter table cards add column if not exists created_at timestamp;
-- risk and label are set by rebatch and carried by publish. They used to be
-- written straight to Supabase, which only worked when the cards were already
-- there; a batch built before its first publish arrived unlabelled, and every
-- card arrived with no risk, which the review screen reads as "safest".
alter table cards add column if not exists risk double;
alter table card_batches add column if not exists label text;
create table if not exists roadmap_nodes (
    id text primary key, roadmap text not null, domain text not null, label text not null,
    kind text not null, sort int not null, topic_slug text
);
create table if not exists pattern_tricks (
    id text primary key, pattern_slug text not null, name text not null, idea_md text not null,
    snippets json, problem_slugs text[], sort int default 0
);
create table if not exists llm_calls (
    called_at timestamp default now(), model text, purpose text, tokens_in int, tokens_out int,
    cost_usd double, off_peak boolean
);
alter table llm_calls add column if not exists tokens_reasoning int default 0;
"""


def connect(path: Path = DB_PATH) -> duckdb.DuckDBPyConnection:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(path))
    con.execute(DDL)
    return con
