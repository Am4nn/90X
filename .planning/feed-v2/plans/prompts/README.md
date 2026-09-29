# Hand-off prompts — paste one, say nothing else

One file per part. Paste the whole file as the agent's first and only message. It names the
worktree, the branch, the spec, everything to read, the traps that part will hit, and what to
report back. No follow-up prompting needed.

| Part | Prompt | Branch | Spec |
|---|---|---|---|
| A | `A.prompt.md` | `feed-v2-schema` | — |
| B | `B.prompt.md` | `feed-v2-grader` | rewrites `e2e/feed.spec.ts` |
| C1 | `C1.prompt.md` | `feed-v2-ui-c1` | `e2e/tapspot.spec.ts` |
| C2 | `C2.prompt.md` | `feed-v2-ui-c2` | `ordering` `pairing` `bucketing` `assembling` `claimgrid` |
| C3 | `C3.prompt.md` | `feed-v2-ui-c3` | `keypad` `gridtoggle` `whystep` |
| D | `D.prompt.md` | `feed-v2-selection` | — (Vitest) |
| E | `E.prompt.md` | `feed-v2-generation` | — (pipeline) |
| F | `F.prompt.md` | `feed-v2-gates` | — (pipeline) |
| G | `G.prompt.md` | `feed-v2-review` | — (pipeline + admin) |
| H | `H.prompt.md` | `feed-v2-swap` | — (pipeline) |

`SETUP.md` is shared and every prompt tells the agent to read it first: environment, testing
rules, the full gate list, forbidden files, PR format.

## Dependency order

```
A (schema + registry)
  └─ B (grader) ──┬─ C1 C2 C3 (UIs, parallel)
                  └─ D (selection)
A ─ E (generation) ─ [GATE 1] ─ F (gates) ─ [GATE 2] ─ full run ─ G (review) ─ [GATE 3] ─ H
```

**A lands first and alone.** Then B. Then C1/C2/C3 and D in parallel. E and F alongside once A
is in. G needs B and C. H is last.

**Run two or three agents at a time, not eight.** Playwright's `baseURL` is hardcoded to
`localhost:3000` and they share one local Supabase stack, so only one can run e2e at a time.

## The three hard rules (restated for the dispatcher)

1. No agent touches production. Migrations apply to the local stack only; never `db push` or
   `pipeline publish` against a real `.env.local` / `DATABASE_URL`.
2. No full generation run without a costed go-ahead. Gate 1 (one topic, cost per card) and Gate 2
   (50 cards, rejection rate) are stop-and-report points. `PIPELINE_MAX_USD` on every pipeline
   invocation; $20 total; report cumulative spend every time.
3. Only the orchestrator touches `web/scripts/check-*.ts` and `.github/workflows/ci.yml`.
