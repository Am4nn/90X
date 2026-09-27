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
| 1 Pipeline | 3,693 problems, 274 topics and their lessons, 191 pattern tricks, 2,109 roadmap nodes |
| 2 Foundation + Library | Google sign-in, admin approval, setup, Pattern Map, check-ins, LeetCode sync |
| 3 Tracker | Campaign, Today + 90 Grid, review ladder, streak with revive, readiness, Me, push |
| 4 Feed | AI-graded typed answers, spaced repetition, diagnostic, flags, declarations, `/admin/cards` |
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
2. **Ask Aman to review the 25-card sample.** `pipeline card-review` writes
   `.planning/card-review.md`: one sample gates every batch, because reviewing
   20 cards from each of 16 batches is 320 and he said plainly he will not do
   that. It carries the lesson behind each card and every rejected card with
   the gate's reason, so an outside reviewer can judge the gate too.

3. **Finish the knowledge index.** About 1,291 chunks of 10,291 are still not in
   Upstash Vector (the free tier allows 10K/day and the first run took 9,000).
   Run `cd pipeline && .venv/Scripts/python.exe -m pipeline embed`. Coach's
   `search_knowledge` is 87% loaded until then.
4. **Ask the user to check the iPhone hand-off.** With an opaque status bar the
   web view starts below it, so the loading splash may sit ~10–30pt lower than
   the iOS launch image. Needs a real device; the fix is either
   `black-translucent` (then pad for the notch) or per-device offsets.

## The content rebuild (2026-09-28)

Aman read the Library and found it unusable: it was rendering raw scraped
source text as if it were study material - 25,000-character OSTEP chapters,
markdown tables of links, PDF output with broken ligatures - and cards were
generated from those chunks while holding them, so drafts asked about "the
reference solution" the reader never sees. He was right, and `.planning/`
holds the whole story: `content-rebuild.md` measures the damage,
`rebuild-plan.md` is the execution list, `rebuild-dependencies.md` is the
pass over what else broke when documents were deleted.

What replaced it:

- **One authored lesson per topic**, written from that topic's material. The
  model fills fields and we render the Markdown, so every lesson reads the
  same way instead of inheriting the shape of its source. Each carries a
  spoken 60-second answer and a follow-up ladder with answers.
- **Gates, because prompts were not enough.** The old card prompt already
  said "no questions about the text itself" and the drafts leaked anyway. So:
  a structural contract, an independent model fact-checking every claim, and
  for cards an answerability gate that reads the question and nothing else.
- **`documents` is gone from Supabase**, along with `/library/doc` and
  `cards.document_id`. The master copy lives in pipeline staging and the
  vector index, which is all Coach's retrieval needs.
- **Roadmaps** from roadmap.sh as a per-area checklist; only 7% of nodes map
  to a topic, which is expected rather than a gap.
- **Declarations**: the reader tells the Feed "new to me" or "I already know
  this", because the app cannot know what they learned before 90x existed.
  Neither can move a score.

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
- **Four lessons are held back** for claims the fact-checker calls outright
  false, and Aman wants to rule on them himself: `sd-design-a-url-shortener`,
  `two-pointers`, `cs-tlb-and-caching`, `sql-recursive-ctes`.
- **Cross-lesson consistency is not exhaustive.** An area is read in
  overlapping windows of eight, so two lessons far apart in the sort order are
  never compared. It found four real contradictions and missed one that a
  human reading the pack had already spotted.
- **Coach should be able to write a lesson on demand** when the existing ones
  do not cover a question, through the same contract, fact check and
  answerability gates. Agreed, not built.

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
- **The OpenAI SDK waits 600s per attempt and retries twice.** Nothing set a
  timeout, and one stalled request blocked a run for 28 minutes. `llm.py` now
  passes 120s. Low CPU looks the same for working and hung: check whether CPU
  is *increasing* between samples, not whether it is low.
- **A green test suite does not mean the code parses.** A syntax error sat in
  `commands.py` through 114 passing tests because nothing imported it;
  `tests/test_cli.py` now imports every module.
- **`cards.id` is a uuid.** Readable ids like `slug:l0` never publish, and an
  id derived from a card's position moves when the gate changes its mind about
  an earlier card, so study history can attach to a different question. Derive
  it from the question.
- **Deleting a card cascades** to `card_reviews`, `card_state`, `card_flags`
  and `batch_review_items`. `publish` refuses to remove cards holding answers
  or schedules unless forced.
- **Signing in on a preview deployment lands on production.** Supabase Auth
  drops a `redirectTo` that isn't in its allow-list and silently falls back to
  Site URL, so the preview looks like it redirects to prod on purpose. Fix is
  one entry in Authentication → URL Configuration → Redirect URLs:
  `https://90x-*-am4nns-projects.vercel.app/**` (`*` spans hyphens, not dots,
  so it covers both deployment hashes and branch aliases). Note that previews
  then sign in against the **production** database — there is no separate
  Supabase project for them.

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
