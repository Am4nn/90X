You are building **unit 1d of the 90x reorg wave: the Coach chat's working state**.

**Worktree** `../90X-wt/1d` · **Branch** `coach-chat` · **Playwright spec** `web/e2e/chat-state.spec.ts`

Other agents may be building units 1a, 1b, 1c, 3 and 4 at the same time in their own
worktrees. Never touch their files.

## Read these first, in this order

1. `.planning/reorg/plans/prompts/SETUP.md` — your environment, how to test, every gate, the
   forbidden files, the PR format. **Read it before you write any code**; it contains the one
   flag (`E2E=1`) without which no test can sign in, and you will need the fake model running.
2. `.planning/briefs/README.md` — how this codebase is written. Wins over everything.
3. **`.planning/reorg/plans/1d-chat-working-state.md` — your plan.** It includes a table of
   every state in `chat.tsx` with line numbers. Read that table before you touch the file.
4. `.planning/reorg/plans/README.md` — the wave's cross-cutting decisions.
5. `.planning/reorg/me-coach-reorg.brief.md` — the "Chat upgrade" section.
6. `.planning/reorg/DECISIONS.md` — the "Coach chat" section.
7. `.planning/reorg/mocks/chat.html` — the visual reference.
8. **`web/e2e/coach.spec.ts`** — the existing contract for this component, and the thing you
   are most likely to break. Read it and how it drives `e2e/fake-model.ts` before writing
   your own spec.

## What you are doing

While the Coach works, the chat prints a flat list of "Looked up…" lines, one per tool call,
and the "you can close the app" note sits in the same visual register as the reply. Make the
working state one quiet line with a progress count, put the detail behind a "Checked N
things" line that expands, set the note apart, and give replies a shape.

## This is the highest-risk unit in the wave

`chat.tsx` is 366 lines holding eleven states that all have to keep working: Stop, the
stop-failed note, the cut-off note, offline, the rate-limit pause, End, the degraded-model
note, proposal cards, citations, starters, and the error alert. Your plan lists them with
line numbers.

**Change how it looks, not what it does.** No change to the transport, the request body, tool
semantics, or what a tool returns. This is a presentation change.

## The five traps that will cost you most

1. **`ToolLine`'s failure test must stay in one place.** It treats a step as failed on
   `state === "output-error"` or an `output.error`. Your new summary helper must use that same
   test, not a reimplementation of it — two copies that disagree is a bug that only appears on
   a failing tool call.
2. **A failed check must stay visible in the collapsed state.** A silent failure hidden behind
   a fold is worse than the flat list you are replacing.
3. **Never post-process what the Coach said.** "Replies lead with a bold line, then short
   bullets" is done in the prose styles, not by parsing or rewriting the model's text.
4. **`coach.spec.ts` reads the fake model's request log**, which is why the e2e shard runs
   with `workers: 1`. Do not add parallelism or a second fake-model server.
5. **Do not reword any existing warning.** Stop, offline, rate-limit, cut-off, stop-failed,
   degraded: same words, same triggers. `KeepOpen` keeps its text and its `slow` timer.

The one piece of real logic is the summary helper in `web/src/lib/coach/chat-rules.ts` —
something of the shape `workingSummary(parts) -> { label, done, total, failed } | null`,
returning `null` when there are no tool parts so a plain reply renders no line. **TDD it**:
write the test, watch it fail, implement, watch it pass.

## Verification

Everything in SETUP.md, plus `bun run check:coach-tools`.

Your spec must be `web/e2e/chat-state.spec.ts`, run with `--retries=0` at least three times.
**Also run the whole of `web/e2e/coach.spec.ts`** — it is the existing contract for this
component and the thing this unit is most likely to break. Report both.

Screenshots at 390px and 1440px: mid-reply with the working line, and a finished reply with
the "Checked N things" line both collapsed and expanded.

Report back as SETUP.md section 8 describes, and say explicitly which of the eleven states
you exercised and which you only read.
