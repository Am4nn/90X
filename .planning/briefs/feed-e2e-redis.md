# Brief H — Enable the Feed browser test in CI (Redis stand-in)

**Read `.planning/briefs/README.md` first.** This brief adds only what is specific to this task.

Branch: your pinned branch. PR to `main`.

## Why
The Playwright suite (`web/e2e/`, CI job `e2e` in `.github/workflows/ci.yml`) has a Feed test marked `test.fixme` (`web/e2e/feed.spec.ts`), because the Feed keeps its queue in Upstash Redis (`web/src/lib/upstash/redis.ts`, REST API), which the CI job doesn't have. Everything else in the suite already passes.

## Build
1. In the `e2e` job, run a local Upstash-compatible REST server in front of a Redis container — e.g. the `hiett/serverless-redis-http` image (`SRH_MODE=env`, `SRH_TOKEN=<any>`, `SRH_CONNECTION_STRING=redis://redis:6379`) plus a `redis:7` service — and set `UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_TOKEN` for the build and `bun run start` steps to it. QStash and Vector stay unset (nothing in the suite needs them; code paths that need them must not run).
2. Remove `test.fixme` from `web/e2e/feed.spec.ts` and make it pass: sign in with the test route, skip the diagnostic if offered (or run it — your choice, document it), answer the seeded typed card with all its key points (exact match, no AI), expect every key point marked hit, then **Next** shows a different card. Also cover: **Skip** shows the answer; **Show options** on the seeded mcq and picking the right option marks it correct; reloading mid-card shows the same card.
3. Add one more test for Today's "10 cards" mission if the e2e user's template can include a cards slot without breaking `finish-day.spec.ts` — otherwise skip it and say why in the PR.
4. Don't hit any AI provider in CI (only exact-match / option / output answers).

## Verification
The `e2e` CI job passes on your PR with the Feed test enabled; all README checks pass. You may not be able to run Docker services locally — iterate by pushing and reading the CI run (`gh run view --log-failed`, or the uploaded Playwright report artifact).
