# 90X

Personal interview-prep app: daily missions, attempt tracking, AI mock interviews and a question feed.

- Spec: [.planning/SPEC.md](.planning/SPEC.md)
- Original research (reference only): `.planning/chatgpt-research/`

## Layout

```
.planning/   spec and research
.data/       raw downloads (git-ignored)
pipeline/    Python data pipeline (uv)
supabase/    migrations, seed, config
web/         Next.js app (bun)
```

## Setup

Needs Bun, uv, and Docker (for local Supabase).

```bash
# Web app
cd web
bun install
cp .env.example .env.local   # fill in values
bun run db:start             # local Supabase
bun run dev

# Pipeline
cd pipeline
uv sync
uv run pipeline
```

## Web scripts

| Script | Does |
|---|---|
| `dev`, `build`, `lint`, `typecheck`, `test` | the usual |
| `db:start` / `db:stop` | local Supabase |
| `db:new <name>` | new SQL migration |
| `db:reset` | rebuild local DB from migrations + seed |
| `db:push` | apply migrations to the linked cloud project |
| `db:pull` | pull schema into Drizzle types |
| `db:types` | generate supabase-js types |
