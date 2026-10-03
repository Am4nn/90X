# Feed card UI: implementation plan

Spec (binding): `.planning/design_handoff_feed_card/README.md` and the prototype `Feed Card.dc.html`
(its logic class is the behaviour spec). Where this plan and the handoff differ, the handoff wins
unless a decision below says otherwise. Plan status: **draft for Aman's review. No code written.**

## Decisions (from the Q&A, 2026-10-03)
- Replace in place, no flag. About 6 PRs by stage. Drag last, own PR.
- Drift control: render every primitive, asking and answered, from the prototype's 22 sample cards;
  screenshots at 390 and 1240 wide go into each PR beside the prototype's. Aman reviews them.
- Skip follows the mock: next card at once, answer not shown, counted Skipped. Only "New to me" reveals.
- Stars are the curation feedback (1-2 Bad, 3 Normal, 4-5 Good); Report = should-be-removed.
  Footer shows after Correct / Not quite / New / Known, never after Skip.
- Editor header: language and line count (no invented file names).
- "Next review" text reports the real scheduler (`srs.ts`). Mock numbers are samples.
- Today Correct = correct / graded, skips excluded, resets at local midnight (profile timezone).
- Overall report hides an area with fewer than 3 graded answers; empty days read "No answers yet".
- Non-card Feed chrome (topic/difficulty toggles, diagnostic intro/summary, empty states) is restyled
  to match. **Not designed by Aman: I will propose, he approves from screenshots.**
- Area colours for LLD, AI, Behavioural: I propose three, he approves, then they go in `DESIGN.md`.
- Assemble equivalent-order question (item 17) is measured after the redesign, not in it.
- Mobile Next-card bar sits above the tab bar; content is padded so the card scrolls fully clear of both.
- Percentage: none on binary verdicts. Compose keeps its rubric % (this already equals today's behaviour).

## What exists vs what is new (checked in code)
| Mock element | Today | Work |
|---|---|---|
| 11 primitives, ask + result | all exist (`components/feed/primitive/*`, `review.tsx`) | restyle, behaviour per handoff |
| Numeric keypad | exists (`numeric.tsx`, `e2e/keypad.spec.ts`) | restyle + keyboard + hints |
| Skip / New to me / Known / retire offer | exist (`card.tsx`) | Skip semantics change; restyle |
| Why this card, Today | exist (`feed.tsx`) | restyle; mobile placement; Overall report is new |
| Stars | **do not exist** | new table, action, UI |
| Report | `components/feed/report.tsx`, `card_flags` | restyle to inline textarea |
| Drag | none | new, last |
| Per-answer history | `card_reviews` (user, card, outcome, created_at) | enough for the report; no new infra |

## Stages (one PR each)
Every PR: gates `typecheck lint test format:check check:tokens check:dead check:dupes check:cycles
check:coverage build check:bundle`, relevant e2e specs, screenshots 390 and 1240 beside the prototype's.

### PR 1: Tokens, card shell, verdict, actions
- `DESIGN.md` and `globals.css`: only tokens the handoff uses that are missing (rating ramp, area colours).
- `components/feed/card.tsx`: verdict ring and words (Correct / Not quite / Skipped / New to you / Marked as known),
  meta row, prompt and code block, hint, action row (`1fr 2fr`), quiet links, answer and key points, retire offer.
- Skip: `service.ts` returns without the answer; client advances to the next card; Skipped count increments.
- Keep accessible names that e2e relies on: "Skip", "Check answer", "Next card", "Skip for now".
- Tests: view tests for verdict wording; e2e `feed.spec.ts` updated for Skip (no reveal).

### PR 2: Footer card, stars, report
- Migration `card_ratings (user_id, card_id, stars 1-5, updated_at)`, RLS owner-only, upsert; clear on re-tap.
  **Production migration only on Aman's explicit approval.**
- Server action to rate; `report.tsx` becomes the inline single-line textarea (300 chars), "Report sent" state.
- Footer: next review, lesson link or source, 84px label + 5 stars with ramp, Report.
- Admin: a simple aggregate (Good / Normal / Bad / Reported per card) on the existing flagged page. Minimal now.
- Tests: rating action unit + `check:rls` for the new table + e2e rate and clear.

### PR 3: Side blocks, Overall report, mobile layout, non-card chrome
- Why this card copy (new / due / weak); Today (Answered / Correct % / Skipped).
- `lib/feed/report.ts`: lifetime, by area (vs 70% mark, hide <3), last 7 days; from `card_reviews` joined to topic area.
- Desktop: sticky 280px column. Mobile: after answering only, Today then Why, below the footer. Pinned Next bar above the tab bar.
- Restyle topic/difficulty toggles, diagnostic intro and summary, empty states (proposal screenshots first).
- Tests: report maths (timezone boundary, <3 rule, empty days), e2e mobile layout (no overlap at 390).

### PR 4: Simple primitives
pick_one (+ "Now the reason"), self_rate, tap_in_place editor with inline review comment, numeric restyle,
claim_grid sliding switch (tap selected side again clears), compose rubric box. Update the matching e2e specs.

### PR 5: Complex primitives (tap behaviour only)
match, order (wrong-way-round list and the rules), bucket, assemble, grid_toggle "Lights".
Answered states keep the question's own shape. Update pairing, ordering, bucketing, assembling, gridtoggle specs.

### PR 6: Drag
Pointer Events on match, order, bucket, assemble; 6px threshold, click suppression, grip handle,
touch drags from chips and tokens, order steps from the grip only, auto-scroll within 56px. Tap stays unchanged.
Test on a real phone before merge. Can slip without blocking anything.

## Traps
- `check:tokens` is an equality ratchet and `check:bundle` has a total ceiling; report measured numbers in the PR, do not edit ceilings.
- Existing e2e specs find controls by name; renaming a control breaks them silently in CI only.
- Never mark with colour alone: glyph plus word on every right/wrong mark.
- Min hit target 44px. No hover dependence (touch).
- Controls must not cover content (Aman's standing complaint).
- Skip no longer reveals: check the diagnostic flow and the queue still advance, and that a skipped card is not re-served immediately (`servableFor`).
- The tab bar and the pinned Next bar both fixed: pad the scroll container for both.
- Prototype controls (View, picker, sample miss) are not shipped.

## Open items for Aman
1. Approve area colours and non-card chrome from screenshots (PR 1 and PR 3).
2. Approve the `card_ratings` production migration when PR 2 is ready.
3. Review-page shape: PRs carry screenshots only, taken from a local fixtures run that is not shipped.
