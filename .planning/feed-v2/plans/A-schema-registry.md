# Part A — schema and the archetype registry

**Branch** `feed-v2-schema` · **Worktree** `../90X-wt-fv2/a` · **Lead: contains the migration.**

Read `.planning/feed-v2/plans/README.md` first, then `DECISIONS.md`, `PRIMITIVES.md`, `CATALOGUE.md`.

A lands first and **alone**. Everything else codes against the contract defined here. A is
purely additive and non-breaking: the existing app and `e2e/feed.spec.ts` stay green when it
merges.

## Scope

Add the schema columns that let a card carry its archetype, its deterministic answer, and the
observed outcomes the difficulty calibration writes. Create `archetypes.json` (the single
source of truth), the generator that turns it into a typed TS module, and regenerate the pulled
schema. **No UI, no grading, no pipeline card-writing, no seed changes.**

## Files

**Create**
- `supabase/migrations/20260930000024_feed_v2.sql`
- `archetypes.json` — repo root, the 47 archetypes (full table below)
- `web/scripts/generate-archetypes.ts` — reads `archetypes.json`, writes the module
- `web/src/lib/feed/archetypes.ts` — generated; commit it, never hand-edit
- `web/src/lib/feed/archetypes.test.ts` — the round-trip: every archetype id resolves, every
  primitive is known, every area is one of the five

**Modify (regenerate only, via commands)**
- `web/src/db/pulled/**`, `web/src/lib/supabase/database.types.ts` — run `bun run db:pull` and
  `bun run db:types` against the **local** stack after applying the migration

**Do not touch**
- `web/scripts/check-*.ts` — including `check-archetypes.ts`, which the orchestrator already
  wrote; your job is to make its inputs exist and agree.
- `.github/workflows/ci.yml`, `web/e2e/feed.spec.ts`, `web/e2e/seed-data.ts`
- every file another part owns (see README). `web/src/db/schema.ts` already re-exports
  `./pulled/*` — leave it.

## The migration

Additive only. Never drop a column, never rewrite existing rows.

```sql
-- cards.format becomes the primitive id going forward; the old enum is a dead letter.
alter table public.cards drop constraint if exists cards_format_check;

alter table public.cards
  add column archetype   text,              -- id from archetypes.json
  add column picked      jsonb,             -- correct indices, shape "chosen"
  add column constraints jsonb,             -- ordering constraints, shape "ordered"
  add column pairs       jsonb,             -- one-to-one [[l,r],...], shape "mapping"
  add column value       double precision,  -- expected number, shape "number"
  add column tolerance   double precision,  -- |given - expected| <= tolerance
  add column why_step    jsonb,             -- { options: string[], correct: number } | null
  add column observed_attempts integer not null default 0,
  add column observed_correct integer not null default 0;

-- The Feed's deterministic graders write "pure"; keep the old values for legacy rows.
alter table public.card_reviews drop constraint if exists card_reviews_graded_by_check;
alter table public.card_reviews add constraint card_reviews_graded_by_check
  check (graded_by = any (array['pure','self','skip','declared','match','ai','options']));
```

`cards.status` already allows `retired` (from `20260926000002_content.sql`) — verify, do not
re-add. The structured answer is stored **serialised as JSON in `card_reviews.answer`** (text),
so no new review column is needed; Part B owns the serialiser.

## The answer contract (what the columns store)

```ts
type Answer =
  | { shape: "chosen"; picked: number[] }
  | { shape: "ordered"; order: number[] }
  | { shape: "mapping"; pairs: [number, number][] }
  | { shape: "number"; value: number };
```

A why-step, where present, is a **second `chosen` answer** stored in `why_step`. The columns
map to the shapes as the comment above says; `ordered` cards store **constraints, not one
blessed sequence** (DECISIONS round 2).

## `archetypes.json` — the registry

```json
{
  "version": 1,
  "answerShapes": ["chosen", "ordered", "mapping", "number"],
  "primitives": [
    { "id": "pick_one",     "shape": "chosen"  },
    { "id": "order",        "shape": "ordered" },
    { "id": "match",        "shape": "mapping" },
    { "id": "bucket",       "shape": "mapping" },
    { "id": "tap_in_place", "shape": "chosen"  },
    { "id": "self_rate",    "shape": null      },
    { "id": "assemble",     "shape": "ordered" },
    { "id": "numeric",      "shape": "number"  },
    { "id": "claim_grid",   "shape": "mapping" },
    { "id": "grid_toggle",  "shape": "chosen"  }
  ],
  "archetypes": [ /* 47 entries, below */ ]
}
```

`self_rate` has no answer shape (the reader declares got/missed). "Pick, then justify" is **not**
a primitive: it is the `why_step` modifier (DECISIONS round 4).

### The 47 archetypes

Areas are the five Feed domains: `dsa`, `system_design`, `cs`, `java`, `sql`. Behavioural is
deliberately absent — no behavioural cards are generated (DECISIONS round 2).

| id | primitives | areas | whyStep |
|---|---|---|---|
| concept | pick_one | dsa system_design cs java sql | yes |
| complexity | pick_one, numeric | dsa java sql | yes |
| which-approach | pick_one | dsa system_design sql | yes |
| what-breaks-first | pick_one | system_design | yes |
| output-prediction | pick_one | dsa java sql | yes |
| counter-example | pick_one | dsa java sql | yes |
| trace-the-value | pick_one, numeric | dsa java | yes |
| failure-diagnosis | pick_one | system_design cs sql | yes |
| threshold | pick_one | system_design cs sql | yes |
| consequence-of-diff | pick_one | dsa java cs | yes |
| estimate | pick_one, numeric | system_design | yes |
| missing-step | pick_one | system_design cs sql | yes |
| next-step | pick_one | dsa system_design cs | yes |
| which-invariant | pick_one | dsa | yes |
| which-is-not-true | pick_one | dsa system_design cs java sql | yes |
| which-test-catches | pick_one | dsa java sql | yes |
| read-query-plan | pick_one | sql | yes |
| error-cause-pick | pick_one | java sql cs | yes |
| impossible-bound | pick_one, numeric | dsa | yes |
| odd-one-out | pick_one | dsa system_design cs java sql | yes |
| all-that-apply | claim_grid | dsa system_design cs java sql | yes |
| which-invariants-hold | claim_grid | dsa cs | yes |
| sequence | order | system_design cs dsa sql | yes |
| rank-by-metric | order | dsa system_design sql | yes |
| timeline | order | system_design cs | yes |
| dependency-order | order | system_design cs sql | yes |
| interleaving | order | cs java | yes |
| term-meaning | match | java sql cs | yes |
| error-cause-match | match | java cs system_design | yes |
| pattern-signal | match | dsa | yes |
| operation-complexity | match | dsa java | yes |
| api-guarantee | match | system_design | yes |
| two-way | bucket | system_design cs sql | yes |
| three-way | bucket | system_design sql | yes |
| which-layer | bucket | system_design | yes |
| tap-the-bug | tap_in_place | dsa java sql | yes |
| tap-the-bottleneck | tap_in_place | system_design sql | yes |
| tap-the-insertion-point | tap_in_place | dsa java sql | yes |
| tap-the-unsafe-line | tap_in_place | java sql system_design | yes |
| fill-code-blank | assemble | dsa java sql | yes |
| fill-definition | assemble | cs java sql | yes |
| fill-signature | assemble | java | yes |
| fill-clause | assemble | sql | yes |
| flash | self_rate | dsa system_design cs java sql | **no** |
| complexity-table | grid_toggle | dsa java | yes |
| isolation-behaviour | grid_toggle | sql | yes |
| method-semantics | grid_toggle | system_design | yes |

Count check: 20 pick-one + 2 claim-grid + 5 order + 5 match + 3 bucket + 4 tap-in-place +
4 assemble + 1 self-rate + 3 grid-toggle = **47**.

`whyStep` is false for `flash` only — self-rate has no correct answer, so there is no reason to
pick. Every other archetype can carry a why-step; the pipeline adds it to Hard cards (Part E).

`difficulty` defaults to `["Easy","Medium","Hard"]` for every archetype **except `flash`, which
is `["Easy"]`**. The design never states per-archetype ranges; this default is a decision — see
below.

### Two name collisions resolved (encode exactly these)

- `error-cause-pick` (pick one, "read a real error message and pick the cause") and
  `error-cause-match` (match, "match each exception to what causes it") are **two distinct
  archetypes**. CATALOGUE.md round 1 calls the second "Error ↔ cause" and round 2 reuses the
  name for the first. The ids above disambiguate.
- `estimate`, `complexity`, `trace-the-value`, `impossible-bound` carry **two primitives**
  (`pick_one` and `numeric`). Same archetype, two screens; the pipeline picks per card. Do not
  split them into two rows.

## The generated module — `web/src/lib/feed/archetypes.ts`

`generate-archetypes.ts` emits, and the module must export exactly:

```ts
export const PRIMITIVES = [/* { id, shape } */] as const;
export type Primitive = (typeof PRIMITIVES)[number]["id"];
export type AnswerShape = "chosen" | "ordered" | "mapping" | "number";
export const ARCHETYPES = [/* { id, label, primitives, areas, difficulty, whyStep } */] as const;
export type ArchetypeId = (typeof ARCHETYPES)[number]["id"];
export function shapeOf(primitive: Primitive): AnswerShape | null;
export function archetype(id: ArchetypeId): (typeof ARCHETYPES)[number] | undefined;
```

`shapeOf("self_rate")` returns `null`. The generator writes a header comment `// generated from
archetypes.json — do not edit` so the staleness check and reviewers both see it.

**The generator's export is already depended on.** `web/scripts/check-archetypes.ts` (the
orchestrator's, already committed) does `await import(...generate-archetypes.ts)` and calls
`generateArchetypesModule(json): string`. Your generator must export exactly
`generateArchetypesModule(json: unknown): string`, returning the exact module text including the
trailing newline, deterministically (stable ordering) so the check's byte-comparison holds. The
`generate:archetypes` and `check:archetypes` npm scripts already exist in `web/package.json`.

## Tests

`web/src/lib/feed/archetypes.test.ts` (Vitest, pure — no database):

- **47 archetypes, no duplicate ids**, and every id in `ARCHETYPES` round-trips through
  `archetype(id)`.
- **every primitive an archetype names is in `PRIMITIVES`**, and `shapeOf` returns the right
  shape for all ten, `null` for `self_rate`.
- **every area is one of the five**, and `flash` is the only archetype with `whyStep: false`.
- **the four dual-primitive archetypes** (`estimate`, `complexity`, `trace-the-value`,
  `impossible-bound`) name exactly `["pick_one", "numeric"]`.

## Traps

- **`cards.status` already allows `retired`.** `20260926000002_content.sql` line 98 has it.
  Do not `add column` or `drop constraint` for status; just confirm.
- **Apply to the local stack only.** `bun run db:push` reads `DIRECT_URL` from `.env.local`;
  if that ever points at the hosted project you are on production. Start local Supabase, write
  `.env.local` against `127.0.0.1:54322` (see `prompts/SETUP.md`), and use `db:reset`/`db:push`
  there. Never run against `DIRECT_URL` from a real `.env.local`.
- **`db:pull` regenerates `pulled/**`; `db:types` regenerates `database.types.ts`.** Commit both.
  Do not hand-edit them. Do not commit a stray `.env.local` or `.data/`.
- **The generated module is committed, not built at CI time.** `check:archetypes` (already
  written) diffs the committed file against a fresh generation and fails when they disagree. If
  you edit `archetypes.json` without regenerating, CI goes red.
- **Do not invent a 48th archetype or drop a 47th.** The count is a contract. If CATALOGUE.md
  seems to imply something else, encode the table above and flag the discrepancy in the PR.
- **No new `check-*.ts`, no `ci.yml` edit.** The staleness gate already exists.

## Verification

From `web/`: `bunx oxfmt`, `typecheck`, `lint`, `test`, `format:check`, `check:tokens`,
`check:dead`, `check:dupes`, `check:cycles`, `check:coverage`, `check:deps`, `check:actions`,
`build && check:bundle`, and `bun run check:archetypes`. Database: `bun run check:rls`,
`check:tracker`, `check:feed` — all against the local stack with the migration applied.

Report the token count and bundle KB, plus confirmation that `check:archetypes` passes and that
`check:feed` still passes (the additive migration must not have changed feed behaviour).

## Decisions (with cost if wrong)

- **`difficulty` defaults to all three except `flash` (Easy only).** Cost if wrong: the pipeline
  could ask for a Hard `flash` card, which is meaningless (no wrong answer). One guard in the
  registry and one in the generator is enough.
- **`whyStep: false` only for `flash`.** Cost if wrong: a Hard card whose "reason" cannot exist
  would make the right-answer-wrong-reason rule unanswerable. Gate 3 is where the rule itself is
  judged.
- **Answer stored serialised in `card_reviews.answer` text, not a new jsonb column.** Cost if
  wrong: querying a structured answer later needs a parse, but nothing consumes the answer text
  today except the review screen, which can parse.
