You are building **unit 1b of the 90x reorg wave: Coach modes and a real Lessons page**.

**Worktree** `../90X-wt/1b` · **Branch** `coach-lessons` · **Playwright spec** `web/e2e/lessons.spec.ts`

Other agents may be building units 1a, 1c, 1d, 3 and 4 at the same time in their own
worktrees. Never touch their files.

## Read these first, in this order

1. `.planning/reorg/plans/prompts/SETUP.md` — your environment, how to test, every gate, the
   forbidden files, the PR format. **Read it before you write any code**; it contains the
   one flag (`E2E=1`) without which no test can sign in.
2. `.planning/briefs/README.md` — how this codebase is written. Wins over everything.
3. **`.planning/reorg/plans/1b-coach-modes-lessons.md` — your plan.** Exact files, the
   existing functions to reuse with their real signatures, the tests, the traps.
4. `.planning/reorg/plans/README.md` — the wave's cross-cutting decisions.
5. `.planning/reorg/me-coach-reorg.brief.md` — the intent, Coach and Lessons sections.
6. `.planning/reorg/DECISIONS.md` — the Coach section.
7. `.planning/reorg/mocks/coach.html` and `lessons.html` — visual references.
8. `web/AGENTS.md` — **this is Next.js 16**; read the guide under
   `web/node_modules/next/dist/docs/` before writing routing, `error.tsx`, `loading.tsx` or
   server-action code.

Worked examples already merged, in this exact style: `web/src/components/library/roadmap-graph.tsx`,
`web/e2e/roadmap.spec.ts`, `web/e2e/mock-picker.spec.ts`.

## What you are doing

Coach's "Lessons" entry links to `/library` — the whole catalogue, not a lessons list. Make
it a real page at `/coach/lessons`, and add Story bank to the modes so interview practice
lives under Coach.

This is the **smallest-diff unit in the wave**: one new route and one array. Resist making it
bigger. **This is an add-on** — keep existing behaviour; where a mock differs from today,
today wins unless your plan says otherwise.

## The four traps that will cost you most

1. **Story bank keeps its current route.** `DECISIONS.md` chose minimal churn: the modes nav
   links to `/me/stories`, and that page is not moved or changed. Do not create
   `/coach/stories`.
2. **`weakestPatterns` drops untouched patterns and returns at most `n`.** A new account has
   no check-ins and therefore **no weakest patterns at all** — that is the common case, not
   an edge case. The page must lead with the full pattern index and an `EmptyState` where the
   weakest section would be, never a blank area. Do not "fix" it by passing a bigger `n`.
3. **Do not build a new teach flow.** `?kind=lesson&ref=<slug>` already exists and
   `coach/page.tsx` trims `ref` to 200 characters. Pass the slug and nothing else.
4. **`patternMap` is `server-only`** — call it in the page, never from a client component,
   and always scoped as `patternMap(viewer.id)`.

`weakestPatterns` is already tested in `web/src/lib/tracker/me-rules.test.ts`. Read those
cases rather than writing new ones for it.

## Verification

Everything in SETUP.md, plus these database checks: `bun run check:tracker`,
`check:coach-tools`.

Your spec must be `web/e2e/lessons.spec.ts`, run with `--retries=0` at least three times. It
must cover the empty case — a user with no check-ins still seeing the pattern index — because
that is the state most real users will hit first.

Screenshots at 390px and 1440px of `/coach` and `/coach/lessons`.

Report back as SETUP.md section 8 describes.
