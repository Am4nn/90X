# Part C1 — the three UIs that exist in some form: pick one, self-rate, tap in place

**Branch** `feed-v2-ui-c1` · **Worktree** `../90X-wt-fv2/c1` · **Spec** `e2e/tapspot.spec.ts`.

Read `.planning/feed-v2/plans/README.md` first. Depends on **B** (the dispatch, the `Answer`
shapes, the stubbed primitive files). Do not start until B is merged.

C1 turns B's minimal pick-one and self-rate shims into real, polished components and builds
**tap in place**. These three are the primitives that already existed in some form (`mcq`,
`flash`, `bug`-as-typed), so C1 owns the interaction the existing `feed.spec.ts` already
exercises and must keep it green.

## Scope

- **Pick one** (`chosen`): a direct option list — tap the option, it submits. No textarea, no
  "Show options". Keyboard navigable, ≥44px targets.
- **Self-rate** (`self_rate`): the "got it / missed it" pair, now a first-class screen.
- **Tap in place** (`chosen`): a code/plan snippet where the reader taps the one correct token
  or line.

## Files

**Modify (replace B's shims)**
- `web/src/components/feed/primitive/pick-one.tsx`
- `web/src/components/feed/primitive/self-rate.tsx`
- `web/src/components/feed/primitive/tap-in-place.tsx`

**Create**
- `web/e2e/tapspot.spec.ts` — tap-in-place + self-rate

## Reuse, do not rewrite

```
card: CardView, userId, onAnswered, onNext, nextPending, nextError   // FeedCard props (card.tsx)
submitAnswer(sent) -> AnswerState                                    // @/app/actions/feed
Answer shapes: { shape: "chosen"; picked: number[] }, { selfMark }   // @/lib/feed/view
PRIMARY, SECONDARY, button({ size })                                 // @/components/button-styles
Markdown                                                            // @/components/markdown
areaDot                                                             // @/lib/admin/review
useServerAction                                                      // @/components/form
```

The `PrimitiveScreen` seam (in `card.tsx`, owned by B) already calls your components with the
card and a submit callback; match its props exactly — read `card.tsx` and `primitive/not-built.tsx`
before writing anything. Do not edit `card.tsx`.

## UI craft — make it feel designed

This is an **Operate** surface: someone answering a card on a phone, one thumb, in a gap. Load
the `impeccable` skill and follow its craft floor, but the repo tokens win (six text sizes,
token colours, borders not shadows, dark theme, mobile-first 390px).

- **Pick one**: option as a full-width row, letter index + text, `hover:border-cyan` and
  `aria-pressed`-style selected state, one subtle press state. The chosen answer should feel
  like the only thing on screen.
- **Self-rate**: two large, obviously-different buttons — "Missed it" secondary, "Got it"
  primary — with copy that is a judgement, not a menu.
- **Tap in place**: render the snippet with each candidate line/token as a tappable target;
  `aria-label` the targets ("Line 3: <text>"); a selected token gets `bg-cyan-bg` + `border-cyan`
  and reads back to the screen reader. Tap, then the answer submits (or a single confirm — your
  call, but never drag).
- Motion via `tw-animate-css`, honour `prefers-reduced-motion`. No decorative-only animation.

## Tests

`e2e/tapspot.spec.ts`, against the seeded cards (you add the tap-in-place seed rows — see
`e2e/seed-data.ts`; append, do not remove B's rows):

- Tapping the correct token in the snippet marks the card correct and shows the answer.
- Tapping a wrong token marks it wrong and highlights the correct one.
- The token targets are keyboard-reachable: Tab to the target, Enter submits.
- Self-rate "Got it" records a correct, "Missed it" a wrong, and both move to the next card.
- `feed.spec.ts` still passes (pick one and self-rate behaviours you did not change).

Unit tests: only if you extract a pure helper (e.g. tokenising a snippet into targets). Do not
component-test with Vitest here.

## Traps

- **Do not touch `card.tsx`, `feed.spec.ts`, `seed-data.ts`'s existing rows, or any `check-*.ts`.**
  Add seed rows at the end of `seed-data.ts` and insert them at the end of `scripts/seed-e2e.ts`.
- **Pick one submits on tap, not on a separate "Check".** The "Check" button belongs to the old
  typed flow and is gone for chosen sets. If you re-add it, `feed.spec.ts` (B's version) breaks.
- **No drag.** Tap-to-place only. Drag fights the scroll at 390px.
- **The snippet in tap-in-place is data, not JSX written by hand.** Derive targets from
  `card.options`/the snippet field B's `CardView` gives you; do not hardcode.
- **Keep the reload/offline invariants.** Tap-in-place submits through the same `submitAnswer`
  path as everything else; the `clientId` idempotency still applies.

## Verification

Full README list. `e2e/tapspot.spec.ts` with `--retries=0` at least three times, and
`e2e/feed.spec.ts` too. Screenshots at 390px and 1440px of all three primitives, taken from the
running app. Report token count and bundle KB.

## Decisions (with cost if wrong)

- **Tap-in-place uses a single tap then immediate submit** (no confirm step). Cost if wrong: an
  accidental tap costs a wrong answer; a confirm step costs a tap on every card. The former is
  recoverable by the card returning in rotation; the latter is permanent friction.
