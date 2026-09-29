# Unit 1d — the chat's working state

**Branch** `coach-chat` · **Worktree** `../90X-wt/1d` · **Spec** `e2e/chat-state.spec.ts`
**Brief** `.planning/reorg/me-coach-reorg.brief.md` (the "Chat upgrade" section)

Read `.planning/reorg/plans/README.md` first.

## Scope

While the Coach works, the chat prints a flat list of "Looked up…" lines — one per tool
call — and the "you can close the app" note sits in the same visual register as the reply.
This unit makes the working state one quiet line, sets the note apart, and gives replies a
shape. It is the only unit that touches the chat.

**This is the highest-risk unit in the wave.** `chat.tsx` is 366 lines holding nine states
that all still have to work. Change how it *looks*, not what it *does*.

## Files

**Create**
- `web/e2e/chat-state.spec.ts`

**Modify**
- `web/src/components/coach/chat.tsx`
- `web/src/lib/coach/chat-rules.ts` — add the pure summary helper

## The states that must all survive

Read these in `chat.tsx` before you change anything. Every one has to work afterwards, and
the e2e spec must not be the first place you find out:

| State | Where |
|---|---|
| Stop button and `halt()` → `/api/coach/stop` | ~199, 339 |
| `stopFailed` note | ~184, 215, 287 |
| Cut-off note ("stopped before answering") | ~260, 286 |
| Offline (`useOnline`, `blocked`, placeholder) | ~140, 180 |
| Rate-limit pause (429 → `pausedUntil`, `RATE_LIMIT_PAUSE_MS`) | ~141, 162, 166 |
| End thread (`endThread`, `ending`, `endNote`) | ~142, 237, 266, 290 |
| `degraded` ("lighter model until next month") | ~279 |
| Proposal cards (`parseProposal` → `ProposalCard`) | ~56 |
| Citations (`citationsOf` → the Sources list) | ~70 |
| Starters | ~300 |
| `errorText` with `role="alert"` | ~250 |

## Reuse, do not rewrite

```
toolLabel(name, phase)              @/lib/coach/chat-rules
  // phase is "running" | "done" | "error"; produces "Looking up X…",
  // "Looked up X", "Couldn't look up X" from TOOL_WHAT
citationsOf(parts)                  @/lib/coach/chat-rules
parseProposal(output)               @/lib/coach/proposals
ProposalCard                        @/components/coach/proposal-card
Markdown                            @/components/markdown
Ren                                 @/components/coach/ren     // already exists
isToolUIPart, getToolName           from "ai"
```

## What to build

**1. One quiet working line.** `AssistantMessage` currently maps every tool part to a
`ToolLine`. Replace that list, while the message is still streaming, with a single line:
the current activity plus progress — **"Checking your weak spots… · 3 of 4 checks done"**.

Add a pure helper to `chat-rules.ts` (it is where `toolLabel` and `TOOL_WHAT` already
live), something of this shape:

```ts
export type WorkingSummary = { label: string; done: number; total: number; failed: number };
export function workingSummary(parts: UIMessage["parts"]): WorkingSummary | null;
```

- `total` is the tool parts seen, `done` the finished ones, `failed` the ones in
  `output-error` or with an `output.error` — the same failure test `ToolLine` uses today,
  which must not drift. Read it; do not reimplement it from this description.
- `label` comes from `toolLabel` for the newest unfinished part, so the wording stays in
  one place.
- `null` when there are no tool parts, so a plain reply renders no line at all.

Unit-test that helper in `lib/coach/chat-rules.test.ts` (or a new test file beside it) —
this is the TDD piece of the unit.

**2. Keep the detail, one tap away.** The brief asks for a **"Checked N things"** line that
expands. Once the message is finished, collapse the tool steps behind it and render
today's `ToolLine` rows inside. Nothing is lost; it stops being the loudest thing on
screen. A failed check must still be visible in the collapsed label — a silent failure
behind a fold is worse than the flat list.

**3. Set the "close the app" note apart.** `KeepOpen` (~110, shown at ~285 when
`busy && slow`) currently reads like part of the reply. Make it muted and visually
separate. Same text, same trigger.

**4. Replies get a shape.** Assistant text comes through `Markdown` inside a bordered
card. Lead with the bold first line and keep bullets tight. Do this in the **prose styles**,
not by parsing or rewriting the model's text — never post-process what the Coach said.

**5. Ren where the Coach speaks.** Put Ren on assistant messages. `UserMessage` keeps its
`bg-cyan-bg` bubble. Ren already exists — consume it, do not modify it.

## Do not touch

`app/api/coach/chat/route.ts` and `stop/route.ts` · `lib/coach/tools.ts`, `modes/**`,
`model.ts` · `app/actions/coach.ts` · `coach/page.tsx` (1b) · `components/coach/ren.tsx`,
`proposal-card.tsx` · plus the README's forbidden list.

**No change to the transport, the request body, tool semantics, or what a tool returns.**
This is a presentation change.

## Tests

`e2e/chat-state.spec.ts` — `e2e/fake-model.ts` and `fake-model-data.ts` already exist and
`coach.spec.ts` drives the chat through them. Read that spec first and follow its setup.

- While a reply with tool calls is streaming, **one** working line shows, with a progress
  count — not a list of "Looked up…" rows.
- When it finishes, a "Checked N things" line is present and expands to the individual
  steps.
- A failing tool call is still visible without expanding.
- Citations still render as the Sources list.
- A proposal still renders as `ProposalCard`.
- Stop still stops; End still ends the thread.
- The offline placeholder still appears when the browser goes offline.

Run the **whole** `e2e/coach.spec.ts` as well, not just your own spec. It is the existing
contract for this component and it is the thing this unit is most likely to break.

## Traps

- `coach.spec.ts` **reads the fake model's request log** and the e2e shard runs it with
  `workers: 1` for that reason. Do not add parallelism or a second fake-model server.
- `ToolLine`'s failure test (`state === "output-error"` or `output.error`) must stay in one
  place. Two copies that disagree is a bug that only shows on a failing tool call.
- `useChat`'s `onFinish` calls `router.refresh()`. Leave it.
- `slow` gates `KeepOpen`. Keep the timer.
- Do not "improve" the copy of any existing warning. Same words.
- Six text sizes, token colours, borders not shadows.

## Verification

The README's full list, plus `bun run check:coach-tools`, your spec **and**
`e2e/coach.spec.ts`. Screenshots at 390px and 1440px: mid-reply with the working line,
and a finished reply with the "Checked N things" line both collapsed and expanded.
