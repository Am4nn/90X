# Setup and verification — every Feed v2 part

Your prompt told you to read this. It is the same for all parts: how to get a working
environment, how to test, and what "done" means. Your own prompt and plan carry what is
different about your part.

## 1. Your worktree

You work in your own git worktree, on your own branch, cut from `main`. Never switch its
branch, never touch another worktree, never push to `main`, never force-push anything.

```bash
git fetch origin
git worktree add ../90X-wt-fv2/<part> -b <branch> origin/main
cd ../90X-wt-fv2/<part>/web   # pipeline parts: cd ../90X-wt-fv2/<part>/pipeline
bun install                   # web only
```

Your prompt names `<part>` and `<branch>`.

## 2. A working database, and the flag nobody guesses — web parts

Everything below is needed because **`/api/test/sign-in` refuses to answer unless all four of
these hold** (see `web/src/lib/auth/test-sign-in.ts`):

- `E2E=1`
- `ALLOW_TEST_SIGN_IN=1` — an explicit opt-in on top of the others, so a stray `E2E=1` alone
  cannot open the route
- `VERCEL` unset
- `NEXT_PUBLIC_SUPABASE_URL` is the local CLI stack — and it is **inlined at build time**, so a
  build made against the hosted project can never mint a session, however you run it

Miss any one and every Playwright test fails at `signIn` with a URL mismatch. That is the single
most expensive hour to lose in this repo.

**Start Docker Desktop**, then from the repo root:

```bash
bunx supabase start                 # local Postgres on 54322, API on 54321
docker run -d --name e2e-redis redis:7
docker run -d --name e2e-srh -p 8079:80 \
  -e SRH_MODE=env -e SRH_TOKEN=ci-redis-token \
  -e SRH_CONNECTION_STRING=redis://e2e-redis:6379 \
  --link e2e-redis hiett/serverless-redis-http:latest
```

Then write `web/.env.local` pointing at that stack. **Back up any existing one first** — it may
hold real keys, and you must never commit it or print its contents:

```bash
cd web
cp .env.local .env.local.backup 2>/dev/null || true
eval "$(cd .. && bunx supabase status -o env)"
cat > .env.local <<EOF
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres
DIRECT_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres
NEXT_PUBLIC_SUPABASE_URL=$API_URL
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=${PUBLISHABLE_KEY:-$ANON_KEY}
SUPABASE_SERVICE_ROLE_KEY=$SERVICE_ROLE_KEY
NEXT_PUBLIC_APP_URL=http://localhost:3000
UPSTASH_REDIS_REST_URL=http://localhost:8079
UPSTASH_REDIS_REST_TOKEN=ci-redis-token
AI_PROVIDER=openai-compatible
AI_API_KEY=ci-fake-model-key
AI_BASE_URL=http://localhost:8078/v1
AI_MODEL_FAST=fake-fast
AI_MODEL_SMART=fake-smart
E2E=1
ALLOW_TEST_SIGN_IN=1
EOF
bun run scripts/seed-e2e.ts
```

**Migration rule (Part A only):** write the migration file, then apply it to the **local** stack
with `bun run db:reset` (or `db:push` against `127.0.0.1:54322`). Never `db:push` against
`DIRECT_URL` from a real `.env.local` — that is production. After the migration, `bun run
db:pull` and `bun run db:types`.

To run the suite you also need the fake model and the app:

```bash
bun run e2e/fake-model.ts &                                  # 8078
bun run build
E2E=1 ALLOW_TEST_SIGN_IN=1 bun run start &                   # 3000
bunx playwright test e2e/<your-spec>.spec.ts --project=desktop --retries=0
```

**Port 3000 is shared.** If another agent is running its spec, `netstat -ano | grep
":3000.*LISTENING"` shows it. Wait and retry; never kill a process you did not start. Stop your
own app as soon as your spec finishes.

## 3. Pipeline parts — E, F, G, H

No Supabase, no Playwright. You work against the **local staging DuckDB**
(`pipeline/.data/staging.duckdb`) and never against production.

```bash
cd pipeline
uv sync --frozen
uv run pytest -q
```

Set `PIPELINE_MAX_USD` on **every** pipeline invocation (`LLM.__init__` reads it). Report
cumulative spend from `spend_usd(con)`. **Never run `pipeline publish`** — that is the
orchestrator's/human's step, and against the wrong `DATABASE_URL` it is production.

## 4. Testing — the part that has already gone wrong twice

**Always `--retries=0`, and run your spec at least three times.** CI retries failures, so a test
that fails once and passes on the retry shows up as a green tick. Both merged reorg units had
exactly that, and one stayed hidden through three all-green CI runs. **A test that passes on a
retry is a failing test.**

**Never reload the page to check that an optimistic write persisted.** The UI flips before the
server action returns, and `page.reload()` cancels the action's own request. Read the value from
a **second page in the same context** instead, inside `expect(async () => {...}).toPass()`.
`e2e/roadmap.spec.ts` has the worked example.

**If your spec needs data the seed does not have, add it.** Append to `web/e2e/seed-data.ts` and
insert at the end of `web/scripts/seed-e2e.ts` so a clash with another part stays trivial, and
**say so prominently in your PR**. Choose rows for *shape*, not volume.

**Test what a mistake would actually break.** A test that loads a page and asserts it loaded
passes just as well when the feature is broken.

## 5. Every gate, run by you — web parts

```bash
bunx oxfmt                 # first: it sorts imports and Tailwind classes
bun run typecheck
bun run lint
bun run test
bun run format:check
bun run check:tokens       # report the number; never edit the ceiling
bun run check:dead
bun run check:dupes
bun run check:cycles
bun run check:coverage
bun run check:deps
bun run check:actions      # needs GITHUB_TOKEN set, or GitHub rate-limits it
bun run check:archetypes   # the registry gate (Part A owns its inputs)
bun run build && bun run check:bundle
```

Plus the database checks your plan names, and your Playwright spec. **Screenshots at 390px and
1440px of every screen you changed**, taken from the running app, not a fixture harness.

## 6. Files no part may touch

- `web/scripts/check-*.ts` — **all of them**. The orchestrator owns them.
- `.github/workflows/ci.yml` — the shard matrix is already written. Your spec name is already
  registered, so your file must be named exactly what your prompt says.
- `supabase/migrations/` — **except Part A**, which owns its one migration.
- Generated, except where a part regenerates on purpose: `web/src/db/pulled/**`,
  `web/src/lib/supabase/database.types.ts`.
- `web/e2e/*.spec.ts` that your plan does not name.
- The other parts' files, as listed in your plan's **Do not touch**.

**If a ceiling fails, do not raise it.** Report the number you measured in the PR. The budgets
are shared bootstrap 300 KB and all client chunks 1000 KB.

## 7. UI craft — C parts (and B's base card)

Load the `impeccable` skill and follow its craft floor. This is an **Operate** surface. But the
repo's own rules win over any generic UI preference: six text sizes, token colours only, borders
not shadows, dark theme, mobile-first 390px, ≥44px tap targets, keyboard- and
screen-reader-reachable, motion via `tw-animate-css` honouring `prefers-reduced-motion`. A card
answered on a phone in a gap between other things is the product.

## 8. Decide, do not ask

You cannot ask the owner questions. Where your plan is ambiguous or contradicts the code, pick
the option closest to the plan and `DECISIONS.md`, keep going, and list it in the PR under
**Decisions** with what it would cost if wrong. Never widen scope.

## 9. Commits and the PR

Small commits, plain-English messages saying what changed and why. No emoji, no banners. End
every commit message with exactly:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```

Open one PR to `main`. Sections: **What** (one line per file or area), **Decisions** (with cost
if wrong), **Checks** (every command above with pass/fail, plus the measured token count and
bundle KB), **Seed changes** (if any), **Not verified**, **Screenshots**, **Suggestions**
(optional, never done in this PR).

## 10. Report back

The branch and PR number; every gate's result; the measured token count and bundle KB; how many
times you ran your spec and whether any attempt failed; every decision with its cost if wrong;
anything you could not verify; and any place the plan was wrong about the code. If a gate fails
and you cannot fix it inside your scope, **stop and report** rather than widening scope or
weakening the gate.
