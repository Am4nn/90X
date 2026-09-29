You are building **Part A of Feed v2: the schema and the archetype registry**.

**Worktree** `../90X-wt-fv2/a` · **Branch** `feed-v2-schema` · **No Playwright spec.**

This part lands first and alone; every other part codes against the contract you define. You
contain the migration.

## Read these first, in this order

1. `.planning/feed-v2/plans/prompts/SETUP.md` — your environment, the migration rule, every gate,
   the forbidden files. **Read it before you write any code.**
2. `.planning/briefs/README.md` — how this codebase is written. Wins over everything.
3. **`.planning/feed-v2/plans/A-schema-registry.md` — your plan.** Exact files, the migration, the
   full 47-archetype table, the generated-module contract, the traps. **The table is the
   contract; encode it exactly, do not re-derive it from CATALOGUE.md.**
4. `.planning/feed-v2/plans/README.md` — the wave's rules and the answer contract.
5. `.planning/feed-v2/DECISIONS.md` and `PRIMITIVES.md` — the reasoning behind the shapes.

## What you are doing

Add the columns that let a card carry its archetype, its deterministic answer and its observed
outcomes; create `archetypes.json` (single source of truth) and the generator that emits
`web/src/lib/feed/archetypes.ts`; regenerate the pulled schema. **Purely additive and
non-breaking** — the existing app and `e2e/feed.spec.ts` stay green.

## The traps that will cost you most

1. **`cards.status` already allows `retired`** (`20260926000002_content.sql`). Verify, do not
   re-add or drop the status check.
2. **Apply the migration to the local stack only.** `db:push` reads `DIRECT_URL` from
   `.env.local`; against a real one that is production. Local only, `127.0.0.1:54322`.
3. **The generated module is committed, not built at CI time.** `check:archetypes` (already
   written by the orchestrator) diffs it against a fresh generation. Edit `archetypes.json`
   without regenerating and CI goes red.
4. **Do not invent a 48th archetype or drop a 47th.** The count is a contract. Two names
   collide (`error-cause-pick` vs `error-cause-match`) and four archetypes carry two primitives
   (`estimate`, `complexity`, `trace-the-value`, `impossible-bound`) — the plan spells out both.
5. **You do not touch `web/scripts/check-*.ts` or `ci.yml`.** The staleness gate exists already.

## Verification

Everything in SETUP.md §5, plus `bun run check:archetypes` and `bun run check:rls` /
`check:tracker` / `check:feed` against the local stack. Confirm `check:feed` still passes — the
migration is additive and must not have changed feed behaviour. Report the token count and
bundle KB, and confirm `check:archetypes` passes.

Report back as SETUP.md §10 describes.
