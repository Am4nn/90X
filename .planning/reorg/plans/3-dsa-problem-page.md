# Unit 3 — the DSA problem page, LeetCode-first

**Branch** `problem-page` · **Worktree** `../90X-wt/3` · **Spec** `e2e/problem-page.spec.ts`
**Brief** `.planning/reorg/dsa-problem-page.brief.md`

Read `.planning/reorg/plans/README.md` first.

## Scope

The problem page is good. This unit reorders the top of it so **Open on LeetCode** is the
obvious first action, adds a **Sync** path to the check-in, and makes every outcome offer
the next step. Keep the statement, the tricks, the reference-solution reveal, the
Review/Learn links and the past check-ins.

## Files

**Create**
- `web/e2e/problem-page.spec.ts`

**Modify**
- `web/src/app/(app)/library/problem/[slug]/page.tsx` — order of the top blocks
- `web/src/components/library/checkin-panel.tsx` — the shell and the sync path
- `web/src/app/actions/sync.ts` — add a per-problem sync action

## What sync can and cannot do — verified, do not design past this

Sync already auto-logs attempts. `syncUser` inserts `checkins` rows with
`source: "leetcode_sync"`, an `externalId`, `attempts` and `minutesSuggested`, uses
`onConflictDoNothing`, and calls `onCheckins` to tick missions. So the feature exists; this
unit surfaces it on the problem page. Its real limits:

| The brief says | The truth |
|---|---|
| solved | **Yes.** `"solved"` or `"failed"` |
| time taken | **Inferred only** — the gap from first to accepted submission, capped at 120 minutes, and **null when there was only one attempt**. `checkins.minutes` stays null until `setMinutes` |
| hints | **Not derivable at all.** There is no hint signal in a LeetCode submission |

Also: `recentSubmissions` fetches about the **last 20 submissions**, only problems present
in our `problems` table are logged (the rest count as `notInLibrary`), it needs
`profiles.leetcodeUsername`, and it needs `LEETCODE_SYNC_ENABLED === "true"`
(`syncEnabled()`).

**So build this, and nothing more:** the button runs a sync, then reports what it found for
*this* problem — solved/failed and a suggested time. Hints stays a manual toggle. Time
stays editable through the existing `setMinutes`. If sync finds nothing for this problem,
say so plainly ("No recent submission for this one.") and leave the manual check-in right
there. **Never show a hint state or a time that sync did not actually produce.**

## Reuse, do not rewrite

```
problemDetail(slug, userId)          @/lib/library/queries
  -> { problem, pattern: {slug,name}|null, mine, friends, tricks } | null
  problem = { slug, kind, lcNumber, title, difficulty, patternSlug, topicSlugs, tags,
              importance, nc150, blind75, companies, statementMd, solutions, videoId,
              url, sourceId, updatedAt, premium, techniques }
  mine    = up to 5 of { id, result, minutes, createdAt, note }

CheckinPanel slug leetcodeUrl        @/components/library/checkin-panel   (client)
checkIn(_, form)                     @/app/actions/checkin
  -> CheckinState { ok?, error?, checkinId? }
RESULTS, TIME_CHIPS, parseCheckin    @/lib/library/checkin
  RESULTS: solved | hints | failed ; TIME_CHIPS: [15,30,45,60]

syncNow()                            @/app/actions/sync   -> SyncResult
setMinutes(form)                     @/app/actions/sync   // fields: checkinId, minutes 1..600
syncEnabled()                        @/lib/activity/service
SyncResult  = { status: "disabled"|"skipped"|"unknown_user" }
            | { status: "failed", error, unavailable }
            | { status: "ok", created: SyncedAttempt[], notInLibrary: number }
SyncedAttempt = { slug, title, result: "solved"|"failed", attempts,
                  minutesSuggested: number|null, externalId, at }
Markdown, BackLink, PageHeader, EmptyState, ChipGroup/Switch, SubmitButton, chip(), button()
```

`leetcodeUrl` is already computed in the page:
`https://leetcode.com/problems/<slug>/` when `kind === "leetcode"`, else `problem.url`.

## What to build

**1. Open on LeetCode, first.** On **mobile it sits above the statement**; on desktop it
belongs in the header or at the top of the right panel. It is the primary action — make it
look like one. `CheckinPanel` already renders an "Open on LeetCode" button; if you keep one
there, do not end up with two competing primaries.

**2. The sync action.** Add to `app/actions/sync.ts` something of this shape:

```ts
export async function syncForProblem(slug: string):
  Promise<{ found: SyncedAttempt | null } | { error: string }>;
```

It runs the existing `syncUser` path (reuse `syncNow`'s body — do not write a second sync),
then picks the attempt whose `slug` matches. Scope it to the signed-in viewer from
`requireViewer()`, validate `slug` with Zod (1–200 characters, matching `parseCheckin`),
return a short human error rather than throwing, and revalidate the problem page. Handle
every `SyncResult` status: `disabled`, `skipped`, `unknown_user` and `failed` each need
their own honest message — "LeetCode sync is off", "No LeetCode username set", and so on.

**3. The panel.** Keep `CheckinPanel`'s action, state and hidden inputs (`problemSlug`,
`result`, `minutes`, the `note` textarea). Restructure the shell around them:

- Sync button → on success, preselect `result` and, when `minutesSuggested` is not null,
  preselect the nearest `TIME_CHIPS` value. Say where it came from.
- **Time chips stay editable after sync**, and clicking the selected chip still clears it to
  null, as today.
- **Hints stays manual.**
- **The note is always visible**, synced or not. It is already a plain textarea; keep it.

**4. Each outcome offers the next step.** After a check-in:
`solved` → capture the time, then **Review solution**; `hints` → **Review solution**;
`failed` → **Learn this pattern** (`/coach?kind=lesson&ref=<patternSlug>`) then **Review
solution** (`/library/problem/<slug>/review`). Both links already exist in the page's
aside — reuse those hrefs, do not invent routes.

**When `syncEnabled()` is false**, no sync button at all. The page must behave exactly as it
does today.

## Do not touch

`lib/activity/**` — read it, do not change it. No new source, no new merge rule, and do
**not** widen the 20-submission window · `app/actions/checkin.ts` and `lib/library/checkin.ts`
(the check-in contract stays) · `library/page.tsx` (unit 2) · `library/problem/[slug]/review/**` ·
`me/page.tsx` and `components/leetcode/**` (unit 1a owns the Me-side LeetCode card) ·
plus the README's forbidden list.

**No migration.** If you conclude sync needs a column, stop and say so in the PR.

## Tests

`web/src/lib/activity/` has existing tests — read them before adding any.

Unit, TDD: the pure "pick the nearest time chip for N minutes" helper (null in → null out;
18 → 15; 38 → 30 or 45, pick one and test it). Put it beside `TIME_CHIPS` in
`lib/library/checkin.ts`.

`e2e/problem-page.spec.ts`:

- At 390px, Open on LeetCode appears **above** the statement; at 1440px it is in the
  header or right panel.
- The manual check-in still works end to end and still reaches
  `/library/problem/<slug>/review?checkin=<id>`.
- The note field is visible before any sync.
- With sync disabled, there is no sync button and the page is unchanged.
- A failed check-in offers **Learn this pattern**; a solved one offers time capture then
  **Review solution**.
- Statement, tricks, the reference-solution `details` and past check-ins are all still
  present.

Sync against the live LeetCode API is not a thing to assert in CI. Drive the sync path with
a seeded `checkins` row where you can, and say plainly in the PR which sync branches you
exercised by hand and which you did not.

## Traps

- **`minutesSuggested` is null whenever there was only one real attempt** — which is most
  solved problems. The no-suggestion path is the common path, not the edge case.
- `checkIn` inserts through the **Supabase (RLS) client**, not Drizzle. Do not "fix" that.
- `problemDetail` returns `null` for an unknown slug; the page must keep `notFound()`.
- `mine` is capped at 5 rows and `friends` shows first names only. Do not widen either —
  friends' notes are deliberately not exposed.
- The reference solution picks `viewer.language` if a solution exists for it, else the first
  key of `solutions`. Keep that.
- `setMinutes` takes `checkinId` and an integer 1–600. A sync-suggested time over 120 cannot
  happen (the cap), but do not assume the field is bounded elsewhere.
- Six text sizes, token colours, borders not shadows; no native `select` or checkbox on
  desktop — use `Switch` for the hints toggle.

## Verification

The README's full list, plus `bun run check:tracker`. Screenshots at 390px and 1440px,
before and after sync, and with sync disabled.
