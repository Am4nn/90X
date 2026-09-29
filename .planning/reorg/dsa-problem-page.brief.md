# Brief — the DSA problem page (LeetCode-first check-in)

**Branch:** `problem-page` (or your session's branch; say so in the PR).
**Read first:** `.planning/briefs/README.md`.

## Rule one: this is an add-on

The mocks are **visual references, not final designs**. The problem page is **fine today** — keep
the statement, the tricks, the reference-solution reveal, the Review / Learn-pattern links and the
past check-ins. This brief adds a **LeetCode-first check-in** and reorders the top of the page. Do
not rebuild the page.

## What to add

1. **Open on LeetCode is the first, obvious action.** A prominent button at the top. On a phone it
   sits **above the statement**; on desktop it is fine in the header/right panel.
2. **Sync with LeetCode** — one button that auto-logs the attempt from the reader's submissions
   (solved, time taken, hints). Reuse the existing LeetCode integration
   (`lib/activity/*`, the sync path behind `SyncButton`); do not invent a second one.
3. **Manual check-in stays** as the fallback (Solved / Hints / Didn't solve), so nothing is lost if
   sync is off or the username is unset.
4. **After sync, keep editing**: a **time-taken** control, a **hints** toggle, and the **note
   field** (the note is always visible, synced or not).
5. **Each outcome offers the next step**: solved → time capture then "Review solution"; hints →
   "Review solution"; didn't solve → "Learn this pattern" then "Review solution".
6. Keep `CheckinPanel`'s action and state; restructure its shell only.

## Constraints

- No schema changes unless the sync genuinely needs a field — if so, do **not** add a migration;
  say so in the PR and the lead will handle it.
- Every query stays scoped to the viewer (`problemDetail` already is).
- DESIGN.md / spec §7 only: six text sizes, token colours, borders not shadows, dark only.

## Out of scope

The Library index and the review page; how attempts are graded or scheduled; the Feed.

## Verification

From `web/`: `typecheck`, `lint`, `test`, `format:check`, `check:tokens`, `check:dead`, `build`.
`check:tracker` needs the database — say so. Screenshots at 390px and 1440px, before and after
sync.
