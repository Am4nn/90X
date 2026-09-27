# 90x handoff

Written 2026-09-28 at the end of the build session that took 90x from a spec to a
working app. Read this, then `.planning/SPEC.md`. Everything below is true of
`main` at commit `78b7c9b`.

## What 90x is

An invite-only interview-prep app for Aman (125aryaaman@gmail.com) and a few
friends. Live at **https://90x.amanarya.com** (Vercel project
`am4nns-projects/90x-web`, region `bom1`; Supabase in Mumbai). Repo
**github.com/Am4nn/90x**, single branch `main`, protected.

All five MVP parts are built and merged:

| Part | What it does |
|---|---|
| 1 Pipeline | 3,693 problems, 5,290 notes, 274 topics, 191 pattern tricks, 8,556 cards |
| 2 Foundation + Library | Google sign-in, admin approval, setup, Pattern Map, check-ins, LeetCode sync |
| 3 Tracker | Campaign, Today + 90 Grid, review ladder, streak with revive, readiness, Me, push |
| 4 Feed | AI-graded typed answers, spaced repetition, diagnostic, flags, `/admin/cards` |
| 5 Coach | Tool-using chat, memory, solution review, pattern lessons, mocks, STAR, weekly review |

Plus: installable app with offline Today/Feed, Playwright in CI, brand icons and
splash, Sentry + Vercel Analytics + Speed Insights.

## How this project is built (keep doing this)

The user has cloud-session credits and wants them spent. The pattern that worked:

1. **The lead (you) writes a brief** into `.planning/briefs/<name>.md`. Every brief
   points at `.planning/briefs/README.md`, which holds the house rules: how we
   code, the design rules, every check to run, the PR format, and "decide, don't
   ask the owner".
2. **The user starts a cloud session** on claude.ai/code against this repo with:
   `Read .planning/briefs/README.md, then do .planning/briefs/<name>.md exactly.
   Don't ask questions: decide and list decisions in the PR. Finish with a PR to main.`
3. **The lead watches** `gh pr list` with a Monitor, then for each PR: reads it,
   merges `main` into the PR branch locally, resolves conflicts, **runs the
   real-database checks the agent could not**, and merges with
   `gh pr merge <n> --squash --admin --delete-branch`.

Three sessions at a time is comfortable. Cloud agents cannot reach the database,
AI keys or a browser, so the lead always verifies those parts. That is how the
serious bugs were caught (see below).

## Do this next, in order

1. **Read the Sentry error.** The user has just filled `SENTRY_READ_TOKEN` in
   `web/.env.local` (scopes `event:read`, `project:read`, `org:read`). Pull the
   issues from `https://sentry.io/api/0/projects/$SENTRY_ORG/$SENTRY_PROJECT/issues/`
   with that token and fix what it found. One real error was captured in
   production and has never been looked at.
2. **Ask the user to review card batches.** `/admin/cards` holds 13 batches of
   drafts; 18 of 20 good publishes one. **The Feed serves nothing until at least
   one batch is published.** This is the single biggest gap between "built" and
   "usable".
3. **Finish the knowledge index.** About 1,291 chunks of 10,291 are still not in
   Upstash Vector (the free tier allows 10K/day and the first run took 9,000).
   Run `cd pipeline && .venv/Scripts/python.exe -m pipeline embed`. Coach's
   `search_knowledge` is 87% loaded until then.
4. **Ask the user to check the iPhone hand-off.** With an opaque status bar the
   web view starts below it, so the loading splash may sit ~10–30pt lower than
   the iOS launch image. Needs a real device; the fix is either
   `black-translucent` (then pad for the notch) or per-device offsets.

## Known open items (none are blocking)

- **A coach answer is lost if the app is closed mid-generation.** The reply lives
  only in the open connection until it is saved. The app now warns about this
  after 4s. The real fix is a resumable run (drive it with QStash, store
  progress, let the client reconnect) — designed but not built.
- **Weekly review windows on UTC Monday**, not the user's local Monday
  (`lib/coach/weekly.ts`). Kolkata loses about 5.5h of the week.
- **Duplicated helpers** across files: `BAND_TEXT` ×4, `DAY_NAMES` ×4, slot labels
  ×3, language labels ×3, `timezoneOf` ×2; `coach/act.ts` re-implements the
  Feed's Redis queue format instead of calling the Feed service.
- **17 more minor findings** are listed in PR #11's description (the whole-app
  review). Read it before starting new work in an area.
- **Cards for ~36 DSA problems** were cut off when the pipeline hit its $22 cap,
  and 13 more failed on invalid JSON. A re-run costs about $0.15.

## Things that bite (learned the hard way)

- **`drizzle-kit pull` mangles column names** containing a digit followed by a
  letter: `p256dh` came back as `p256Dh` with no explicit name, so **web push
  silently never worked**. `scripts/fix-pulled-schema.ts` now repairs this. After
  any `db:pull`, check the diff.
- **DeepSeek bills hidden thinking tokens** that are missing from
  `completion_tokens`. Our cost log was 5× under the real bill until we started
  counting `total_tokens - in - out`. Short structured calls pass
  `providerOptions: NO_THINKING` (from `@/lib/ai`).
- **Correlated subqueries in Drizzle**: a bare column renders as `"id"`, which
  inside a subquery means the subquery's own table. Spell out table names
  (`lib/admin/cards.ts` has the pattern).
- **Next 16 error boundaries take `retry`, not `reset`.** Read
  `web/node_modules/next/dist/docs/` before writing framework code; `web/AGENTS.md`
  says the same.
- **The React Compiler lint rule forbids a synchronous `setState` in an effect.**
  Reset such state in the event handler instead.
- **Vercel Hobby allows 300s** when Fluid Compute is on (it is, by default). A
  route timing out at 60s was our own `maxDuration = 60`, not the plan.

## Verifying work

From `web/`: `bun run typecheck`, `lint` (ESLint + oxlint, zero warnings),
`test` (Vitest), `format:check` (run `bunx oxfmt` to fix), `check:tokens`
(design tokens; the ratchet may only fall), `check:dead` (knip), `build`.

Against the real database (these need `.env.local`, so only the lead can run
them): `check:rls` (29 checks), `check:tracker` (22), `check:feed` (14),
`check:coach-tools` (15). With real AI keys and a few cents:
`check:grading` (12 fixed answers), `check:coach` (memory extraction end to end).

CI runs everything except the AI ones, plus Playwright browser tests against a
throwaway Supabase, a Redis stand-in and a fake model (`web/e2e/fake-model.ts`,
an OpenAI-compatible server with fixed replies), so the Coach specs never call
a real model.

## Conventions

- Commit straight to `main` for lead-side work; everything from an agent comes
  through a PR. Never skip hooks.
- The user wants: short answers in bullets, menus (`AskUserQuestion`) for real
  decisions, no shortcuts when something looks wrong, and proof rather than
  claims. He pushed back correctly when a number was guessed instead of measured.
- Ask before spending on AI runs. The pipeline cap is `PIPELINE_MAX_USD` (raised
  to $22 once, with permission); the app's budget is $10/month in `ai_usage`
  and a Redis meter.
- Server code uses Drizzle over a connection that **bypasses row-level
  security**, so every query must be scoped to the signed-in user or admin-gated.
  `check:rls` and `check:coach-tools` exist to prove it.
- Design: spec §7 only — six text sizes, token colours, borders not shadows,
  dark only, no native selects on desktop. `check:tokens` enforces it.
