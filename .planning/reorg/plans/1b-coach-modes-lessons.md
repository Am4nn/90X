# Unit 1b — Coach modes and a real Lessons page

**Branch** `coach-lessons` · **Worktree** `../90X-wt/1b` · **Spec** `e2e/lessons.spec.ts`
**Brief** `.planning/reorg/me-coach-reorg.brief.md` (the Coach and Lessons sections only)

Read `.planning/reorg/plans/README.md` first.

## Scope

Coach's "Lessons" entry currently links to `/library` — the whole catalogue, not a lessons
list. This unit makes it a real page, and adds Story bank to the modes so interview
practice lives under Coach.

**Not yours:** the chat component (1d), Today (1c), Me (1a), the story bank page itself.

## Files

**Create**
- `web/src/app/(app)/coach/lessons/page.tsx`, `loading.tsx`, `error.tsx`
- `web/e2e/lessons.spec.ts`

**Modify**
- `web/src/app/(app)/coach/page.tsx` — the `MODES` array only

## Reuse, do not rewrite

```
patternMap(userId, q?)              @/lib/library/queries
  -> { patterns: PatternNode[], links: { from, to }[] }
  PatternNode = { slug, name, total, solved, failed, state: Mastery }
  Mastery ("mastered" | "started" | "weak" | "untouched")  @/lib/library/map-layout

weakestPatterns(patterns, n = 3)    @/lib/tracker/me-rules
  -> (T & { detail: string })[]   // detail is "N solved, M failed"
  // Pure. Sorts by solve rate ascending, then failures descending, and keeps only
  // patterns with attempts. This is exactly the "weakest-first" the brief asks for.

areaTopics(domain)                  @/lib/library/queries
  -> { slug, name, description, parent, importance, summary, words }[]
  // Inner-joins lessons, so only topics that HAVE an authored lesson come back.

AREAS, AreaKey                      @/lib/library/queries
requireViewer()                     @/lib/auth/viewer
PageHeader, EmptyState, RouteError, button()
```

## What to build

**`MODES` in `coach/page.tsx`** becomes four entries, keeping the existing shape
(`{ href, label, hint }`) and the nav markup untouched:

```
Chat        /coach?new=1        Ask about your prep
Lessons     /coach/lessons      Pick a pattern to learn
Mocks       /coach/mocks        Design and behavioral
Story bank  /me/stories         Your examples for behavioural rounds
```

Story bank **keeps its current route and page** — DECISIONS.md chose Option A, minimal
churn. Do not move it to `/coach/stories`. "What Coach knows" stays as the header action.

**`/coach/lessons`** — "Pick a pattern", **weakest-first, not roadmap order**:

1. A lead section of the weakest patterns from `weakestPatterns(map.patterns, 3)`, each
   row showing the name, its `detail` ("4 solved, 6 failed") and its mastery state, with a
   **Teach me** action linking to `/coach?kind=lesson&ref=<slug>` — the existing Coach
   lesson flow, already wired, do not build a new one.
2. Below it, the **full pattern index**: every `map.patterns` row, same Teach-me action,
   in the map's own order (`patternMap` returns them ordered by `sort`).
3. A link to `/library` for topic lessons in the other areas. If you want to be more
   useful than a bare link, `areaTopics(area)` returns only topics that actually have a
   lesson — but keep it to a count or a short list, not a second catalogue.

Empty state: a user with no check-ins has no weakest patterns at all (`weakestPatterns`
keeps only patterns with attempts). That is the common case for a new account, so the page
must lead with the full index and an `EmptyState` in the weakest section — **not** a blank
area.

## Do not touch

`components/coach/chat.tsx` and `lib/coach/chat-rules.ts` (1d) · `today/page.tsx` (1c) ·
`me/page.tsx`, `nav.tsx`, `page-header.tsx` (1a) · `me/stories/**` (nobody) ·
`coach/mocks/**` and `components/coach/mock-picker.tsx` (5) · `library/page.tsx` (2) ·
plus the README's forbidden list.

## Tests

`e2e/lessons.spec.ts`:

- The Coach modes nav shows four entries, and Lessons goes to `/coach/lessons`, **not**
  `/library`.
- Story bank in the modes nav reaches `/me/stories`.
- `/coach/lessons` lists patterns, and a Teach-me link carries
  `?kind=lesson&ref=<slug>` to `/coach`.
- A user with no check-ins still sees the pattern index and an empty state where the
  weakest section would be.

No Vitest needed unless you extract a helper — `weakestPatterns` is already tested in
`lib/tracker/me-rules.test.ts`. Read those cases rather than writing new ones.

## Traps

- **`weakestPatterns` returns at most `n` and drops untouched patterns.** Do not "fix"
  that by passing a larger `n` and hoping; the full index below is what covers the rest.
- `patternMap` is `server-only` — call it in the page, never from a client component.
- Scope it: `patternMap(viewer.id)`, never an unscoped call.
- The `?kind=lesson&ref=` flow already exists and `coach/page.tsx` trims `ref` to 200
  characters. Pass the slug, nothing else.
- `loading.tsx` shaped like the page, `error.tsx` via `RouteError`, which in **Next 16
  receives `retry`, not `reset`**.
- Six text sizes, token colours, borders not shadows.

## Verification

The README's full list, plus `bun run check:tracker` and `check:coach-tools`.
Screenshots at 390px and 1440px of `/coach` and `/coach/lessons`.
