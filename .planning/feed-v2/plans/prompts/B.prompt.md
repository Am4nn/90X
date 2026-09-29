You are building **Part B of Feed v2: the grader, pure**.

**Worktree** `../90X-wt-fv2/b` · **Branch** `feed-v2-grader` · **Spec** rewrites `e2e/feed.spec.ts`.

You depend on **A** (the `archetypes.ts` module and the answer columns). Do not start until A is
merged. You remove typed from the Feed: every Feed answer is marked by a pure function, and
`gradeWithAi` stays in `grader.ts` for mocks and reviews but leaves every Feed path.

## Read these first, in this order

1. `.planning/feed-v2/plans/prompts/SETUP.md`
2. `.planning/briefs/README.md`
3. **`.planning/feed-v2/plans/B-grader.md` — your plan.** The pure-grader contract, the named
   test cases, the stub seam that lets C1/C2/C3 own disjoint files, the traps.
4. `.planning/feed-v2/plans/README.md`
5. `web/src/lib/feed/grade.ts`, `grader.ts`, `view.ts`, `service.ts` — read the current
   signatures before you change anything; the plan lists exactly what to keep and what to
   replace.

## The traps that will cost you most

1. **`gradeWithAi` stays exported.** Mocks and the Coach call it; `web/scripts/check-grading.ts`
   (the orchestrator's) still imports it. Remove it from `service.ts` only.
2. **You do not touch `web/scripts/check-feed.ts`.** The orchestrator extends it after you land.
3. **The `AnswerInput` union is zod-validated in `app/actions/feed.ts`.** Widen the zod schema in
   lockstep with `view.ts` or every answer 400s. Add `why` only on the four shaped shapes.
4. **Ordering grades against constraints, not one blessed sequence.** A free clause order must
   not mark a correct answer wrong — that is the exact bug PRIMITIVES warns about.
5. **The seed drives `feed.spec.ts`.** Re-cast `LIVE_CARDS` to `pick_one` and `self_rate`; no
   `typed`, no `output`, no numeric/order (those are C2/C3's to seed).

## Verification

Full SETUP.md §5 list. Run `e2e/feed.spec.ts` with `--retries=0` **at least three times**, and
run the Vitest suite three times too — this is the one part where "no test passes on a retry"
must be visibly true. `bun run check:feed` should still pass. Report token count and bundle KB.

Report back as SETUP.md §10 describes.
