# Unit 1c — the Coach's weekly read on Today

**Branch** `today-read` · **Worktree** `../90X-wt/1c` · **Spec** `e2e/weekly-read.spec.ts`
**Brief** `.planning/reorg/me-coach-reorg.brief.md` (the Today and Ren sections)

Read `.planning/reorg/plans/README.md` first.

## Scope

The weekly review carries the Coach's own score, a written read and suggested plan
changes, and today it is reachable only through a small link on Me. This unit puts it on
Today as a full card above the missions, and gives the Coach line its real mark.

**Not yours:** the weekly review page itself, Me, Coach, the chat.

## Files

**Create**
- `web/src/components/coach/weekly-read.tsx` — client (it owns the dismiss state)
- `web/e2e/weekly-read.spec.ts`

**Modify**
- `web/src/app/(app)/today/page.tsx` — render the card; swap the inline "C" for Ren

## Reuse, do not rewrite

```
latestWeekly(userId)                @/lib/coach/weekly
  -> { id, weekStart, coachScore } | null        // NOTE: only these three fields

weeklyView(userId, id)              @/lib/coach/weekly
  -> (WeeklyReviewRow & { changes: Change[] }) | null
  WeeklyReviewRow = { id, userId, weekStart, formulaScore, coachScore,
                      summaryMd, suggestedChanges, accepted, createdAt }
  Change = { weekday: 0-6, slot: "new_problem"|"review"|"topic"|"cards",
             from: number, to: number, why: string }     @/lib/coach/weekly-rules

SLOT_LABEL, SLOT_LABEL_SHORT        @/lib/tracker/template
DAY_NAMES, DAY_NAMES_LONG           @/lib/tracker/dates
Markdown                            @/components/markdown
Ren                                 @/components/coach/ren        // already exists
EmptyState, button()
```

**`latestWeekly` is not enough on its own.** It selects only `id`, `weekStart` and
`coachScore` — no summary, no changes. Today's page needs both, so call `latestWeekly`
first and then `weeklyView(viewer.id, latest.id)` for the body. Do **not** add a new query
to `lib/coach/weekly.ts`; two calls on a page that already awaits several is not the
problem, and a third query is a maintenance cost nobody asked for. If you disagree, say so
in the PR rather than writing it.

## What to build

**The card**, above the missions and below the day line / offline banner / pending
requests, in the left column:

- Ren, then "Coach's read" and the week (`weekStart`).
- The **coach score** (`coachScore`) — and note `formulaScore` is also available from
  `weeklyView` if the mock shows both.
- The read itself: `summaryMd` through `Markdown`.
- The **suggested changes**: on desktop, the rows (`DAY_NAMES_LONG[weekday]`,
  `SLOT_LABEL[slot]`, from → to, `why`) exactly as `/me/weekly/[id]` renders them. On
  **mobile, drop the rows and show the count** ("3 suggested changes").
- A link to `/me/weekly/<id>` — **"Read it" / "Decide"**.
- A **dismiss ✕**.

**No inline Accept.** Deciding happens on `/me/weekly/[id]`, which already has
`WeeklyDecision` and `decideWeeklyAction`. Do not import either one here, and do not add a
server action to this unit.

**Dismiss persistence — decided, do not re-open:** `localStorage`, keyed by the review's
`weekStart`, under `90x:weekly-dismissed`. A new weekly review has a new `weekStart`, so
the card comes back on its own with no extra bookkeeping. It is per-device — dismissing on
a phone leaves it showing on a laptop — and that is accepted. There is no column for this
and **you may not add one**.

Because the dismissal is read on the client, the card will exist in the server HTML and
hide on mount. Render it hidden until the check has run (not the reverse) so a dismissed
card never flashes into view. Guard every `localStorage` access in `try/catch`: it throws
in a private window and with site data blocked, and the card must still render correctly
when it does.

**Ren replaces the inline "C"** at `today/page.tsx` (the
`grid size-7 … bg-cyan-bg … text-cyan` span holding a literal "C"). Ren is the shared
character from Curfew and it already exists at `components/coach/ren.tsx` — **consume it,
do not modify it, do not create your own**. Use it on the read card and on the coach line.
It does **not** go in the nav; the nav keeps `CoachIcon`.

**Keep exactly as they are:** the day line, `OfflineBanner`, `PendingRequests`, the 90
`Grid` (mobile and the desktop aside), `ReviveBanner`, the missions section and the
desktop readiness strip. Also keep the `no_campaign` and `ended` branches working — a user
with no campaign has no weekly review, so the card simply does not render there.

## Do not touch

`me/weekly/[id]/page.tsx` and `components/coach/weekly-decision.tsx` (nobody — they work) ·
`app/actions/weekly.ts` · `components/coach/ren.tsx` · `me/page.tsx` and `nav.tsx` (1a) ·
`coach/page.tsx` (1b) · `chat.tsx` (1d) · plus the README's forbidden list.

## Tests

`e2e/weekly-read.spec.ts`, seeding a weekly review for the user:

- The card renders above the missions, showing the coach score and the read.
- It links to `/me/weekly/<id>` and has **no Accept button anywhere on Today**.
- Dismissing hides it, and it is still hidden after a reload.
- Seeding a *newer* weekly review makes it appear again despite the earlier dismissal.
  This is the case the `weekStart` key exists for, and the one that would silently break.
- A user with no weekly review sees Today unchanged.
- The missions, the grid and the readiness strip are all still present.

Pure helper worth extracting and unit-testing: the "is this review dismissed" decision
(dismissed `weekStart` plus current `weekStart` → boolean). Put it in
`lib/coach/weekly-rules.ts` beside the other pure weekly rules and test it there.

## Traps

- **`latestWeekly` has no `summaryMd`.** Reading it off that return value is a type error
  at best and an invented field at worst.
- `weeklyView` returns `null` for a bad id — handle it, do not assert.
- `accepted` is `boolean | null`. Null means undecided. A review that has already been
  decided should still show the read; it just has nothing left to decide.
- The readiness strip and the desktop `Grid` live in a `hidden md:flex` aside. Do not move
  the card into it.
- Do not change the ordering of the existing blocks other than inserting the card.
- Six text sizes, token colours, borders not shadows. `Markdown` already carries the prose
  styles — do not restyle it.

## Verification

The README's full list, plus `bun run check:tracker` and `check:coach-tools`.
Screenshots at 390px and 1440px of Today with the card, and Today after dismissing it.
