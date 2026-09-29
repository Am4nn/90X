# Security Hardening + Break-in Suite — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port curfew's break-in suite to 90x, add the missing security headers, and close the real holes the audit found (unbounded AI spend, Markdown sanitization, prompt injection, test-sign-in hardening) — all gated by CI.

**Architecture:** A `web/scripts/break-in/` suite mirrors curfew's: `world.ts` builds a throwaway fixture, `direct.ts` attacks the app's own service functions as the wrong identity, `http.ts` sweeps a running server (headers, signed-out routes, API auth). Defense-in-depth fixes land beside it, each with a failing-then-passing test.

**Tech Stack:** Next.js 16 (App Router, React 19, `proxy.ts` not middleware), TypeScript strict, Drizzle + Supabase, Bun, `@upstash/ratelimit`, `rehype-sanitize`, `eslint-plugin-security`, `gitleaks`, `@secretlint/secretlint`.

**Spec:** `.planning/security/2026-09-29-break-in-design.md`

## Global Constraints

- Next.js 16 APIs differ from older versions: read the matching guide in `web/node_modules/next/dist/docs/` before writing framework code (headers config, proxy, route handlers).
- Server code bypasses RLS: every query is scoped to `viewer.id` (`requireViewer()` in `@/lib/auth/viewer`) or admin-gated behind `viewer.isAdmin`.
- No SQL migrations. No secrets. No `.env*`. No edits to generated `web/src/db/pulled/**` or `web/src/lib/supabase/database.types.ts`.
- Comments: short, why not what. No `any`, no non-null `!` unless the invariant is local.
- Design tokens only (six text sizes, token colours). Server actions return `FormState` and never throw to the UI.
- Break-in scripts use the rolled-back-transaction pattern of `check-rls.ts` / `check-coach-tools.ts` and leave no rows behind.
- `check:tokens` / `check:bundle` / `check:coverage` ceilings may only fall, never rise.
- Every commit message ends with `Co-Authored-By: Claude <noreply@anthropic.com>`.

## Review Focus

1. **A route that forgot `requireViewer()` renders a 200 to a stranger** — the signed-out sweep must fail it. Pinned by `http.ts` "nothing was served to nobody".
2. **A header declared but not served** — the header check reads a real response, not the config. Pinned by `http.ts` `responseHeaders`.
3. **A new admin surface not in the second list** — `admin-surfaces.ts` completeness check fails loudly. Pinned by `direct.ts` round "admin escalation".
4. **A rate limiter that fails open under a Redis outage** — the fail-closed decision is asserted by the limiter unit test (a rejecting `redis.get` returns `{ allowed: false }`).
5. **A display name carrying control characters into another user's prompt** — `sanitizeForPrompt` strips C0/C1 controls; pinned by its Vitest test.

---

### Task 1: Security response headers

**Files:**
- Modify: `web/next.config.ts`
- Modify: `web/scripts/break-in/http.ts` (the header assertion — added in Task 4, but the header values are pinned here)

**Interfaces:**
- Produces: every response carries the six headers below. `http.ts` asserts the exact strings.

- [ ] **Step 1: Read the Next 16 headers guide**

Read `web/node_modules/next/dist/docs/` for the `headers` config shape (curfew uses `headers: () => Promise.resolve([{ source, headers }])`; verify Next 16 still takes this form and note any deprecation).

- [ ] **Step 2: Add the headers to `web/next.config.ts`**

Add a `headers()` export returning one entry for `source: "/:path*"` with:
```
Content-Security-Policy: frame-ancestors 'none'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Strict-Transport-Security: max-age=31536000; includeSubDomains
```
(90x uses no camera, so `Permissions-Policy` denies everything — simpler than curfew's camera exception.)

- [ ] **Step 3: Verify the build still works**

Run: `cd web && DATABASE_URL=postgresql://ci:ci@localhost:5432/ci DIRECT_URL=postgresql://ci:ci@localhost:5432/ci NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321 NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=ci NEXT_PUBLIC_APP_URL=http://localhost:3000 bun run build`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add web/next.config.ts
git commit -m "Security headers on every response"
```

### Task 2: Break-in harness and world

**Files:**
- Create: `web/scripts/break-in/harness.ts`
- Create: `web/scripts/break-in/world.ts`
- Create: `web/scripts/break-in/run.ts`
- Modify: `web/package.json` (add `"break-in": "bun run scripts/break-in/run.ts"`)

**Interfaces:**
- Produces `harness.ts`: `section(name: string)`, `check(name: string, ok: boolean, detail?: string)`, `refuses(name: string, attempt: () => Promise<unknown>)`, `allows(name: string, attempt: () => Promise<unknown>)`, `skipped(name: string, why: string)`, `summary(): number` — copied from curfew, `held`/`BROKE` wording kept.
- Produces `world.ts`: `interface World { tag; admin; friend; stranger; pending; invite; today; ... }` and `build(): Promise<World>`, `teardown(w: World): Promise<void>`, `leftovers(w: World): Promise<number>`.
- Produces `run.ts`: `--http=<origin>` runs the http sweep in addition to direct; `--http-only` runs only the http sweep.

- [ ] **Step 1: Port `harness.ts`**

Copy curfew's `scripts/break-in/harness.ts` verbatim (its `refuses`/`allows` shape is the proven guard against inverted try/catch). Adjust import paths only.

- [ ] **Step 2: Write `world.ts`**

Build the fixture using `@/db` (Drizzle) over one rolled-back transaction, mirroring `check-rls.ts` IDs (`...00a` admin, `...00b` friend, `...00c` non-friend, `...00d` pending): insert `auth.users`, approve three, friendship admin↔friend, a live `cards` row, a `coach_threads` + `coach_messages` + `coach_memory` + `stories` + `mocks` + `mock_details` for the admin, a `checkins` + `checkin_notes`, a `campaigns` + `days` + `missions` + `problem_reviews` + `readiness_snapshots` + `push_subscriptions`, and one `friend_invites` row. `teardown` deletes every row keyed to the run's own tag/ids; `leftovers` returns the count still present.

- [ ] **Step 3: Write `run.ts`**

Parse `--http=<origin>` and `--http-only`; call `build()`, then `direct(world)` (Task 3) and, when a base is present, `http(world, base)` (Task 4); `teardown`; `check("the round cleans up after itself", (await leftovers(world)) === 0)`; `process.exit(summary() === 0 ? 0 : 1)`. Guard the direct/http imports so `run.ts` compiles before Tasks 3–4 exist (stub imports to no-op functions that are replaced in later tasks).

- [ ] **Step 4: Wire the npm script**

Add `"break-in": "bun run scripts/break-in/run.ts"` to `web/package.json`.

- [ ] **Step 5: Typecheck**

Run: `cd web && bun run typecheck`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add web/scripts/break-in/harness.ts web/scripts/break-in/world.ts web/scripts/break-in/run.ts web/package.json
git commit -m "Break-in harness: world, scoreboard and runner"
```

### Task 3: `direct.ts` — attack the service layer

**Files:**
- Create: `web/scripts/break-in/direct.ts`
- Create: `web/scripts/break-in/admin-surfaces.ts`

**Interfaces:**
- Consumes: `World` from `world.ts`; `harness` from Task 2; the service functions under `@/lib/**` already exercised by `check-rls.ts` and `check-coach-tools.ts`.
- Produces `direct.ts`: `run(w: World): Promise<void>`.
- Produces `admin-surfaces.ts`: `ADMIN_SURFACES_FOR_TEST: { name: string; attempt: (nonAdminId: string) => Promise<unknown> }[]` — the hand-maintained second list.

- [ ] **Step 1: Write the failing completeness check**

In `direct.ts`, assert `ADMIN_SURFACES_FOR_TEST.length === 4` (decide approval, record verdict, undo verdict, resolve flag — the four admin-only actions in `admin/users/actions.ts` and `admin/cards/actions.ts`). Run: `bun run break-in` → FAIL with a length mismatch, proving the second list is independent of the code.

- [ ] **Step 2: Write the attack rounds**

Implement `run(w)` with these rounds, using `refuses`/`allows`/`check`:
1. **cross-tenant reads** — for each private table (`coach_threads`, `coach_messages`, `coach_memory`, `stories`, `mock_details`, `checkin_notes`, `card_reviews`, `card_state`, `missions`, `problem_reviews`, `push_subscriptions`), `friend` (and `non-friend`) selects `where user_id = admin` and gets 0 rows; `mocks` (score) is the one row a friend *does* see.
2. **forged writes** — `friend` cannot insert into the admin's `coach_messages`, cannot write a `checkins` row for the admin, cannot `editFact`/`deleteFact` the admin's memory, cannot delete the admin's story.
3. **admin escalation** — a non-admin is refused every entry in `ADMIN_SURFACES_FOR_TEST`; an admin is allowed each (positive control).
4. **replay/duplicate** — submitting the same card answer twice records one `card_reviews` row (idempotency key, mirroring `check-tracker.ts`'s style).
5. **invites** — self-invite refused, wrong-email accept refused, per-address and per-sender caps refused (reuse `check-friends.ts`'s `INVITE_CAP`/`INVITES_PER_ADDRESS`).
6. **rate limits** — skip with `skipped(...)` when `UPSTASH_REDIS_REST_URL` is unset (mirror curfew's section 22); otherwise flood `takeMessageSlot`/the new limiters (Task 5) and assert a refusal.

- [ ] **Step 3: Run it against a throwaway DB**

Run: `cd web && bun run db:start && bun run break-in` (database required; note "needs local Supabase" in the PR if this environment cannot run it).
Expected: PASS, "All break-in checks passed".

- [ ] **Step 4: Commit**

```bash
git add web/scripts/break-in/direct.ts web/scripts/break-in/admin-surfaces.ts
git commit -m "Break-in direct round: cross-tenant, forgery, escalation, caps"
```

### Task 4: `http.ts` — the HTTP sweep

**Files:**
- Create: `web/scripts/break-in/http.ts`

**Interfaces:**
- Consumes: `World`; `harness`. Runs against `base` (e.g. `http://localhost:3000`).
- Produces: `run(w: World, base: string): Promise<void>`.

- [ ] **Step 1: Write the header assertions**

`responseHeaders(base)` fetches `base` and asserts each header equals the exact value pinned in Task 1 (the six headers). A `headers()` that never matches the route fails here.

- [ ] **Step 2: Write the signed-out sweep**

`routes(w)` lists every app route (`/`, `/today`, `/feed`, `/library`, `/coach`, `/me`, `/me/friends`, `/admin`, `/admin/users`, `/admin/cards`, and one private detail route). For each, GET with no cookie and assert it never returns a 200 that renders app content (a redirect to `/sign-in`/`/pending`/`/setup` is correct; a 200 with the app shell is a break).

- [ ] **Step 3: Write the API route assertions**

For each QStash job (`/api/jobs/hourly`, `/api/jobs/leetcode-sync`) assert a GET/POST with no `upstash-signature` returns 401, and a wrong signature returns 401. Assert `/api/coach/chat` POST with no session returns 401. Assert an unknown route `/api/nope` returns non-200.

- [ ] **Step 4: Wire it into `run.ts`**

Replace the stub `http` import with the real `run(w, base)`; `run.ts` calls it when `--http=<origin>` or `--http-only` is given, and prints a `skip` line otherwise.

- [ ] **Step 5: Run the sweep against a local server**

Run: `cd web && bun run break-in --http=http://localhost:3000` against a running build.
Expected: headers held, nothing served to nobody, job routes refuse.

- [ ] **Step 6: Commit**

```bash
git add web/scripts/break-in/http.ts web/scripts/break-in/run.ts
git commit -m "Break-in HTTP sweep: headers, signed-out routes, API auth"
```

### Task 5: Per-user rate limits on the paid actions

**Files:**
- Modify: `web/package.json` (add `@upstash/ratelimit`)
- Create: `web/src/lib/upstash/ratelimit.ts`
- Modify: `web/src/app/actions/review.ts` (gate `createSolutionReview`)
- Modify: `web/src/lib/coach/mocks.ts` (gate scoring in `endMock`)
- Modify: `web/src/lib/feed/grader.ts` (gate `gradeWithAi`)
- Test: `web/src/lib/upstash/ratelimit.test.ts`

**Interfaces:**
- Produces `web/src/lib/upstash/ratelimit.ts`: `takeSlot(userId: string, kind: "review" | "mock" | "grade", now?: number): Promise<{ allowed: boolean; retryAfterSec: number }>`. Fail-closed: a rejecting Redis returns `{ allowed: false, retryAfterSec: 0 }` (decision: paid actions refuse under an outage, unlike coach chat which fails open).
- Ceilings (decisions, tune-able): review 10/hour, mock 20/hour, grade 120/hour, sliding window.

- [ ] **Step 1: Write the failing test**

In `ratelimit.test.ts`: (a) `takeSlot` returns `allowed` within the ceiling; (b) it returns `!allowed` past the ceiling; (c) when the Redis client rejects, it returns `{ allowed: false }` (fail closed). Run: `bun run test` → FAIL (module missing).

- [ ] **Step 2: Install and implement**

Add `@upstash/ratelimit`; implement `takeSlot` using a sliding-window limiter over the existing `@/lib/upstash/redis` client, keyed by `key("rl", kind, userId)`. Verify the installed `@upstash/ratelimit` constructor shape from its types before writing.

- [ ] **Step 3: Gate the three call sites**

In `review.ts` call `takeSlot(viewer.id, "review")` before `createSolutionReview` and return a 429-style `FormState` error when refused. In `endMock` call `takeSlot(userId, "mock")` before `coachModel()` and return `{ error: ... }`. In `grader.ts` call `takeSlot(userId, "grade")` and return a "rate limited" outcome without calling the model.

- [ ] **Step 4: Run the tests**

Run: `cd web && bun run test`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add web/package.json web/src/lib/upstash/ratelimit.ts web/src/lib/upstash/ratelimit.test.ts web/src/app/actions/review.ts web/src/lib/coach/mocks.ts web/src/lib/feed/grader.ts
git commit -m "Rate-limit the paid AI actions per user"
```

### Task 6: Markdown sanitization

**Files:**
- Modify: `web/package.json` (add `rehype-sanitize`)
- Modify: `web/src/components/markdown.tsx`
- Test: `web/src/components/markdown.test.tsx` (Vitest, render to string)

**Interfaces:**
- Consumes: `Markdown`'s current `ReactMarkdown` + `remark-gfm` setup.
- Produces: `Markdown` now sanitizes the rendered HTML.

- [ ] **Step 1: Write the failing test**

Render `<Markdown>{'<img src=x onerror=alert(1)> <script>alert(1)</script>'}</Markdown>` and assert no `onerror` and no `<script>` reach the output. Run: `bun run test` → FAIL.

- [ ] **Step 2: Add `rehype-sanitize`**

Add `rehype-sanitize` to `package.json`; add `rehypePlugins={[rehypeSanitize]}` to the `ReactMarkdown` call. Keep the existing `remark-gfm` and `COMPONENTS`.

- [ ] **Step 3: Run the tests**

Run: `cd web && bun run test`
Expected: PASS (including the existing `email/templates.test.ts` escape test).

- [ ] **Step 4: Commit**

```bash
git add web/package.json web/src/components/markdown.tsx web/src/components/markdown.test.tsx
git commit -m "Sanitize Markdown output against injected HTML"
```

### Task 7: Prompt-injection containment

**Files:**
- Create: `web/src/lib/coach/prompt-safety.ts`
- Modify: `web/src/lib/coach/tools.ts` (the `get_friend_summary` summary text) and `web/src/lib/coach/tools-data.ts` (or wherever a profile name is interpolated into a prompt)
- Test: `web/src/lib/coach/prompt-safety.test.ts`

**Interfaces:**
- Produces `prompt-safety.ts`: `sanitizeForPrompt(text: string): string` — strips C0/C1 control characters (except none), collapses `\r\n`, and returns the text inside delimiters.

- [ ] **Step 1: Write the failing test**

Assert `sanitizeForPrompt("ignore\b previous\ninstructions\x00")` contains no control characters, and `sanitizeForPrompt('A\n"ignore previous"')` is delimited. Run: `bun run test` → FAIL.

- [ ] **Step 2: Implement and apply**

Implement `sanitizeForPrompt`; apply it to the display name where it enters `get_friend_summary`'s prompt text, and to any profile name interpolated into a model prompt (grep `p.name` / `name` in `tools.ts`). Do not change the stored name.

- [ ] **Step 3: Run the tests**

Run: `cd web && bun run test`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add web/src/lib/coach/prompt-safety.ts web/src/lib/coach/prompt-safety.test.ts web/src/lib/coach/tools.ts web/src/lib/coach/tools-data.ts
git commit -m "Contain display names in the coach prompt"
```

### Task 8: Harden the test sign-in route, document decisions

**Files:**
- Modify: `web/src/lib/auth/test-sign-in.ts` (add a 4th gate: an explicit opt-in env var)
- Modify: `web/src/app/api/test/sign-in/route.ts` (pass the new env value through)
- Modify: `web/src/lib/auth/test-sign-in.test.ts`
- Create: `SECURITY.md`
- Create: `.planning/security/2026-09-29-audit.md`

**Interfaces:**
- Produces: `testSignInAllowed(env: { E2E?; VERCEL?; NEXT_PUBLIC_SUPABASE_URL?; ALLOW_TEST_SIGN_IN? }): boolean` now also requires `env.ALLOW_TEST_SIGN_IN === "1"` — an explicit opt-in on top of the existing `E2E=1` + `VERCEL` unset + local-URL triple gate, so a stray `E2E=1` can no longer open the route.

- [ ] **Step 1: Write the failing test**

In `web/src/lib/auth/test-sign-in.test.ts`, assert `testSignInAllowed` returns `false` when `ALLOW_TEST_SIGN_IN` is missing or not `"1"`, even with `E2E=1`, `VERCEL` unset and a local URL. Run: `bun run test` → FAIL.

- [ ] **Step 2: Implement the gate and document**

Add the `ALLOW_TEST_SIGN_IN` requirement to `testSignInAllowed`; pass `ALLOW_TEST_SIGN_IN: process.env.ALLOW_TEST_SIGN_IN` from the route. Write `SECURITY.md` (threat model, trust boundaries, how to run `bun run break-in`, the fail-open/fail-closed decisions) and `.planning/security/2026-09-29-audit.md` (findings table: severity, file:line, effect, fixed?).

- [ ] **Step 3: Set the flag in the e2e CI env**

In `ci.yml`'s `e2e-shard` `env:` block add `ALLOW_TEST_SIGN_IN: "1"` (the only place the route is ever meant to answer). This is folded into Task 10's commit.

- [ ] **Step 4: Run the tests**

Run: `cd web && bun run test`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add web/src/lib/auth/test-sign-in.ts web/src/app/api/test/sign-in/route.ts web/src/lib/auth/test-sign-in.test.ts SECURITY.md .planning/security/2026-09-29-audit.md
git commit -m "Harden test sign-in and document the security decisions"
```

### Task 9: Static security tooling

**Files:**
- Modify: `web/package.json` (add `eslint-plugin-security`, `@secretlint/secretlint` + a preset, and the scripts)
- Modify: `web/eslint.config.mjs` (enable `plugin:security/recommended`)
- Create: `web/.secretlintrc.json`
- Create: `.gitleaks.toml` (allow-list any known false positives)

**Interfaces:**
- Produces: `bun run lint` now includes the security rules; `bun run check:secrets` runs secretlint; CI runs gitleaks.

- [ ] **Step 1: Enable the security lint**

Add `eslint-plugin-security` and its recommended config to `eslint.config.mjs`. Run: `bun run lint` → fix any findings it flags (or document an allow with a comment). Expected: PASS with zero warnings.

- [ ] **Step 2: Add secretlint**

Add `@secretlint/secretlint` + preset, `web/.secretlintrc.json`, and a `check:secrets` script. Run it once; commit the config and any allow-list.

- [ ] **Step 3: Add gitleaks config**

Add `.gitleaks.toml` (base config plus allow-list for the deliberate `ci-*` and `e2e-local-only-password` fixtures that are documented as non-secrets).

- [ ] **Step 4: Commit**

```bash
git add web/package.json web/eslint.config.mjs web/.secretlintrc.json .gitleaks.toml
git commit -m "Security lint and secret scanning"
```

### Task 10: Wire everything into CI

**Files:**
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: the `break-in` npm script (Task 2) and the gitleaks config (Task 9).

- [ ] **Step 1: Add the direct round to the `database` job**

After `check-coach-tools`, add a step: `working-directory: web`, `run: bun run break-in` (no `--http`, so the sweep skips and says so).

- [ ] **Step 2: Add the HTTP sweep to the `e2e-shard` job**

After the app start step, add: `run: bun run break-in --http-only --http=http://localhost:3000` (the server and throwaway Supabase are already up).

- [ ] **Step 3: Add a `gitleaks` job**

A `gitleaks` job using `gitleaks/gitleaks-action@v2` with `GITHUB_TOKEN`, scanning every push/PR.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "Run the break-in suite and secret scan in CI"
```

### Task 11: Full verification and PR

**Files:** none (verification only)

- [ ] **Step 1: Run every local check**

From `web/`: `bunx oxfmt`, `bun run typecheck`, `bun run lint`, `bun run test`, `bun run format:check`, `bun run check:tokens`, `bun run check:dead`, `bun run check:dupes`, `bun run check:cycles`, `bun run check:coverage`, `bun run check:deps`, `bun run check:actions`, `bun run build && bun run check:bundle`. Report the measured token count and bundle KB; do not raise any ceiling.

- [ ] **Step 2: Run the database checks**

`bun run db:start`, then `bun run check:rls`, `bun run check:tracker`, `bun run check:feed`, `bun run check:friends`, `bun run check:coach-tools`, and `bun run break-in`. Note in the PR anything that could not run here (the lead runs it).

- [ ] **Step 3: Push and open the PR**

```bash
git push -u origin security/break-in
```
Open a PR to `main` with sections **What** (one line per area), **Decisions** (rate-limit ceilings, fail-closed, header set, scope of `ci.yml` change), **Checks** (each command above, pass/fail + measured numbers), **Not verified**, **Suggestions**.

- [ ] **Step 4: Confirm CI is green**

Watch the PR checks: `web`, `database` (with the new break-in step), `e2e feed`, `e2e coach` (with the HTTP sweep), `deps`, `gitleaks`.
