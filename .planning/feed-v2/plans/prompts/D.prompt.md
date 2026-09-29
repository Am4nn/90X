You are building **Part D of Feed v2: session selection and difficulty**.

**Worktree** `../90X-wt-fv2/d` · **Branch** `feed-v2-selection` · **No Playwright spec** — the
proof is a Vitest test over the pure selection function.

You depend on **B** (the answer shapes, for rolling accuracy). You run in parallel with C1/C2/C3.
Never touch their files.

## Read these first, in this order

1. `.planning/feed-v2/plans/prompts/SETUP.md`
2. `.planning/briefs/README.md`
3. **`.planning/feed-v2/plans/D-selection-difficulty.md` — your plan.** The pure mix function, the
   named test cases, the traps.
4. `.planning/feed-v2/plans/README.md`
5. `web/src/lib/feed/service.ts` (`pools`, `refill`), `queue.ts` (`buildQueue`),
   `components/feed/topic-toggle.tsx` — the precedent for the toggle.

## What you are doing

Give a session a deliberate difficulty mix instead of "whatever FSRS surfaces": rolling accuracy
over the last ~20 answers, target 70–85% correct, `profiles.level` as the starting point, plus a
reader toggle that **shifts the mix, never filters it**.

## The traps that will cost you most

1. **Never filter.** The toggle and the mix change probabilities, not membership. A deprioritised
   card must stay reachable.
2. **FSRS is untouched.** You bias which cards enter the queue, not their intervals.
3. **`observed_attempts`/`observed_correct` are global priors, not this reader's queue gate.**
4. **Rolling accuracy counts `correct`/`wrong` only** — `skip`, `new_to_me`, `known` carry no
   signal (`isGraded` already encodes this).
5. **Do not touch `card.tsx`, the C parts' files, `check-*.ts`, or `ci.yml`.** The toggle is a
   header action beside `TopicToggle`, not inside the card.

## Verification

Full SETUP.md §5 list. No new spec, but run `e2e/feed.spec.ts` to confirm the queue change did
not break it. Screenshots at 390px and 1440px of the Feed header with the toggle open. Report
token count and bundle KB.

Report back as SETUP.md §10 describes.
