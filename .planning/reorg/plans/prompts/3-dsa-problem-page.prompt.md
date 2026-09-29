You are building **unit 3 of the 90x reorg wave: the DSA problem page, LeetCode-first**.

**Worktree** `../90X-wt/3` · **Branch** `problem-page` · **Playwright spec** `web/e2e/problem-page.spec.ts`

Other agents may be building units 1a, 1b, 1c, 1d and 4 at the same time in their own
worktrees. Never touch their files.

## Read these first, in this order

1. `.planning/reorg/plans/prompts/SETUP.md` — your environment, how to test, every gate, the
   forbidden files, the PR format. **Read it before you write any code**; it contains the one
   flag (`E2E=1`) without which no test can sign in.
2. `.planning/briefs/README.md` — how this codebase is written. Wins over everything.
3. **`.planning/reorg/plans/3-dsa-problem-page.md` — your plan.** Exact files, the existing
   functions to reuse with their real signatures, the tests, the traps. Its table of what sync
   can and cannot do is the heart of this unit.
4. `.planning/reorg/plans/README.md` — the wave's cross-cutting decisions.
5. `.planning/reorg/dsa-problem-page.brief.md` — the intent.
6. `.planning/reorg/DECISIONS.md` — the "Problem page (DSA)" section.
7. `.planning/reorg/mocks/problem.html` — the visual reference.
8. `web/AGENTS.md` — **this is Next.js 16**; read the guide under
   `web/node_modules/next/dist/docs/` before writing server-action code.

Worked example of a server action added in this style: `web/src/app/actions/sync.ts` itself.
Worked example of a spec: `web/e2e/checkin.spec.ts`, which already covers this page's check-in.
**Read it first — you must not break it.**

## What you are doing

The page is good. Reorder the top so **Open on LeetCode** is the obvious first action (on a
phone it sits **above the statement**), add a Sync path to the check-in, and make every
outcome offer the next step. Keep the statement, the tricks, the reference-solution reveal,
the Review/Learn links and the past check-ins.

## The brief promises something the code cannot do — build only what is true

Sync already auto-logs attempts: `syncUser` inserts `checkins` rows with
`source: "leetcode_sync"`. Its real limits, verified:

- **solved** — yes, `"solved"` or `"failed"`
- **time taken** — inferred only, from the gap between the first and the accepted submission,
  capped at 120 minutes, and **null whenever there was only one attempt**, which is most
  solved problems. `checkins.minutes` stays null until `setMinutes` is called.
- **hints** — **not derivable at all.** There is no hint signal in a LeetCode submission.

Also: only about the **last 20 submissions** are fetched, only problems in our `problems`
table are logged, it needs `profiles.leetcodeUsername`, and it needs `syncEnabled()`
(`LEETCODE_SYNC_ENABLED === "true"`).

So: the button runs a sync and reports what it found **for this problem** — solved/failed and
a suggested time. **Hints stays a manual toggle. Time stays editable** through the existing
`setMinutes`. The note is always visible. If sync finds nothing, say so plainly and leave the
manual check-in right there. **Never show a hint state or a time that sync did not produce.**

When `syncEnabled()` is false there is **no sync button at all** and the page behaves exactly
as it does today.

## The five traps that will cost you most

1. **`minutesSuggested` is null for most solved problems.** The no-suggestion path is the
   common path, not the edge case. Design for it first.
2. **Handle every `SyncResult` status honestly** — `disabled`, `skipped`, `unknown_user` and
   `failed` each need their own message ("LeetCode sync is off", "No LeetCode username set").
   A generic error hides a fixable problem from the reader.
3. **`checkIn` inserts through the Supabase (RLS) client**, not Drizzle. Do not "fix" that.
4. **Do not change `lib/activity/**`.** Read it; no new source, no new merge rule, and do not
   widen the 20-submission window. Your new action reuses the existing sync path rather than
   writing a second one.
5. **`mine` is capped at 5 rows and `friends` shows first names only.** Do not widen either —
   friends' notes are deliberately not exposed.

**No migration.** If you conclude sync needs a column, stop and say so in the PR.

## Verification

Everything in SETUP.md, plus `bun run check:tracker`.

Your spec must be `web/e2e/problem-page.spec.ts`, run with `--retries=0` at least three times,
and **also run `web/e2e/checkin.spec.ts`** — the existing contract for this page.

Sync against the live LeetCode API is not something to assert in CI. Drive the sync-shaped
paths with seeded `checkins` rows where you can, and say plainly in the PR which sync branches
you exercised by hand and which you did not.

TDD the one pure helper: nearest time chip for N minutes (null in → null out; 18 → 15), beside
`TIME_CHIPS` in `web/src/lib/library/checkin.ts`.

Screenshots at 390px and 1440px, before and after sync, and with sync disabled.

Report back as SETUP.md section 8 describes.
