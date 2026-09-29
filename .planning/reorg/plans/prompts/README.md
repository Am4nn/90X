# Hand-off prompts — paste one, say nothing else

One file per remaining unit. Paste the whole file as the agent's first and only message. It
names the worktree, the branch, the spec file, everything to read, the traps that unit will
hit, and what to report back. No follow-up prompting needed.

| Unit | Prompt to paste | Branch | Spec |
|---|---|---|---|
| 1a | `1a-shell-me-friends-settings.prompt.md` | `me-shell-friends` | `me-reorg` |
| 1b | `1b-coach-modes-lessons.prompt.md` | `coach-lessons` | `lessons` |
| 1c | `1c-today-coach-read.prompt.md` | `today-read` | `weekly-read` |
| 1d | `1d-chat-working-state.prompt.md` | `coach-chat` | `chat-state` |
| 3 | `3-dsa-problem-page.prompt.md` | `problem-page` | `problem-page` |
| 4 | `4-plan-setup.prompt.md` | `plan-setup` | `plan-setup` |

`SETUP.md` is shared and every prompt tells the agent to read it first: environment, testing
rules, the full gate list, forbidden files, PR format.

## Order

**Any of them can run in parallel** — no two units modify the same file. 1a has the widest
diff, so it is cheapest to review and merge last.

Units 2 (Library roadmap) and 5 (Coach mocks) are **already merged**, PRs #31 and #32. Their
code is the worked example these prompts point at.

## What the first two runs taught, now baked into SETUP.md

- **`E2E=1`** plus a local Supabase URL plus `VERCEL` unset, or `/api/test/sign-in` refuses and
  every test dies at `signIn`. Both of those cost real time.
- **`--retries=0`, three runs minimum.** CI retries failures, so a test that fails once and
  passes on the retry reports as a green tick. One such test survived three all-green CI runs.
- **Never reload a page to check an optimistic write.** The reload cancels the action's own
  request. Read it from a second page instead; `e2e/roadmap.spec.ts` has the pattern.
- **CI's seed is not production.** `roadmap_nodes` was empty because the pipeline fills it, and
  three tests failed on a view that worked. Adding seed rows is in scope.
- **Take screenshots from the running app**, not a fixture harness.
