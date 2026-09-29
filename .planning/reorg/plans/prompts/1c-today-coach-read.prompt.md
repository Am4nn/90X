You are building **unit 1c of the 90x reorg wave: the Coach's weekly read on Today**.

**Worktree** `../90X-wt/1c` · **Branch** `today-read` · **Playwright spec** `web/e2e/weekly-read.spec.ts`

Other agents may be building units 1a, 1b, 1d, 3 and 4 at the same time in their own
worktrees. Never touch their files.

## Read these first, in this order

1. `.planning/reorg/plans/prompts/SETUP.md` — your environment, how to test, every gate, the
   forbidden files, the PR format. **Read it before you write any code**; it contains the
   one flag (`E2E=1`) without which no test can sign in.
2. `.planning/briefs/README.md` — how this codebase is written. Wins over everything.
3. **`.planning/reorg/plans/1c-today-coach-read.md` — your plan.** Exact files, the existing
   functions to reuse with their real signatures, the tests, the traps.
4. `.planning/reorg/plans/README.md` — the wave's cross-cutting decisions.
5. `.planning/reorg/me-coach-reorg.brief.md` — the Today and Ren sections.
6. `.planning/reorg/DECISIONS.md` — the Today and "coach mark" sections.
7. `.planning/reorg/mocks/today.html` — the visual reference.
8. `web/AGENTS.md` — **this is Next.js 16**; read the guide under
   `web/node_modules/next/dist/docs/` before writing routing or server-action code.

Worked examples already merged, in this exact style: `web/e2e/roadmap.spec.ts` (especially its
tick test — see trap 3), `web/src/components/library/roadmap-graph.tsx`.

## What you are doing

The weekly review carries the Coach's score, a written read and suggested plan changes, and
today it is reachable only through a small link on Me. Put it on Today as a full card above
the missions.

**This is an add-on.** Keep the day line, `OfflineBanner`, `PendingRequests`, the 90 `Grid`
(mobile and the desktop aside), `ReviveBanner`, the missions section and the desktop readiness
strip exactly as they are, and keep the `no_campaign` and `ended` branches working.

## The five traps that will cost you most

1. **`latestWeekly` returns only `{ id, weekStart, coachScore }`** — no summary, no changes.
   Reading `summaryMd` off it is an invented field. Call `latestWeekly` first, then
   `weeklyView(viewer.id, latest.id)` for the body. **Do not add a new query** to
   `lib/coach/weekly.ts`; if you think one is needed, say so in the PR instead of writing it.
2. **No inline Accept.** Deciding happens on `/me/weekly/[id]`, which already has
   `WeeklyDecision` and `decideWeeklyAction`. Do not import either, and add no server action
   to this unit. Your spec should assert there is **no Accept button anywhere on Today**.
3. **Dismiss lives in `localStorage`, keyed by the review's `weekStart`** — decided, do not
   re-open, and you may not add a column. Wrap every access in `try/catch`: it throws in a
   private window and with site data blocked, and the card must still render correctly when
   it does. Render the card hidden until the check has run, so a dismissed card never flashes
   into view.
4. **Ren already exists and is already on Today's coach line**, put there by the prep PR — so
   the import is in the file when you start. Consume it, do not modify it, do not create your
   own. It does **not** go in the nav.
5. **`accepted` is `boolean | null`.** Null means undecided; a decided review still shows its
   read, it just has nothing left to decide. And `weeklyView` returns `null` for a bad id —
   handle it, do not assert.

## Verification

Everything in SETUP.md, plus these database checks: `bun run check:tracker`,
`check:coach-tools`.

Your spec must be `web/e2e/weekly-read.spec.ts`, run with `--retries=0` at least three times.
Two cases matter most and are the ones most likely to be missing:

- **Dismiss survives a reload**, and
- **a newer weekly review makes the card come back despite the earlier dismissal** — that is
  what keying on `weekStart` is for, and it would break silently.

You will need to seed a weekly review; SETUP.md section 3 covers adding seed rows.

Screenshots at 390px and 1440px of Today with the card, and Today after dismissing it.

Report back as SETUP.md section 8 describes.
