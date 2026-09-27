# Brief J — Fresh-eyes review of the whole app, then fix what matters

**Read `.planning/briefs/README.md` first.** You are a senior reviewer seeing 90x for the first time. Parts 1–5 were built quickly by several agents in parallel and merged by a lead; each piece was reviewed alone, never the whole.

Branch: your pinned branch. PR to `main`.

## Read
`.planning/SPEC.md` (the product), the plans in `.planning/plans/` (their **Decisions** sections are binding product choices — don't "fix" those), then the code under `web/src/` and `supabase/migrations/`.

## Review, in this order (write findings as you go)
1. **Security and privacy** (spec §3 Privacy / Coach isolation). Server code uses Drizzle over a connection that bypasses row-level security, so every query in `web/src/lib/**`, `web/src/app/actions/**`, `web/src/app/api/**` and server pages must be scoped to the signed-in user's id or be admin-gated, or read data meant for all approved users. Look for: another user's private rows (notes, missions, card answers, coach threads/memory, solution reviews, stories, mock transcripts, push subscriptions) reachable by id from any action or route; IDs taken from the client without an ownership check; answers/key points reaching the client before answering; the test sign-in route's gate; the QStash job routes' signature checks; the service worker caching anything personal it shouldn't (and clearing on sign-out).
2. **Correctness across features**: Today ↔ Feed ↔ Coach interactions (missions ticked twice or never, days closing wrong around local midnight, streak/revive, readiness numbers disagreeing between Today, Me and the Coach's tools, rest days), proposals confirmed twice, budget fallback, time zones (users in Asia/Kolkata and America/Los_Angeles).
3. **Consistency and UX**: spec §7 visual rules (six text sizes, tokens, borders not shadows, no native selects on desktop), empty/loading/error states on every route, copy tone, mobile (390px) and desktop layouts, navigation dead ends (every page reachable and every page has a way back), and things that look unfinished (placeholders like "arrives in part N").
4. **Dead code and drift**: leftovers from the parallel build (duplicate helpers doing the same thing, unused props, outdated comments such as "browser tests are not here yet" in `ci.yml`).

## Fix
- Fix every **Critical** and **Important** finding (effect on a real user: data leak, wrong numbers, broken flow, crash, dead end). Each fix gets a test that fails first (Vitest for pure logic; for DB behaviour add a case to the relevant `web/scripts/check-*.ts` rolled-back check — you can't run those, the lead does).
- Don't change product decisions recorded in the plans; if you think one is wrong, list it under **Suggestions**.
- Minor findings: list them, don't fix them (unless trivial and zero-risk).

## PR description
**Findings** table (severity, file:line, what a user would see, fixed?), **Decisions**, **Checks** (every README command), **Not verified**, **Suggestions**. Keep it scannable.
