# Brief — the DSA problem page (check-in and read)

**Branch:** `dsa-problem-page` (or your session's own branch; say so in the PR).
**Read first:** `.planning/briefs/README.md`. It wins over the plan; the plan wins over the spec.

## Why

`/library/problem/[slug]` is where a check-in actually happens, and it is the least-designed
surface in the app. Today (`web/src/app/(app)/library/problem/[slug]/page.tsx`) it is a statement
card, a collapsible reference solution, and a `CheckinPanel` squeezed into a right-hand column.

The owner's words: *"we have to redesign the dsa question checking page"*.

The problems, in priority order:

1. **The check-in is the point, and it looks like a side panel.** On a phone the primary action
   (log the attempt) sits below a long statement. It should be reachable without a hunt.
2. **"Didn't solve" is a dead end.** A failure should route into the pattern lesson, not just
   record a number.
3. **The statement dominates.** The pattern, the tricks, and the reference solution are the
   transferable part; today they are below the fold or hidden behind `<details>`.
4. **The page has no memory of you.** Past check-ins for this problem are a small text list; there
   is no "you last did this 3 days ago in 22m" at the top.
5. **Actions scatter.** "Review solution", "Learn pattern", the video link and the check-in panel
   are separate blocks with no hierarchy.

## Definition of done

1. **One primary action.** The check-in (Solved / Solved with hints / Didn't solve) is visible
   without scrolling on a 390px phone — a sticky bottom action bar on mobile, the top of the
   right column on desktop. Reuse `CheckinPanel`'s action and state; you may restructure its
   shell.
2. **Each outcome leads somewhere.** After logging, the page offers the next step: solved → the
   time capture (existing `setMinutes` flow) then "Review solution"; hints → "Review solution";
   didn't solve → "Learn this pattern" (`/coach?kind=lesson&ref=<pattern>`) then "Review
   solution".
3. **Your history first.** Above the statement, a one-line summary of your last attempt on this
   problem ("You solved this with hints 3 days ago in 24m"), or a quiet "First time here" when
   there is none. Data already comes from `problemDetail` (`mine`).
4. **The pattern leads the reading.** Pattern name, the tricks it uses, and the reference solution
   form one "the idea" group, ordered before the raw statement. Keep the reference solution
   behind a reveal (it is a spoiler), but make the reveal obvious and not a `<details>` caret.
5. **Friends are secondary.** Keep the friends' check-in line, but below your own history and
   visually quieter.
6. **No new data.** Everything comes from the existing `problemDetail` query and components. No
   schema change, no new migration.
7. `loading.tsx` and `error.tsx` exist for the segment (they do — keep them shaped like the new
   page). All empty states use `EmptyState`.

## Constraints

- DESIGN.md and spec §7 only: the six text sizes, token colours, borders not shadows, dark only,
  no native selects on desktop. The coach mark is **Ren** (see DESIGN.md → Signature Components);
  do not draw a plain initial for the Coach.
- Mobile first (390px), then desktop two-column. Reference the committed reorg mocks in
  `.planning/mockups/reorg/` for the shell (6 tabs, Ren, tokens).
- Server code stays scoped to the viewer (`problemDetail` already is). No changes to
  `problemDetail` unless a field is missing; if it is, say so in the PR.

## Out of scope

- The Library index and Pattern Map (a separate brief).
- The review page (`/library/problem/[slug]/review`).
- Any change to how attempts are graded or scheduled.

## Verification

From `web/`: `typecheck`, `lint`, `test`, `format:check`, `check:tokens`, `check:dead`, `build`.
`check:rls` and `check:tracker` need the database — say so; the lead runs them. Attach before/after
screenshots of the page at 390px and 1440px to the PR.
