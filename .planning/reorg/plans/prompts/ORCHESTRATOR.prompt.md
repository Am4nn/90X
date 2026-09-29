You are the orchestrator for the 90x reorg wave. Repo: `C:\Aman\Coding-Bamzii\Web Development\90X`, branch `main`.

Six units are ready to build. Each has a paste-ready prompt in
`.planning/reorg/plans/prompts/`. **Read `README.md` there first.**

## Your job

Dispatch one subagent per unit. Paste that unit's prompt file as the subagent's entire
message — nothing added, nothing summarised. Each works in its own git worktree on its own
branch, both named in its prompt.

**You do not write code.** You dispatch, track, and report.

## Run two or three at a time, not six

Playwright's `baseURL` is hardcoded to `localhost:3000` and all the agents share one local
Supabase stack, so only one can run its e2e suite at a time. Two or three in flight keeps
that queue short. Start with **1b, 3, 4** — they are the most independent. Then **1c, 1d**.
Run **1a last**: widest diff, cheapest to rebase onto the others.

## Accept a unit as done only when

- its PR is open against `main` and **every CI check passes**, and
- **no test passed on a retry** — open the `e2e feed` / `e2e coach` job log and grep for
  `retry #`. A retry-passing test is a failing test, and one survived three all-green CI runs
  on this project before anyone read the log.
- the agent reported: every gate's result, the measured token count and bundle KB, how many
  times it ran its spec, its decisions with costs, and anything unverified.

If a unit reports a gate failure it could not fix inside its scope, do not let it widen scope
or weaken the gate. Collect it and report.

## Do not merge

Merging, rebasing and any shared-file fix (`web/scripts/check-*.ts`, `.github/workflows/`,
`supabase/migrations/`, the generated schema) belong to the lead. Flag them.

## Report

A table: unit, branch, PR, CI state, retries seen, gate failures, decisions needing a human.
Then the one-line summary of what is left.
