# Brief — Coach mocks: searchable picker + behavioural empty state

**Branch:** `coach-mocks` (or your session's branch; say so in the PR).
**Read first:** `.planning/briefs/README.md`.

## Rule one: this is an add-on

The mocks are **visual references, not final designs**. Keep today's mocks page (past mocks,
scores, the two forms' behaviour). Change only what is below.

## 1. Design mock — a searchable picker

Today `DesignMockForm` (`web/src/components/coach/mock-picker.tsx`) picks a topic from a wall of
chips. Replace that **picker control only** with a **single text input with a searchable dropdown**
of existing topics:

- Type → filters the topics; a dropdown of matches shows while typing.
- Selecting a topic fills the input; the value still posts exactly what it does today.
- Keep the submit behaviour, validation and the server action unchanged.

## 2. Behavioural mock — explain the requirement

Today, with **no stories**, the behavioural form just does not make sense to a new user. Fix that:

- **No stories**: show a short explanation of **why** a behavioural mock needs a story ("behavioural
  questions ask for your own examples, so a mock has nothing to ask without at least one"), and a
  link to the Story bank. Disable/park the start action.
- **Has stories**: start works as today, and keep the **Story bank link visible** (so they can add
  or edit stories without leaving the flow).
- Do not change the story bank itself.

## Where

- `web/src/components/coach/mock-picker.tsx`, `web/src/app/(app)/coach/mocks/page.tsx`.
- No migrations; no changes to `lib/coach/mocks.ts` beyond a search helper if needed (add a test).

## Verification

From `web/`: `typecheck`, `lint`, `test`, `format:check`, `check:tokens`, `check:dead`, `build`.
Screenshots at 390px and 1440px, both states (no stories / has stories).
