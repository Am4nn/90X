# 90x handoff

Rewritten 2026-09-29. The previous version was written on 2026-09-28 and went
stale within a day: it listed as open eight things that were already done, named
four held lessons that had since been rewritten, and said the DeepSeek account
was empty when it had been topped up. **Verify any "known open item" against the
code before acting on it** — that habit is the single most useful thing in this
file.

Read this, then `.planning/SPEC.md`. The app is `main` at `eed4f49`. Work in
flight is branch `source-grounding` (no PR yet); see **Work in flight**.

## What 90x is

An invite-only interview-prep app for Aman (125aryaaman@gmail.com) and a few
friends. Live at **https://90x.amanarya.com** (Vercel project
`am4nns-projects/90x-web`, region `bom1`; Supabase in Mumbai). Repo
**github.com/Am4nn/90x**, `main` protected.

All five MVP parts are built and merged, and so is the content rebuild
(PRs #19–#22):

| Part | What it does |
|---|---|
| 1 Pipeline | 3,693 problems, 274 topics and their lessons, 191 pattern tricks, 2,109 roadmap nodes |
| 2 Foundation + Library | Google sign-in, admin approval, setup, Pattern Map, check-ins, LeetCode sync |
| 3 Tracker | Campaign, Today + 90 Grid, review ladder, streak with revive, readiness, Me, push |
| 4 Feed | AI-graded typed answers, spaced repetition, diagnostic, flags, declarations, `/admin/cards` |
| 5 Coach | Tool-using chat, memory, solution review, pattern lessons, mocks, STAR, weekly review |

Plus: installable app with offline Today/Feed, Playwright + axe in CI, brand
icons and iOS launch images, Sentry + Vercel Analytics + Speed Insights.

## The one content rule that overrides everything

**Lesson and card content is written from sources we downloaded, never from a
model's own knowledge.** Aman's words:

> "I dont want AI writing content as many problems are there but always go with
> sources we have download from there and then create lesson out of it or feed
> things etc… always source based"

This is not a style preference. A lesson invented from memory is the one failure
the downstream gates cannot catch: it satisfies the structural contract, reads
perfectly well, and the fact-checker is another model with the same gaps. It
cites nothing and nothing notices.

`pipeline/src/pipeline/lessons/run.py` raises `NoSource` rather than calling the
model when a topic yields no reference or under 400 characters of context.
**Do not weaken or bypass that guard.** Widening what *counts* as a source is
the right move instead — assigned documents, unassigned documents whose title
overlaps, roadmap.sh node text, and a DSA pattern's own problem statements all
qualify, because all of them were downloaded. A topic with genuinely nothing
stays held and this file says why.

## How this project is built (keep doing this)

Aman has cloud-session credits and wants them spent. The pattern that worked:

1. **The lead writes a brief** into `.planning/briefs/<name>.md`. Every brief
   points at `.planning/briefs/README.md`, which holds the house rules: how we
   code, the design rules, every check to run, the PR format, and "decide, don't
   ask the owner".
2. **Aman starts a cloud session** on claude.ai/code against this repo with:
   `Read .planning/briefs/README.md, then do .planning/briefs/<name>.md exactly.
   Don't ask questions: decide and list decisions in the PR. Finish with a PR to main.`
3. **The lead watches** `gh pr list`, then for each PR: reads it, merges `main`
   into the PR branch locally, resolves conflicts, **runs the real-database
   checks the agent could not**, and merges with
   `gh pr merge <n> --squash --admin --delete-branch`.

Three sessions at a time is comfortable. Cloud agents cannot reach the database,
AI keys or a browser, so the lead always verifies those parts. That is how the
serious bugs were caught.

A brief may describe a sibling project's code, because a cloud session cannot
read one. `.planning/briefs/friends.md` does this at length for Curfew.

## Work in flight

Branch **`source-grounding`**, cut from `main` at `eed4f49`. Not yet a PR.

| Commit | What |
|---|---|
| `66c9a2d` | Lessons read the whole downloaded corpus, including problem statements |
| `bde3992` | `queueFirst` — the Coach stops writing the Feed's queue by hand |
| `80fbf56` | Slot and language label maps, coach prompt naming |
| `315b23d` | A coverage floor, and 40 KB off every cold start |
| `9d4c2db` | A follow-up may set the scene before it asks |
| `914d9a4` | A brief for the friend graph |

Every local gate passed at `315b23d`. Before the PR: re-run them, then wait for
CI **and both reviewers clean on the same commit**, then squash-merge.

## Do this next, in order

1. **Top up Gemini** — see the first known open item. Everything below that
   touches a model is blocked on it.
2. **Re-run cross-lesson consistency (~$1.40).** It was run and its five
   contradictions were fixed (`.planning/lesson-contradictions.md`) — and then
   every lesson was rewritten underneath it, so that pass no longer describes
   the current text. It is not exhaustive either: an area is read in overlapping
   windows of eight, so two lessons far apart in the sort order are never
   compared.
3. **Build the friend graph** — `.planning/briefs/friends.md`, written and
   reviewed, waiting on a session. Today every approved user sees every other
   approved user. Needs no model, so it is not blocked.
4. **Read the Sentry error.** `SENTRY_READ_TOKEN` is in `web/.env.local`
   (scopes `event:read`, `project:read`, `org:read`). Pull
   `https://sentry.io/api/0/projects/$SENTRY_ORG/$SENTRY_PROJECT/issues/`.
   One real production error was captured and, as far as this file knows, has
   still never been looked at — **check before assuming that is still true.**

## Waiting on Aman (he has said that is fine)

- **Approve card batches in `/admin/cards`.** This is the one thing gating the
  Feed: nothing is `live`, so the Feed serves nothing until he approves.
  `.planning/card-review.md` is the sample — 25 cards, each beside the lesson it
  came from, plus every card the gate rejected with its reason. One sample gates
  every batch, because reviewing 20 cards from each of 16 batches is 320 and he
  said plainly he will not do that.
- **Read a lesson on a real screen.**
- **Check the iPhone splash hand-off on a device.** With an opaque status bar the
  web view starts below it, so the loading splash may sit ~10–30pt lower than the
  iOS launch image. The fix is either `black-translucent` (then pad for the
  notch) or per-device offsets.
- **Cut `.planning/taxonomy-proposal.md` down** from its recommended 46 of 94.

## The content rebuild, and the re-grounding after it

Aman read the Library and found it unusable: it was rendering raw scraped source
text as if it were study material — 25,000-character OSTEP chapters, markdown
tables of links, PDF output with broken ligatures — and cards were generated
from those chunks, so drafts asked about "the reference solution" the reader
never sees. He was right. `.planning/content-rebuild.md` measures the damage,
`rebuild-plan.md` is the execution list, `rebuild-dependencies.md` covers what
else broke when documents were deleted.

What replaced it:

- **One authored lesson per topic.** The model fills fields and we render the
  Markdown, so every lesson reads the same way instead of inheriting the shape
  of its source. Each carries a spoken 60-second answer and a follow-up ladder
  with answers.
- **Gates, because prompts were not enough.** The old card prompt already said
  "no questions about the text itself" and the drafts leaked anyway. So: a
  structural contract, an independent model fact-checking every claim, and for
  cards a five-stage gate (schema → grounding → answerable → format fit →
  gradable) whose first two stages are deterministic code, not a model.
- **`documents` is gone from Supabase**, along with `/library/doc` and
  `cards.document_id`. The master copy lives in pipeline staging and the vector
  index, which is all Coach's retrieval needs.
- **Roadmaps** from roadmap.sh as a per-area checklist; only 7% of nodes map to a
  topic, which is expected rather than a gap.
- **Declarations**: the reader tells the Feed "new to me" or "I already know
  this", because the app cannot know what they learned before 90x existed.
  Neither can move a score.

**Then the re-grounding (2026-09-29).** Lessons only ever read documents assigned
to their own topic, and 2,346 of 5,290 downloaded documents have no topic at all
— so 44% of the corpus was invisible to lesson writing, and 39 published lessons
had been written from a roadmap.sh paragraph alone, including `sliding-window`,
`arrays-hashing`, `trees`, `binary-search`, `graphs` and
`1-d-dynamic-programming`. The most important topics in the app were the thinnest
sourced. Meanwhile 3,693 problem statements sat keyed to those exact patterns and
no lesson read one.

`lessons/context.py` `for_topic()` now assembles four kinds of material in order:
roadmap notes, assigned documents, problem statements, then unassigned documents
whose title overlaps. Problem refs are `<source_id>:<slug>`
(`leetcode-detailed:two-sum`), **not** `problem:<slug>` — `publish._source_rows()`
already publishes every source id used by `problems` and `_sources_of()` keys on
the prefix, so the "Written from" line credits LeetCode with no code change,
where a `problem:` prefix would have resolved to nothing and silently dropped the
credit.

Result over 274 topics, $8.61:

| | |
|---|---|
| Roadmap-only lessons | **39 → 1** (`beh-prioritization`, a behavioural topic with no corpus) |
| Source refs | 1,595 document · 1,027 roadmap · 138 problem |
| `simulation` | was held with no source; now 1,161 words from 10 LeetCode statements |
| `beh-teamwork` | **still held.** 0 refs, 0 characters. One document mentions teamwork and it is about questions to ask an interviewer. It stays held until something is downloaded for it — it will not be written from memory. |

## Known open items

- **BLOCKING: the Gemini key's AI Studio *project* has no prepay credit left.**
  `402` on every model tried (`gemini-3.8-flash`, `gemini-3.5-flash`,
  `gemini-3.5-flash-lite`), so it is account-level, not a model or quota problem.
  AI Studio prepay is **per project**, and the error says so: "manage your
  project and billing". Aman reports a Gemini balance, so it is almost certainly
  on a different project than this key. A project with no billing at all returns
  `429`, not `402`, so this project is on prepay and the prepay is spent.

  The same key is in both `pipeline/.env` (`REVIEW_API_KEY`) and
  `web/.env.local` (`GEMINI_API_KEY`) — 53 characters, prefix `AQ.Ab8R`,
  `sha256` beginning `c2090209`. Either issue a key in the project that holds the
  balance and replace it in both files, or add prepay to this key's project.

  Gemini is the review tier — the independent fact-checker on every lesson — so
  **no `pipeline lessons`, `lesson-cards`, `cards` or `consistency` run can
  finish until this is sorted.** DeepSeek still works, so a run produces text and
  then fails at verification: the right way round, but it spends DeepSeek tokens
  to reach the wall.
- **`beh-teamwork` has no source material** and is therefore not in the Library.
  Confirmed twice, including after the `spare_documents` cap was removed and all
  2,071 unassigned documents became visible: it still resolves to 0 refs. Either
  download something for it or leave it held.
  - Its staging row still holds an **841-word body with `source_refs = []` and
    `generated_at 2026-09-28`** — text from the pre-rebuild era, written from the
    model's own memory, which is the one thing the source rule forbids. It is
    inert (`status = 'failed'`, and `publish` only sends `status = 'ok'`) and a
    successful rewrite would overwrite it, so it was left alone rather than
    quietly deleted. **Do not flip its status by hand.** If you want it gone,
    `update lessons set body_md = '' where topic_slug = 'beh-teamwork'`.
- **Cross-lesson consistency is stale and not exhaustive** — see "Do this next".
  It needs Gemini, so it is blocked on the item above.
- **Every approved user can see every other approved user.** There is no friend
  graph; `lib/tracker/me.ts:42` says "You and every approved friend" and means
  every approved user. Three leaks come with it: `profiles_read` hands a friend
  the whole profile row including `leetcode_username` and notification
  preferences; `notifyFriends` (`lib/push.ts:65`) pushes every check-in to every
  opted-in user; `friendActivity` returns full names beside a scoreboard showing
  first names. `.planning/briefs/friends.md` fixes all of it.
- **The 292 KB shared bootstrap has not been broken down.** `check:bundle`
  measures and ratchets it, and removing Sentry Session Replay took 40 KB off
  (`web/src/instrumentation-client.ts` documents exactly how to restore it and
  why lazy-loading cannot substitute), but nobody has read the remaining chunk
  contents.
- **Remaining findings from PR #11** (the whole-app review) are in its
  description. Several are now done — check each against the code before acting.

## Things that bite (learned the hard way)

### Shell and tooling on this machine

- **Bash heredocs mangle backslash escapes.** `\b` in a regex became a literal
  `\x08` byte in `gaps.py` and silently broke a coverage check; `\n` became real
  newlines several times. **Write the patch to a scratchpad `.py` file and run
  that**, or use the Edit tool. This trap has now been hit on three separate
  days.
- **`jq` is not installed.** Three `Monitor` watches silently produced nothing
  for 30 minutes each. Use `gh --jq` instead.
- **`gh run list --limit 1` can return a stale run.** Pin the commit SHA, or you
  will read yesterday's result as today's.
- **`gh pr merge --admin` reports `fatal: Not possible to fast-forward` when the
  merge succeeded.** Only the stale local `main` update failed. Check the PR
  before re-running anything.
- **The staging DuckDB takes an exclusive lock** (`.data/staging.duckdb`, at the
  repo root, not under `pipeline/`). One pipeline command at a time.

### Gates and measurement

- **A ratchet on a non-deterministic measure needs tolerance in one direction
  only.** `check:bundle` once failed at 292 KB local against a 291 KB ceiling set
  in CI — failing *under* budget, which is wrong for a gzip byte count. It now
  fails only when over, with 5% slack before it suggests tightening.
  `check:coverage` does the same for v8 branch counting (`SLACK = 0.5`). Counted
  items (dead exports, duplicate blocks, cycles) need no tolerance.
- **Don't change production code off a single red CI run when the test is new and
  timing-dependent.** A coach test failed once and I concluded `consumeSseStream`
  was insufficient; run `45a3e6f` had passed with identical code, so the test was
  flaky and the conclusion was wrong.
- **A green test suite does not mean the code parses.** A syntax error sat in
  `commands.py` through 114 passing tests because nothing imported it;
  `tests/test_cli.py` now imports every module.
- **Grep `getByLabel` before changing an accessible name.** The mission square's
  `aria-label` was wrong three times: labelling all four squares double-announced,
  hiding all four removed the state and broke locators in three Playwright specs.
  Settled by making the square own the state (`role="img"`) and hiding the
  redundant text.

### The pipeline

- **One lock per DuckDB connection** (`llm.lock_for`). The runners each held a
  lock of their own while `LLM` held a second over the same connection, so a
  worker's select could interleave with another worker's cost log; the select came
  back short, `dict(zip(cols, row))` dropped the keys it had no values for, and
  two topics of 274 died on `KeyError: 'title'` with no traceback.
- **DeepSeek bills hidden thinking tokens** missing from `completion_tokens`. The
  cost log was 5× under the real bill until we counted `total_tokens - in - out`.
  Short structured calls pass `providerOptions: NO_THINKING` (from `@/lib/ai`).
- **The OpenAI SDK waits 600s per attempt and retries twice.** Nothing set a
  timeout and one stalled request blocked a run for 28 minutes; `llm.py` now
  passes 120s. Low CPU looks the same for working and hung — check whether CPU is
  *increasing* between samples, not whether it is low.
- **A follow-up is setup then ask, and must never answer itself.** `any()` let an
  answer hide behind a question ("What breaks under load? The lock serializes
  every request."); `all()` then rejected the setup-then-ask phrasing interviewers
  actually use ("Your team has a method with a long chain of instanceof checks.
  How would you refactor it?"). The rule is: statements may lead, and once a
  sentence prompts, every sentence after it must prompt too.
- **`cards.id` is a uuid.** Readable ids like `slug:l0` never publish, and an id
  derived from a card's position moves when the gate changes its mind about an
  earlier card, so study history can attach to a different question. Derive it
  from the question.
- **Keying a fix by topic slug rewrites the wrong card.** A topic has about ten
  cards, so 12 of 13 reviewer objections landed on a card the reviewer had never
  seen. `.planning/card-objections.md` entries now carry a `match:` fragment and
  `cards/fix.py` `pick()` returns `None` rather than guessing.
- **`confidence_of` keyed by list index, looked up by `id(card)`** — so every card
  scored 0.5 and the review sample was never risk-weighted. `confidence_by_card`
  keys both ends the same way.
- **A lesson mention is not coverage.** `gaps.taught_in` treated one as settled
  and hid 230 real gaps; 539 clobbered verdicts had to be recovered from a report
  committed at `132e68e`. Mentions now annotate rather than settle.
- **Deleting a card cascades** to `card_reviews`, `card_state`, `card_flags` and
  `batch_review_items`. `publish` refuses to remove cards holding answers or
  schedules unless forced. What counts as "staging still has this card" is `kept`,
  not the row's presence: a rejected card keeps its row, so matching on presence
  left a card a later run had rejected live in the Feed for good.
- **`publish` is the only path to Supabase, and it converges.** `rebatch` writes
  to staging alone. It used to write to both, which worked only while the cards
  were already up there: the first batch built before its first publish was
  marked published, and publish sends what is not published, so 2,692 cards were
  grouped and would never have been sent. `risk` and `label` travel in staging
  for the same reason — written straight to Supabase they missed any card
  published afterwards, and `pickReviewSample` sorts risk ascending, so a null
  card reads as the safest in the batch.

### The app

- **`drizzle-kit pull` mangles column names** containing a digit followed by a
  letter: `p256dh` came back as `p256Dh` with no explicit name, so **web push
  silently never worked**. `scripts/fix-pulled-schema.ts` repairs it. After any
  `db:pull`, read the diff.
- **Correlated subqueries in Drizzle**: a bare column renders as `"id"`, which
  inside a subquery means the subquery's own table. Spell out table names
  (`lib/admin/cards.ts` has the pattern).
- **Stopping a coach run needs an out-of-band signal.** Aborting the request only
  hid the reply while the server kept generating and saved it. `lib/coach/stop.ts`
  writes a Redis timestamp; nothing clears the flag and a run ignores any stop
  older than itself. In `api/coach/chat/route.ts`, `startedAt` is read before any
  await, and the stop handle is declared **outside** the `try` — inside it,
  `stop?.done()` resolved to `lib.dom`'s global `stop()` and was a silent no-op.
  The stream is `tee()`d so the client and the store both get it.
- **Next 16 error boundaries take `retry`, not `reset`.** Read
  `web/node_modules/next/dist/docs/` before writing framework code; `web/AGENTS.md`
  says the same.
- **The React Compiler lint rule forbids a synchronous `setState` in an effect.**
  Reset such state in the event handler instead.
- **Vercel Hobby allows 300s** when Fluid Compute is on (it is, by default). A
  route timing out at 60s was our own `maxDuration = 60`, not the plan.
- **Signing in on a preview deployment lands on production.** Supabase Auth drops
  a `redirectTo` that isn't allow-listed and silently falls back to Site URL, so
  the preview looks like it redirects to prod on purpose. Fix is one entry in
  Authentication → URL Configuration → Redirect URLs:
  `https://90x-*-am4nns-projects.vercel.app/**` (`*` spans hyphens, not dots, so
  it covers both deployment hashes and branch aliases). Previews then sign in
  against the **production** database — there is no separate Supabase project.

## Verifying work

From `web/`, no secrets needed:

`typecheck` · `lint` (ESLint + oxlint, zero warnings) · `test` (Vitest) ·
`format:check` (`bunx oxfmt` fixes) · `check:tokens` (design tokens) ·
`check:dead` (knip, unreferenced exports) · `check:dupes` (jscpd, duplicated
blocks) · `check:cycles` (dpdm, circular imports) · `check:coverage` (floor on
`src/lib`) · `check:deps` (deprecated dependencies) · `check:actions` (stale
workflow actions) · `build` then `check:bundle` (gzipped ceiling) · `bun audit`

Against the real database (need `.env.local`, so only the lead can run them):
`check:rls` · `check:tracker` · `check:feed` · `check:coach-tools`.
With real AI keys and a few cents: `check:grading`, `check:coach`.

Five of these gates were added on 2026-09-28 and **three found real bugs on
their first run.** Do not treat a new gate's first red as noise.

CI runs everything except the AI ones, plus Playwright against a throwaway
Supabase, a Redis stand-in and a fake model (`web/e2e/fake-model.ts`, an
OpenAI-compatible server with fixed replies) so the Coach specs never call a real
model, plus an `@axe-core/playwright` WCAG 2.1 AA scan.

From `pipeline/`: `.venv/Scripts/python.exe -m pytest -q`.

## Conventions

- Commit straight to `main` for lead-side work; everything from an agent comes
  through a PR. Never skip hooks.
- Aman wants: short answers in bullets, menus (`AskUserQuestion`) for real
  decisions, no shortcuts when something looks wrong, and proof rather than
  claims. He pushed back correctly when a number was guessed instead of measured.
  Quantify before asserting.
- **Ask before spending on AI runs.** The pipeline cap is `PIPELINE_MAX_USD`.
  Lifetime pipeline spend is **$65.47** as of 2026-09-29; the approved ceiling was
  ~$44.50 of that (earlier spend predates it). The app's own budget is $10/month
  in `ai_usage` plus a Redis meter.
- Server code uses Drizzle over a connection that **bypasses row-level
  security**, so every query must be scoped to the signed-in user or admin-gated.
  RLS is the second line of defence, not the first — changing a policy without
  changing the query changes nothing. `check:rls` and `check:coach-tools` prove it.
- Design: spec §7 only — six text sizes, token colours, borders not shadows, dark
  only, no native selects on desktop. `check:tokens` enforces it.
