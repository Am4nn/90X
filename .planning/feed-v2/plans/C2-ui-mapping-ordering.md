# Part C2 — the five mapping and ordering screens: order, match, bucket, assemble, claim grid

**Branch** `feed-v2-ui-c2` · **Worktree** `../90X-wt-fv2/c2` · **Specs** `ordering`, `pairing`,
`bucketing`, `assembling`, `claimgrid` (five files).

Read `.planning/feed-v2/plans/README.md` first. Depends on **B** (the dispatch, the `Answer`
shapes, the stub files). Do not start until B is merged.

C2 owns the five new screens that share two answer shapes but need their own UI: **order**
(ordered list), **match** (mapping), **bucket** (mapping, one tick per row), **assemble**
(templated ordered list), **claim grid** (mapping, true/false on every row). All of them are
**tap-to-place, never drag** (DECISIONS risk 4).

## Scope

- **Order** — tap items in the order you want them; they slot into a result rail.
- **Match** — tap left, tap right, pairs lock in.
- **Bucket** — tap item, tap column; one item per row (constrained, not free).
- **Assemble** — tap tokens from a pool into a line; a mostly-filled template is a word bank
  (difficulty is a property of the card, not a fork in the code).
- **Claim grid** — a true/false judgement on every row, forced (no skipping a row you're unsure
  of).

## Files

**Modify (replace B's stubs)**
- `web/src/components/feed/primitive/order.tsx`
- `web/src/components/feed/primitive/match.tsx`
- `web/src/components/feed/primitive/bucket.tsx`
- `web/src/components/feed/primitive/assemble.tsx`
- `web/src/components/feed/primitive/claim-grid.tsx`

**Create**
- `web/e2e/ordering.spec.ts`, `web/e2e/pairing.spec.ts`, `web/e2e/bucketing.spec.ts`,
  `web/e2e/assembling.spec.ts`, `web/e2e/claimgrid.spec.ts`

## Reuse, do not rewrite

```
Answer shapes: { shape: "ordered"; order: number[] }, { shape: "mapping"; pairs: [number, number][] }
submitAnswer(sent) -> AnswerState                        // @/app/actions/feed
PRIMARY, SECONDARY, button(), chip()                     // @/components/button-styles
Markdown                                                 // @/components/markdown
useServerAction                                          // @/components/form
```

Match B's `PrimitiveScreen` props (read `card.tsx` and `primitive/not-built.tsx`). Do not edit
`card.tsx`. The grader (B) already accepts your shapes; you own only the screen that produces
them.

## UI craft — make it feel designed

An **Operate** surface on a phone, one thumb. Load `impeccable`; the repo tokens win.

- **Tap-to-place everywhere.** A selected item shows a clear "lifted" state (`border-cyan`,
  `bg-cyan-bg`); its destination highlights as the drop target. Tap the destination to place.
  Never drag.
- **Order/assemble**: the pool is the source, the result rail is the destination; both scroll
  independently on a long card. Each placed item stays tappable to move or send back.
- **Match/bucket**: left column and right column(s); tapping a left item arms it, tapping a
  right slot locks the pair. A locked pair can be unlocked by tapping it again. Bucket renders
  exactly one tick per row (the constraint is visual, not just graded).
- **Claim grid**: every row shows True/False as two tap targets; both states are always
  reachable and an un-answered row reads "answer every row" before it will submit.
- ≥44px targets, visible focus, `aria-pressed`/`aria-label` on every interactive cell, motion
  via `tw-animate-css` honouring `prefers-reduced-motion`.

## Tests

Five specs, one per primitive, against seed rows you add (append to `seed-data.ts` / insert at
the end of `scripts/seed-e2e.ts`; never remove B's or C1's rows):

- `ordering` — placing items in a valid order marks correct; two items swapped marks wrong; the
  result screen shows the correct order and why.
- `pairing` — matching all pairs right is correct; one wrong pair is wrong; unlocking and
  re-matching works.
- `bucketing` — every item lands in a column and one tick per row is enforced in the UI.
- `assembling` — building the line from the pool is correct; a wrong token in the middle is
  wrong. A templated (word-bank) card shows the pre-filled tokens and only asks for the gaps.
- `claimgrid` — marking every row true/false and getting them all right is correct; one wrong row
  is wrong; the form refuses to submit with a row unanswered.

Unit tests: only for pure helpers you extract (e.g. the ordered→constraint check is B's, not
yours — do not reimplement it).

## Traps

- **Do not touch `card.tsx`, `feed.spec.ts`, `tapspot.spec.ts`, or any `check-*.ts`.**
- **Drag is banned.** If you reach for `@dnd-kit` or pointer-drag, stop; the design forbids it.
- **Assemble and order are the same grading shape but different screens.** Share nothing except
  the `ordered` answer; do not make assemble a special case of order in the code.
- **Bucket is a constrained grid, not a free mapping.** Enforce one-tick-per-row in the UI.
- **Claim grid forces every row.** "Select the true ones" lets a reader skip; the grid must not.
- **Long pools scroll.** A five-item order at 390px fits without scrolling; an eight-item one
  scrolls its pool only, never the page.

## Verification

Full README list. Each of the five specs with `--retries=0` at least three times. Screenshots at
390px and 1440px of every primitive. Report token count and bundle KB.

## Decisions (with cost if wrong)

- **A locked match/bucket pair is reversible (tap to unlock).** Cost if wrong: none — the grader
  only sees the final pairs; reversibility is free and prevents an accidental tap costing a card.
- **Claim grid submits only when every row is answered.** Cost if wrong: a reader who wants to
  skip one row cannot, which is exactly the point of the grid, but it is also the harshest card
  in the catalogue — flag in the PR if the seed makes it feel unfair rather than harder.
