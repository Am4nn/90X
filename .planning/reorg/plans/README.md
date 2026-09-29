# The reorg wave — eight units, one set of rules

Eight agents build the `.planning/reorg/` design in parallel. This file is the part that
is the same for all of them. Read it, then read your own plan, then your brief.

## Reading order

1. **This file** — the wave's rules.
2. **`.planning/briefs/README.md`** — how we code here. It wins over everything below.
3. **Your plan** — `.planning/reorg/plans/<unit>.md`. Exact files, signatures, tests.
4. **Your brief** — `.planning/reorg/<name>.brief.md`. The intent your plan implements.
5. **`.planning/reorg/DECISIONS.md`** — every screen decision, binding.
6. **`.planning/reorg/mocks/`** — the visuals. Open `index.html` in a browser.

Precedence when two of them disagree: **`briefs/README.md` → your plan → DECISIONS → the
brief → PLAN.md → the mocks.** `PLAN.md` is the oldest and has known stale lines.

## Rule one: this is an add-on

The mocks are **visual references, not final designs**. Keep every existing behaviour,
feature and control. Move things, do not delete them. Where a mock differs from today's
behaviour, **today's behaviour wins unless your plan says otherwise**. Do not rewrite a
page from scratch.

## Your worktree and branch

| Unit | Plan | Branch | Worktree |
|---|---|---|---|
| 1a | `1a-shell-me-friends-settings.md` | `me-shell-friends` | `../90X-wt/1a` |
| 1b | `1b-coach-modes-lessons.md` | `coach-lessons` | `../90X-wt/1b` |
| 1c | `1c-today-coach-read.md` | `today-read` | `../90X-wt/1c` |
| 1d | `1d-chat-working-state.md` | `coach-chat` | `../90X-wt/1d` |
| 2 | `2-library-roadmap.md` | `library-roadmap` | `../90X-wt/2` |
| 3 | `3-dsa-problem-page.md` | `problem-page` | `../90X-wt/3` |
| 4 | `4-plan-setup.md` | `plan-setup` | `../90X-wt/4` |
| 5 | `5-coach-mocks.md` | `coach-mocks` | `../90X-wt/5` |

You work **only in your own worktree**. Never switch its branch, never touch another
worktree, never push to `main`.

## Files no unit may touch

Eight branches editing one integer is how a wave of green PRs turns `main` red. These are
the lead's, and a diff that touches them will be sent back:

- `web/scripts/check-tokens.ts`, `check-bundle.ts`, `check-coverage.ts`, `check-shards.ts`
- `.github/workflows/` — anything
- `supabase/migrations/` — anything. If you need a column, **stop and say so in the PR**;
  do not add one. (The one column this wave needed already exists; see unit 4.)
- Generated: `web/src/db/pulled/**`, `web/src/lib/supabase/database.types.ts`
- `web/src/components/coach/ren.tsx` — it exists already; consume it, do not change it.

**If a ceiling fails, do not raise it.** Report the number your branch measured in the PR
under **Checks** and leave the file alone. The lead re-measures on merged `main`.

Your plan also lists the other units' files under **Do not touch**. A conflict there is
out of bounds, not something to resolve.

## Your Playwright spec name is fixed

Every shard in `.github/workflows/ci.yml` already names your spec, so the file must be
called exactly what your plan says. **Playwright takes its positional arguments as
substring filters**, so a name containing `coach`, `today`, `friends`, `feed`, `admin`,
`checkin`, `offline`, `brand` or `a11y` would be claimed by two shards at once and
`check:shards` would refuse it. The names in the plans are chosen to avoid that. Do not
rename, and do not add a second spec file.

## Verification — all of it, by you

You have the database and a browser. Nothing here is handed to the lead. From `web/`:

```bash
bunx oxfmt                 # first: it sorts imports and Tailwind classes
bun run typecheck
bun run lint
bun run test
bun run format:check
bun run check:tokens       # report the number; never edit the ceiling
bun run check:dead
bun run check:dupes
bun run check:cycles
bun run check:coverage
bun run check:deps
bun run check:actions
bun run build && bun run check:bundle     # report the KB; never edit the ceiling
bunx playwright test e2e/<your-spec>.spec.ts
```

Plus the database checks your plan names (`check:rls`, `check:tracker`, `check:friends`,
`check:coach-tools`), and screenshots at **390px and 1440px** of every screen you changed.

TDD for logic: write the test, run it, watch it fail, implement, watch it pass.

## Cross-cutting decisions

These are settled. Do not re-open them, and do not follow `PLAN.md` where it disagrees.

1. **The mobile tab bar stays five tabs** — Today · Feed · Library · Coach · Me. Friends
   is a **desktop sidebar entry only**, reached from Me on a phone. `PLAN.md` §5.1 and D1
   say six tabs and `grid-cols-6`; that is stale and wrong.
2. **`PendingRequests` stays on Today.** Someone with no campaign still has to see friend
   requests. Only *Me* loses it.
3. **Every query stays scoped to the viewer.** Drizzle runs over a connection that
   **bypasses row-level security**, so scoping is the actual defence, not a formality.
   Use `requireViewer()` from `@/lib/auth/viewer`.
4. **No new content, ever.** No lesson text, no problem statements, no card prompts
   written by a model. Everything rendered comes from the database.

## The PR

Open one PR to `main`, titled as a sentence about what changed. Sections:

- **What** — one line per file or area.
- **Decisions** — anything you interpreted, and what it costs if you got it wrong.
- **Checks** — every command above with pass/fail, plus the **measured token count and
  bundle KB**.
- **Not verified** — anything you could not prove.
- **Screenshots** — 390px and 1440px.
- **Suggestions** — optional, and never done in this PR.

End every commit message with:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```
