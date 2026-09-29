# Part C3 — numeric, grid toggle, and the why-step

**Branch** `feed-v2-ui-c3` · **Worktree** `../90X-wt-fv2/c3` · **Specs** `keypad`, `gridtoggle`,
`whystep` (three files).

Read `.planning/feed-v2/plans/README.md` first. Depends on **B** (dispatch, shapes, stubs). Do
not start until B is merged. C3 is last of the C parts and owns the **why-step**, which is a
second screen on the same card — the only place in C that touches `card.tsx`'s flow, not just a
primitive file.

## Scope

- **Numeric entry** (`number`): a keypad, not a text input — three taps, nothing to phrase.
- **Grid toggle** (`chosen`): a small matrix (structures × operations); tick the cells.
- **Why-step** (`chosen`, second): after a correct answer on a Hard card, pick the reason. Both
  halves must be right (B already grades it; you build the screen).

## Files

**Modify (replace B's stubs)**
- `web/src/components/feed/primitive/numeric.tsx`
- `web/src/components/feed/primitive/grid-toggle.tsx`

**Modify (the one C part that may)**
- `web/src/components/feed/card.tsx` — add the why-step phase: after a correct main answer on a
  card with `card.whyStep`, show the reason options, then submit `{ ..., why }`.

**Create**
- `web/src/components/feed/primitive/why-step.tsx`
- `web/e2e/keypad.spec.ts`, `web/e2e/gridtoggle.spec.ts`, `web/e2e/whystep.spec.ts`

## Reuse, do not rewrite

```
Answer shapes: { shape: "number"; value: number }, { shape: "chosen"; picked: number[] }
AnswerInput's `why?: number` (B)                            // @/lib/feed/view
gradeCard's why-step rule (B, do not reimplement)           // @/lib/feed/grade
submitAnswer(sent) -> AnswerState                           // @/app/actions/feed
PRIMARY, SECONDARY, button()                                // @/components/button-styles
Markdown                                                    // @/components/markdown
useServerAction                                             // @/components/form
```

Read `card.tsx`'s `Phase` state machine before adding the why-step phase: it is `ask →
(result | self_mark | saved)`. You add a `why` step between `ask` and submit, and only for cards
whose `card.whyStep` is present. B's `feed.spec.ts` has no Hard card, so nothing there changes.

## UI craft — make it feel designed

An **Operate** surface, one thumb. Load `impeccable`; the repo tokens win.

- **Keypad**: a real grid of digit keys (and a backspace, a negative sign, and a decimal point
  where the card allows it). Every key ≥44px, `aria-label` per key. Show the running value
  large, `text-display`, so a glance confirms the number. No `<input>` — the keypad is the input.
- **Grid toggle**: the smallest viable grid is 3×3 and it already scrolls at 390px; cap it there.
  Structure names down the side, operations across the top. A ticked cell is `bg-cyan-bg` +
  `border-cyan`; re-tap to untick. `aria-label` every cell ("<structure>, <operation>").
- **Why-step**: a distinct second screen on the same card, with a small "the answer, then the
  reason" stepper so the reader knows why a second question appeared. The reason options are
  plausible mistakes (the owner judges their plausibility at Gate 3 — surface them honestly,
  never as obvious straw men).
- Motion via `tw-animate-css`, honour `prefers-reduced-motion`.

## Tests

- `keypad` — tapping digits builds the number; the correct value marks correct, an off-by-one
  marks wrong; backspace corrects before submit.
- `gridtoggle` — ticking the correct cells marks correct; one wrong cell marks wrong; untick
  works.
- `whystep` — a correct answer with the right reason marks correct; **a correct answer with the
  wrong reason marks wrong** (this is the decision under review at Gate 3; pin it in the spec so
  it is visible when it changes); a wrong main answer never reaches the why-step.

Seed rows for numeric and grid-toggle and one Hard why-step card appended to `seed-data.ts`
and inserted at the end of `scripts/seed-e2e.ts`.

## Traps

- **The why-step only appears after a correct answer.** A wrong answer goes straight to the
  result. Do not show the reason screen for a wrong main answer.
- **`card.tsx` is shared; you are the only C part allowed to touch it**, and only the why-step
  phase. Do not refactor the rest of the card.
- **Keypad is not a `<input type="text">`.** A native text input on mobile opens a system
  keyboard and reintroduces "typing", which the design removed. The keypad is buttons.
- **Grid toggle caps at 3×3.** A 4×4 grid at 390px is nine+ taps and a scroll that defeats the
  card's purpose.
- **Do not touch `feed.spec.ts`, the other C parts' specs, `seed-data.ts`'s existing rows, or any
  `check-*.ts`.**

## Verification

Full README list. The three specs with `--retries=0` at least three times, plus `feed.spec.ts`
still green. Screenshots at 390px and 1440px of the keypad, the grid, and the why-step. Report
token count and bundle KB.

## Decisions (with cost if wrong)

- **The why-step stepper is two dots, not a page.** Cost if wrong: if it feels like a second
  card, it breaks the "one card, one mark" model; if it feels like nothing happened, the reader
  misses that a reason is being asked. The stepper is the cheap way to say both.
- **Keypad supports decimals only where the card's tolerance implies them.** Cost if wrong: an
  integer-count card with a decimal pad invites a wrong-typed answer; a decimal estimate with
  only integer keys cannot be answered.
