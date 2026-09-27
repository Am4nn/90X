# Brief D — Playwright smoke tests in CI (spec §9)

**Read `.planning/briefs/README.md` first** (how we code, verify, open PRs, when to ask). This brief adds only what is specific to this task.

Branch: `e2e` (or whatever your session is pinned to). PR to `main`.

## Goal

A small, reliable browser suite that proves the core loops work end to end, running in CI against a throwaway local Supabase (like the existing `database` job in `.github/workflows/ci.yml`). Spec §9: "Playwright smoke tests: sign in, check in, answer a card, finish a day."

## The hard part: signing in without Google

Production sign-in is Google OAuth only. Build a **test-only sign-in** that can never be active in production:
- `web/src/app/api/test/sign-in/route.ts`: works only when `process.env.E2E === "1"` **and** `process.env.VERCEL` is unset **and** `NODE_ENV !== "production"` is not required (CI runs `next start`), so gate on `E2E === "1"` plus `!process.env.VERCEL` plus the Supabase URL being `http://127.0.0.1:54321` or `http://localhost:54321`. Otherwise return 404. Explain the gate in a comment.
- It creates (or reuses) a user in local Supabase Auth with email + password via the admin API (service role key from `supabase status -o env` in CI), marks them approved (+ optionally admin, via `user_approvals`), completes setup (profile fields + a campaign via existing `startCampaign` in `lib/tracker/campaign.ts`), then signs in with `@supabase/ssr` server client so auth cookies are set, and redirects to a `next` param.
- Add a test (Vitest) for the gate function (pure: env → allowed or not).

## Seed

`web/scripts/seed-e2e.ts`: inserts a small deterministic dataset into the local database: one source, a few DSA topics + topic links, ~10 problems in 2 patterns (statement + python solution), 1 system-design topic with a document, ~12 **live** cards across areas (typed with key points, one mcq with options, one output), plus one draft batch for the admin test. Idempotent.

## Tests (`web/e2e/*.spec.ts`, Playwright, Chromium only, one worker)

1. **Sign-in gate**: `/today` without a session redirects to `/sign-in`; the Google button is visible.
2. **Today**: after test sign-in, Today shows the day line, the grid and at least one mission.
3. **Check in**: open a problem from a mission → check in "Solved", 30m → back on Today that mission shows done.
4. **Answer a card**: `/feed` → type an answer that contains all key points of the seeded typed card → Check → result shows all key points hit → Next shows another card. (Exact match needs no AI; don't hit AI providers in CI. If the first card shown is not the seeded one, answer whatever is shown with its key points by reading them from the seed.)
   - If the Feed screen (brief C) hasn't merged when you start, write this test against the Feed's intended UI (see `.planning/briefs/part4-C-feed-screen.md`) and mark it `test.fixme` with a note; the lead enables it after merging.
5. **Finish a day**: complete every countable mission (check-ins for problems, "Mark studied" on the topic, answer 10 cards if a cards mission exists) → Today shows the day as done (the grid square has `data-s="done"`).
6. **Admin**: as an admin user, `/admin/cards` lists the seeded draft batch; a non-admin gets 404.
7. **Mobile**: run tests 2 and 4 also at 390×844.

Use roles/labels in selectors (`getByRole`, `getByLabel`), not CSS classes; add `aria-label`s to components only where needed.

## CI

New job `e2e` in `.github/workflows/ci.yml`:
- `supabase start` (same excludes as the `database` job, but keep `gotrue`/auth), export `supabase status -o env` values into the environment,
- `bun install`, `bunx playwright install --with-deps chromium`, run `seed-e2e.ts`, `bun run build` with `E2E=1` and local Supabase env, `bun run start` in the background, wait for port 3000, `bunx playwright test`,
- upload the Playwright report as an artifact on failure.
- Add `"test:e2e": "playwright test"` to `web/package.json`, `playwright.config.ts` in `web/` (baseURL `http://localhost:3000`, retries 1 in CI, trace on first retry).
- Keep Playwright out of the Vitest run (`vitest.config.ts` includes only `src/**/*.test.ts` already).

You probably can't run Supabase locally in your session. Iterate by pushing to your branch and reading the CI run (`gh run view --log-failed` if `gh` is available; otherwise ask the owner to paste the failing log).

## Definition of done
The `e2e` CI job passes on your PR (except a `fixme`'d Feed test if brief C isn't merged), all README checks pass, and the PR explains the auth gate so the lead can confirm it's impossible to reach in production.
