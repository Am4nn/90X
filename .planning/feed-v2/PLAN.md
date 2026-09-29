# Feed v2 — implementation plan

**Status:** written 2026-09-30, after four rounds of discussion. Everything here rests on
`DECISIONS.md`; where this plan and that file disagree, `DECISIONS.md` wins and this file is
wrong.

## Context

The Feed today is 2,808 cards in five formats, of which **1,383 are typed** — prose answers
graded by a model. Typed is the only format that costs money to mark, the only one that can
mark two identical answers differently, and the one Aman says nobody will use. A reviewer
separately said the cards are too easy.

Measuring both complaints turned up the thing that shapes this plan: **25 of the 26 Hard cards
are typed.** Removing typed without a difficulty target would delete almost all the hard
content and leave a Feed of 11 Easy multiple-choice cards and 28 Easy flashcards — making the
complaint worse. So difficulty is a constraint on the rebuild, not a follow-up to it.

What replaces it: **47 archetypes over 11 primitives and 4 answer shapes, every one graded by a
pure function.** No model in the loop when an answer is marked.

## What changes

| | today | after |
|---|---|---|
| formats | `typed · flash · mcq · output · bug` | 11 primitives, archetype as a separate field |
| grading | `gradeOption` + `gradeWithAi` for typed | pure functions only; `gradeWithAi` leaves the Feed |
| answer shapes | option index, prose, self-mark | chosen set · ordered list · mapping · number |
| format choice | whatever the writer produced | a per-topic budget the writer fills on request |
| difficulty | a text label the writer assigned itself | rubric at write time, calibrated from outcomes |
| session | whatever FSRS surfaces | a difficulty mix that adapts, plus a reader toggle |
| guessability | nothing checks it | a three-sample blind gate before a card ships |
| corpus | 2,808, flat ~10 per topic | ~3,000, weighted by `topics.importance` |

## The one rule that keeps this from drifting

**The archetype registry is a single file that both the pipeline and the app read.**

`archetypes.json` at the repo root: for each archetype, its id, primitive, answer shape,
eligible areas, difficulty range, and whether it takes a why-step. Python reads it directly.
The app gets a generated typed module from it — the same pattern as `db/pulled`, with a
`check:archetypes` gate that fails when the generated file is stale.

Without this there are two lists, and the first time they disagree the pipeline writes cards
the app cannot render. That failure is silent in the pipeline and fatal in the Feed.

## The answer contract

Four shapes. Everything downstream — storage, grader, attempt record — understands exactly
these and nothing else.

```ts
type Answer =
  | { shape: "chosen"; picked: number[] }        // pick one, grid toggle, tap in place
  | { shape: "ordered"; order: number[] }        // order, assemble
  | { shape: "mapping"; pairs: [number, number][] } // match, bucket, claim grid
  | { shape: "number"; value: number };          // numeric entry
```

A card stores what makes an answer correct, per shape: `picked` for chosen, **ordering
constraints** rather than one sequence for ordered, a one-to-one `pairs` for mapping, and
`value` + `tolerance` for number. A why-step, where present, is a second `chosen` answer.

**Both halves must be right.** A Hard card answered correctly with the wrong reason is marked
wrong — see the note in `DECISIONS.md` round 4, and judge it in review before trusting it.

---

## The eight parts

Ordered by dependency. A and B are the contract; nothing else is safe until they exist.

### A — Schema and the registry *(lead: contains a migration)*

- `supabase/migrations/<next>_feed_v2.sql` — `cards.archetype`, the answer-definition columns,
  ordering `constraints` jsonb, numeric `tolerance`, `why_step` jsonb, `status` gains
  `retired`, and the observed-outcome columns the difficulty calibration writes.
- `archetypes.json` + the generator + `check:archetypes`.
- `bun run db:pull` and `db:types` afterwards; `web/src/db/schema.ts` re-exports as usual.
- Python side: `pipeline/src/pipeline/staging.py` and `publish.py` learn the new columns.

**Done when** a card with each of the four shapes can be inserted and read back, and the
registry's TS and JSON cannot disagree.

### B — The grader, pure

- `web/src/lib/feed/grade.ts` — one pure function per primitive over the four shapes.
  `CardFormat` goes; the primitive comes from the registry.
- Ordering grades against **constraints**, so every genuinely correct order passes.
- Numeric grades `|given − expected| <= tolerance`.
- The why-step rule: both halves right, or the card is wrong.
- `web/src/lib/feed/grader.ts` — `gradeWithAi` stays in the file for mocks and reviews and is
  **removed from every Feed path**.
- `web/scripts/check-feed.ts` gains cases per primitive.

**Done when** every primitive has Vitest cases including two-valid-orderings, a numeric
boundary at exactly the tolerance, and a right-answer-wrong-reason card. This part is all pure
functions and should be the best-tested code in the app.

### C — The eleven card UIs

- `web/src/components/feed/card.tsx` dispatches on primitive; one component per primitive
  beside it.
- **Tap-to-place everywhere, never drag** — tap the item, tap its destination. Drag inside a
  scrolling page fights the scroll, and tap is reachable by keyboard and screen reader without
  extra work.
- Numeric entry is a keypad, not a text input.
- The why-step is a second screen on the same card.
- Mobile first at 390px. Grid toggle caps at 3×3; claim grid at 4 rows.

Split for parallel work: **C1** the three that exist in some form (pick one, self-rate, tap in
place) · **C2** the five new mapping and ordering screens · **C3** numeric, grid toggle and the
why-step.

### D — Session selection and difficulty

- `web/src/lib/feed/service.ts`, `srs.ts`, `view.ts` — the queue gains a difficulty mix:
  rolling accuracy over the last ~20 answers, target 70–85% correct, `profiles.level` as the
  starting point.
- **The reader's toggle shifts the mix, it never filters.** "Harder" raises the share of Hard in
  the pool; no card becomes unreachable, and FSRS scheduling is untouched.
- The toggle lives with the other Feed preferences (`topic-toggle.tsx` is the precedent).

**Done when** a seeded reader at 95% accuracy is served a measurably harder mix than one at
50%, proven by a test over the pure selection function rather than by inspection.

### E — Generation *(pipeline)*

- `pipeline/src/pipeline/cards/` — `generate.py` and `from_lessons.py` take an archetype and
  write that one thing. The writer **never chooses** the format and **may refuse**: no natural
  sequence for this topic, and the budget refills with another archetype.
- Budget per topic: count ∝ `topics.importance`, spread equally across the archetypes eligible
  for that area.
- **Hard cards may draw on `problems.statement_md` and pattern tricks**, not only the lesson —
  a three-step question needs a concrete situation. Source refs credit them as they already do.

### F — The gates *(pipeline)*

- **Blind gate**, new: the options alone, no lesson, no topic, **three samples, reject at two or
  more correct.**
- **Structural rules**, free: options within a length band, no option that is the only one of
  its kind, no all-of-the-above.
- **Difficulty rubric** (`DECISIONS.md` round 3 table) assigns Easy/Medium/Hard.
- `fix.py` repairs rejects; `regate.py` re-judges against the lesson as it already does.

### G — Review

- `pipeline/src/pipeline/cards/review_pack.py` samples **two per archetype, ~94 cards**, grouped
  by archetype rather than shuffled.
- `web/src/app/admin/cards/**` renders every primitive, since a reviewer cannot judge a card
  they cannot see.
- The verdict is per archetype — *does this earn a place* — not per card.

### H — Publish and the swap

- Publish the new corpus as **`draft`** so it is invisible.
- Deploy the app.
- **Then one statement** flips new to `live` and old to `retired`.
- `card_state` on retired cards is **kept**, unscheduled. Deleting it would drop everyone's
  readiness dial on release day.

Publishing before deploying is the mistake that took production down on 2026-09-29. The order
is not a preference.

---

## Sequencing, and the three measurement gates

```
A (schema + registry)
  └─ B (grader)  ──┬─ C1 C2 C3 (UIs, parallel)
                   └─ D (selection)
A ─ E (generation) ─ [GATE 1] ─ F (gates) ─ [GATE 2] ─ full run ─ G (review) ─ [GATE 3] ─ H
```

**Gate 1 — one topic, then price it.** Generate one topic's cards and measure the cost. The
original pass averaged ~$0.0017 a card; structured formats carry more fields. Do not run 274
topics on an estimate.

**Gate 2 — fifty cards through the blind gate.** If it rejects half, the gate is wrong, not the
corpus. Check before spending the rest.

**Gate 3 — the 94-card review.** The first thing to judge is whether why-step wrong reasons are
genuinely plausible. If they are not, the right-answer-wrong-reason rule punishes a writing
failure, and it should be relaxed before release rather than after a complaint.

## Verification

Per part, from `web/`: `typecheck`, `lint`, `test`, `format:check`, `check:tokens`,
`check:dead`, `check:dupes`, `check:cycles`, `check:coverage`, `check:deps`, `check:actions`,
`build` + `check:bundle`, `check:feed`, `check:archetypes`, and `check:rls` / `check:tracker`
where the part touches them. Playwright: the existing `feed.spec.ts` must keep passing, plus
one spec per new primitive, run with `--retries=0`.

Pipeline: `pytest`, and the structural gate's own tests.

**No test may pass on a retry.** That rule caught a real bug twice in the reorg wave.

## Budget

| step | estimate |
|---|---|
| generate ~3,000 structured cards | ~$5–7 |
| blind gate, three samples | ~$3 |
| difficulty rubric | ~$1 |
| repair pass | ~$1 |
| **total** | **~$10–12** |

Against $20 approved for this work. Gate 1 exists so the generation number is measured rather
than trusted.

## The three risks worth naming

1. **The registry drifting from the app.** Mitigated by generating the TS from the JSON and
   gating on staleness. Without that, the pipeline writes cards the Feed cannot render, and
   nothing notices until a reader sees a blank card.
2. **Right-answer-wrong-reason being too harsh.** It is a decision that follows from two others
   rather than one anybody argued for. Gate 3 is where it gets tested.
3. **The new corpus being no harder than the old one.** The rubric labels difficulty; it cannot
   conjure a three-step question out of a lesson with four claims. That is why E may read
   problem statements, and why the honest fallback is fewer Hard cards rather than Hard labels
   on Medium questions.
