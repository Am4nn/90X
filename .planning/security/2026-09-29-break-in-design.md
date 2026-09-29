# Security design: a break-in suite and defense-in-depth hardening for 90x

Status: design spec, pending owner review.
Date: 2026-09-29.

## Purpose

Make 90x hard to exploit, and — more importantly — keep it that way. The app already
has a strong authorization core (every server action calls `requireViewer()`, every
query is scoped to the viewer because the Drizzle connection bypasses RLS, admin pages
return `notFound()`). What it lacks is:

1. **An HTTP-layer break-in suite.** The existing `check:*` scripts prove the guards at
   the service and database layer, but nothing sends a real request to a running server
   and asserts what comes back. The sibling project `curfew` has this (`scripts/break-in/`).
2. **Any security response headers.** `next.config.ts` sets nothing — no clickjacking
   protection, no HSTS, no `nosniff`.
3. **Rate limits on the paid AI actions.** Solution review, grading and mock scoring call
   the model without a per-user ceiling, so one account can burn the shared monthly
   budget and degrade the coach for everyone.
4. **Defense-in-depth on the two surfaces that touch untrusted content:** the Markdown
   renderer, and the model prompt.

## Non-goals

- Not making the app literally "unhackable" — that is not a state a web app reaches.
  The goal is defense in depth plus a regression gate that fails CI when a hole opens.
- No new product features, no content, no SQL migrations (none of this work needs one).
- No manual browser "hack session" — the break-in script is the reproducible probe and
  runs in CI forever. (Owner chose this.)
- Full nonce-based Content-Security-Policy is a **follow-up**, not this pass: a wrong one
  blanks the page, and Next's App Router emits inline bootstrap scripts. We ship the
  `frame-ancestors` directive and the "boring" headers now, exactly as `curfew` does.

## Threat model

Actors: anonymous visitor, pending/rejected user, approved user, *friend* (may see some
rows), admin, QStash, and an attacker holding a session.

Trust boundaries:

- **Database.** Drizzle connects as a role RLS does not apply to, so the boundary is the
  query's `WHERE user_id = viewer.id`, not the database. The break-in suite must attack
  this: call the app's own service functions as the wrong identity and assert refusal.
- **HTTP.** A page must never render private data to a signed-out or non-owner visitor;
  a route must never answer a forged or missing signature.
- **Model prompt.** Display name and coach memory are user-controlled and reach another
  user's model context. They must be treated as data, never instructions.
- **Cost.** Paid model calls must be bounded per user, not only by the global budget.

## Deliverables

### 1. The break-in suite (`web/scripts/break-in/`)

Ported from `curfew/scripts/break-in/`, adapted to 90x's features and idioms.

- `harness.ts` — the scoreboard: `section`, `check`, `refuses`, `allows`, `skipped`,
  `summary`. Non-zero exit when anything "breaks". Copied nearly verbatim; it is the
  proven shape.
- `world.ts` — builds a throwaway world and tears it down. Four users (admin, friend,
  non-friend, pending), a friendship between admin/friend, a campaign + day + missions,
  live cards, a coach thread + memory, a check-in + note, a mock + transcript, a story,
  a push subscription, and one invite. Reuses the `check-rls.ts` fixture shape so the
  two suites agree on names and IDs. Teardown removes every row the run created and
  asserts nothing is left behind.
- `direct.ts` — attacks the server's own functions as the wrong identity. Rounds:
  1. cross-tenant reads of every private table (coach threads/messages/memory, notes,
     card answers/state, mock transcripts, stories, push subscriptions, missions,
     problem reviews);
  2. forged writes (post into another's thread, check-in as someone else, edit/delete
     another's memory, delete another's story);
  3. admin escalation (a non-admin deciding approvals, recording batch verdicts,
     running admin actions);
  4. replay/duplicate (answering a card twice, reviving a day twice);
  5. invites (self-invite, wrong-email accept, the per-address and per-sender caps);
  6. rate limits (coach chat, solution review, grading) — flood and assert refusal;
  7. the QStash signature guard and the test sign-in gate (unit-level, since they are
     build-time/env gates).
  `direct.ts` complements, and does not duplicate, `check-rls.ts` and
  `check-coach-tools.ts`; where a guard is already proven there, `direct.ts` references
  it instead of re-proving it.
- `http.ts` — the missing layer. Real requests to a running server:
  1. **Response headers** — assert `Content-Security-Policy: frame-ancestors 'none'`,
     `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`,
     `Referrer-Policy: strict-origin-when-cross-origin`, and a `Permissions-Policy`
     that denies geolocation/microphone. Read from a real response, not the config, so a
     `headers()` that never matches the route is caught.
  2. **Signed-out sweep** — every route must redirect (to `/sign-in`/`/pending`), never
     render a 200 with app content.
  3. **API routes** — job routes refuse a missing or wrong QStash signature; the test
     sign-in route refuses outside its gate; an unknown API route answers nothing.
  This half runs in the e2e CI job, where a real server is already started.
- `run.ts` — orchestrates: build world, run direct, run http (when a base is given),
  teardown, assert no leftovers, exit non-zero on any break.
- `admin-surfaces.ts` — a hand-maintained list of the admin-only operations (decide an
  approval, record/undo a batch verdict, resolve a flag). `direct.ts` iterates it and
  asserts each is refused to a non-admin, and a completeness check fails loudly when the
  list drifts from the actual admin actions — the same "second list" discipline as
  curfew's `capabilities.ts` and `check-deps.ts`'s own `ALLOWED` table.

### 2. Security headers (`web/next.config.ts`)

Add a `headers()` config that returns, for every route:

```
Content-Security-Policy: frame-ancestors 'none'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

90x uses the camera nowhere, so `Permissions-Policy` denies everything — simpler than
curfew's camera exception. HSTS is honoured over HTTPS only (fine locally). The exact
`headers()` API shape is verified against the Next 16 docs during implementation
(`web/AGENTS.md` warns the APIs differ).

### 3. Hardening — the holes the audit found

Each fix lands with a failing-then-passing test.

1. **Per-user rate limits on paid actions.** Introduce `@upstash/ratelimit` and wrap
   the two truly repeatable paid paths — solution review and mock scoring — with a
   per-user ceiling, and add a ceiling to grading (bounded today only by how many cards
   the feed serves). The coach chat limiter already exists and stays.
2. **`rehype-sanitize` on the Markdown renderer.** Add it to the shared `<Markdown>`
   component so AI-generated markdown is sanitized on top of react-markdown's default
   HTML escaping. Also prevent external `<img>` tracking pixels (keep the existing
   `urlTransform` behaviour, and do not allow `http` images).
3. **Prompt-injection hardening.** Treat user-controlled text as data where it crosses
   into the model: strip control characters and delimit the display name in the friend
   summary prompt; keep coach memory and message text clearly quoted. The
   propose → confirm → re-validate architecture already re-reads proposals from the
   saved assistant message, so the fix is containment, not a new mechanism.
4. **Harden the test sign-in route.** It ships in every build and can mint admin
   sessions. Add a build-time assertion that the route cannot answer in production
   (defense-in-depth on top of the existing `E2E`/`VERCEL`/local-URL triple gate), and
   document it in `SECURITY.md`.
5. **Make the coach rate-limiter's fail-open behaviour a decision.** The lesson limiter
   fails closed, the coach limiter fails open. Keep both as-is but record the rationale
   and assert the intended behaviour in tests so a future change is deliberate, not
   accidental.

### 4. Security libraries and static tooling

- `@upstash/ratelimit` — correct sliding-window/token-bucket rate limits (replaces the
  hand-rolled window for the new surfaces).
- `rehype-sanitize` — Markdown sanitization.
- `eslint-plugin-security` — static rules in the lint step (command injection, unsafe
  regex, prototype pollution, etc.).
- `gitleaks` (via `gitleaks/gitleaks-action`) — secret scanning as its own CI job.
- `@secretlint/secretlint` — a fast local/dev secret lint, run in the lint step.

Considered and rejected: `next-safe-action` (every action already does `requireViewer()` +
zod; adopting it is a large refactor with little new protection).

### 5. CI wiring (`.github/workflows/ci.yml`)

- A `break-in` job (direct round) beside the `database` job, against the same local
  Supabase stack, so the world is built and torn down on a throwaway database.
- The HTTP sweep runs inside the existing `e2e-shard` job after the app starts, pointed
  at `http://localhost:3000`.
- A `gitleaks` job scans every push/PR.
- The response-header assertions live in the HTTP sweep itself, so they cannot drift
  from what is actually served.

Note: `.github/workflows/` is normally reserved for the lead during the reorg wave. This
security pass is a separate effort requested by the owner and is the only branch editing
`ci.yml`; the change is additive and conflicts with nothing the wave touches.

### 6. Findings report + `SECURITY.md`

- `.planning/security/2026-09-29-audit.md` — the full audit findings table (severity,
  file:line, what an attacker/user would see, fixed?).
- `SECURITY.md` at the repo root — the threat model, the trust boundaries, how to run
  the break-in suite, and the fail-open/fail-closed decisions, so a future contributor
  reads the reasoning instead of re-deriving it.

## Testing strategy

- TDD for every fix: write the Vitest/break-in assertion, see it fail, implement, see it
  pass.
- The break-in suite is a CI command (`bun run break-in`), not a checklist; a break is a
  red merge.
- Database-dependent rounds reuse the rolled-back-transaction pattern of
  `check-rls.ts` / `check-coach-tools.ts`, so the suite leaves no rows behind.
- The HTTP sweep asserts a positive control (a route the identity *should* reach) so a
  green sweep cannot be a sweep that silently looked at nothing.

## Risks and out of scope

- **Nonce CSP** — deferred; documented in `SECURITY.md` as the next step.
- **LeetCode sync / web push** — outside the attack surface that reaches user data via
  the app's own routes; left as-is beyond the existing guards.
- **Pipeline (Python)** — runs locally, not exposed to the web; the break-in suite does
  not cover it, but `gitleaks` and `eslint-plugin-security` do scan its secrets/scripts
  where applicable.

## Definition of done

- `bun run break-in` exists, runs against a throwaway database, and its HTTP sweep runs
  in CI against a real server.
- Every route serves the security headers, asserted by the sweep.
- The three unbounded paid actions are rate-limited per user, with tests.
- Markdown is sanitized; the display name is contained in the model prompt.
- `gitleaks` and the security lint run in CI.
- The audit report and `SECURITY.md` are committed.
- All existing checks (typecheck, lint, test, format, tokens, dead, dupes, cycles,
  coverage, deps, actions, build, bundle) still pass, and the break-in suite is green.
