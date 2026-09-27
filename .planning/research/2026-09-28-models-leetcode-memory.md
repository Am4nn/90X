# Models, LeetCode API, AI memory: what to adopt

Research done 2026-09-27 for three questions: are Laya or Jev better for our AI jobs, does
leetcode-stats-api give us anything, and should `coach_memory` move to Letta, Mem0 or Zep.
One subagent per area; I checked the load-bearing code claims myself (file:line below).

## Verdicts

| Area | Verdict | Cost if the verdict is wrong |
|---|---|---|
| Laya, all jobs | **Skip**. Close the SPEC §3 experiment row | Under $1: the triage it targets already ran and a re-run costs ~$0.90 |
| Jev, grading | **Skip** (was "spike further" until Flash was measured: ~$0.70/month and 0 grade changes over 3 repeats) | Skipping a good Jev: at most ~$0.60/month |
| Jev, coach / triage / cards | **Skip**. It can't chat, generate text or call tools | None |
| leetcode-stats-api | **Skip**. Keep SPEC §6.6 "No third-party proxy" | If LeetCode blocks Vercel's IPs: sync shows "unavailable", manual check-ins keep working; a self-hosted relay is ~half a day |
| Mem0 | **Skip** | Low: we can add pgvector retrieval ourselves if a user passes ~150 facts |
| Zep / Graphiti | **Skip** | Low to medium: no time-scoped memory queries ("what did I struggle with in August") |
| Letta | **Skip** | Very low |

Seven verdicts, zero adopts, zero spikes. What this research found worth doing is in our own code:
`coach_memory` kept contradicted facts, and its aging clock was wrong. A suspected cost-meter gap
for DeepSeek thinking tokens turned out not to exist once measured (see "Measured later").
See "What to do instead" at the end.

## Measured later (2026-09-27, after keys were added)

Run from this environment against the real DeepSeek API once the owner added the env vars.

| What | Result |
|---|---|
| Grading benchmark (`check-grading.ts`, 7 answers over 3 questions, not 12) | 7/7 within one key point; **0 grade changes across 3 repeats**; 0 errors |
| Grading latency, Flash, `NO_THINKING` | p50 1.01 s, p90 1.21 s |
| Grading tokens, Flash | avg 269 in, 10 out, 0 hidden → $0.000093/grade → **~$0.70/month** at 7,500 grades |
| Same with thinking on | 7/7, avg 117 out (≈11×), p50 1.23 s → ~$1.72/month; `NO_THINKING` is worth keeping |
| Pro, thinking on, raw usage | `prompt 95, completion 168, reasoning 78, total 263`: **thinking is inside `completion_tokens`**, so `total − in − out = 0` |
| `check:coach` with the real model (local DB copy) | all pass, twice, including correction, expiry, dismissed and aging checks |
| LeetCode adapter, live | real user: 32 submissions with Accepted / Wrong Answer / TLE; unknown user: see Area 2 note |

What this changes:
- **The cost meter was not undercounting.** DeepSeek now reports thinking inside
  `completion_tokens`, so the handoff's 5× gap no longer happens on either model. `billedTokens`
  stays as a zero-cost guard (it adds only what `total_tokens` bills beyond prompt + completion,
  which is 0 today), matching what the pipeline does.
- **Jev's ceiling is even lower.** Flash grading is ~$0.70/month and already fully consistent on
  our set, so Jev could save at most ~$0.60/month and can't improve consistency on these cases.
  Verdict moves from "spike further" to **skip** unless grading volume grows 10×.
  (`AI_GATEWAY_API_KEY` is still unset, so Jev itself was not run.)
- **Supabase Postgres is still unreachable from here**: the pooler on port 6543 times out
  (the network allows HTTPS, not raw Postgres), so `check:rls`, `check:tracker`, `check:feed`
  and `check:coach-tools` ran against a local Postgres 16 with every migration applied, not
  against production.

## What could not be measured at first, and why

At first nothing ran against a live model. This container has **no AI keys** (`DEEPSEEK_API_KEY` /
`AI_API_KEY`, `AI_GATEWAY_API_KEY`, `TYPESAFE_AI_API_KEY` are all unset) and its network policy
blocks the hosts: **api.deepseek.com, ai-gateway.vercel.sh, api.typesafe.ai, leetcode.com,
leetcode-stats-api.herokuapp.com** (proxy `connect_rejected`). Web reading was also blocked for
**medium.com, www.jevai.org, typesafe.ai, vercel.com, arxiv.org, huggingface.co, mem0.ai,
www.getzep.com, docs.letta.com**, so facts from those come from search-result summaries and are
marked that way. GitHub repos were cloned and read directly; npm packages were read from source.

The benchmark is ready to run where the keys are: see "Running the grading benchmark" below.

---

## Area 1: Laya and Jev

### What they are

**Laya** ([repo](https://github.com/NandhaKishorM/laya), read at `4066d5d`) is an Apache-2.0
Python library plus three small **encoder** checkpoints (ModernBERT-large 421M with a 512-token
context, mmBERT-base 322M). It answers typed questions (choice, score, yes/no probability) in one
forward pass and cannot generate text. It is an open, self-hostable clone of Jev's API
(`POST /v1/systemone`). Its own README is honest that the stock models are near chance
zero-shot: 0.362 on its typed-decisions benchmark against a 0.318 random and 0.461 majority
baseline, "a fast base to specialise, not a zero-shot decision engine". It needs torch on a
server; the 33 ms figure is on a T4 GPU, 193–464 ms on CPU.

**Jev** is TypeSafe AI's hosted "System One" model, on Vercel AI Gateway as `typesafe-ai/jev`
since 2026-09-16. You send a `state` and typed questions; it returns probabilities. No prose, no
chat, no tool calls. In the AI SDK it is `experimental_evaluate` with
`gateway.evaluationModel('typesafe-ai/jev')` (read from `ai@7.0.116` and
`@ai-sdk/gateway@4.0.96` source; our repo already pins `ai ^7.0.116`). It is **not** reachable
through `web/src/lib/ai.ts`: that module returns `LanguageModel`s and Jev is an evaluation model,
so adopting it means a second code path in the grader, not an env switch.

- Price: $0.042 per 1M input tokens, output free (search summaries of vercel.com and pricing blogs).
- Latency: 127–276 ms median in third-party benchmarks
  ([jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks),
  [LiteLLM](https://docs.litellm.ai/blog/jev-auto-router-benchmark)).
- Grading evidence: arXiv 2609.29769 (snippets only) found Jev matches an LLM rubric judge
  when the rubric is closed and the evidence is in the request, which is our setup, at 29–325×
  lower cost and far lower variance. Caveats: badly calibrated on some datasets, and nobody has
  tested it on short technical answers against key points.
- Data: not trained on customer data; zero retention is enterprise-only or via Gateway settings.
  Grading would send question, reference, key points and the user's answer. That already goes to
  DeepSeek today, so it adds a processor, not a new category of exposure.

### Fit per job

**1. Answer grading** (`web/src/lib/feed/grader.ts`). Jev's shape fits: one yes/no question per
key point. But the upside is small, because grading is already cheap:

| | Estimate |
|---|---|
| Tokens per grade | ~270–640 in, ~15 out (o200k tokenizer as a proxy; DeepSeek's is on blocked huggingface.co) |
| Flash cost per grade | ~$0.0001 at peak ($0.30 / $1.20 per 1M, matching `web/src/lib/ai/cost.ts`) |
| Volume assumed | 5 users × 50 AI-graded answers/day × 30 = 7,500/month (upper bound; exact matches skip AI) |
| Monthly, Flash | ~$0.85 (range $0.73–1.57) |
| Monthly, Jev | ~$0.10 |

So Jev saves at most ~$1.40/month. It is only worth adopting if it also grades **more
consistently** than Flash, which the 7-answer benchmark can test but not prove. Verdict: spike
further, low priority. Adopt only after it matches Flash on 50–100 real answers graded by hand
and varies less across repeats. If adopted and wrong, every card answer drifts silently, which
is what users feel most, so keep Flash as the fallback.

**2. Coach**. Neither can do tool-using chat. Skip both. Nothing found beats a tool-calling LLM
here; this research didn't turn up a better coach model worth a spike.

**3. Pipeline**. Competitive triage (`pipeline/src/pipeline/normalize/competitive.py`) asks for
a free-text `title` plus 1–4 of 49 techniques over ~1,200+ tokens of input. Laya can't produce
the title, its English checkpoint reads ~320 tokens, and 49-way multi-label is where its
accuracy collapses. The job has already run (268 kept); a full Flash re-run is ~$0.90 peak,
~$0.45 off-peak. The SPEC experiment would cost hours of hand-labelling 200 problems to save
under $1. Card generation is generation; neither applies.

### Running the grading benchmark

`web/scripts/check-grading.ts` uses whatever `AI_*` env is set, so it already covers DeepSeek
direct and any OpenAI-compatible endpoint. For Jev and for hidden-token counting, a throwaway
spike is committed at `.planning/research/spikes/grading/` (same 7 answers and prompt; records
latency, input/output/hidden tokens, Jev's per-key-point probability, and grade changes across
repeats). It runs here up to authentication and fails with exactly:
`DeepSeek API key is missing … DEEPSEEK_API_KEY`,
`Unauthenticated request to AI Gateway … AI_GATEWAY_API_KEY`,
`TypeSafe API key is missing … TYPESAFE_AI_API_KEY`.

On a machine with keys (about 1–3 cents in total):

```bash
cd web && bun run check:grading                       # baseline, uses web/.env.local
cd ../.planning/research/spikes/grading && bun install
SPIKE_BACKEND=deepseek DEEPSEEK_API_KEY=... SPIKE_REPEATS=3 bun grade-spike.ts
SPIKE_BACKEND=deepseek DEEPSEEK_API_KEY=... SPIKE_THINKING=on bun grade-spike.ts   # what a lost NO_THINKING costs
SPIKE_BACKEND=jev-gateway AI_GATEWAY_API_KEY=... SPIKE_REPEATS=3 bun grade-spike.ts
SPIKE_BACKEND=jev-gateway AI_GATEWAY_API_KEY=... SPIKE_JEV_THRESHOLD=0.7 bun grade-spike.ts
```

The Gateway model id for DeepSeek Flash (`deepseek/deepseek-v4-flash`) is a guess; check the
Gateway model list before using `SPIKE_BACKEND=gateway`.

---

## Area 2: leetcode-stats-api

### What it is

A Java 8 / Spring Boot 2.4 service ([repo](https://github.com/JeremyTsaii/leetcode-stats-api)),
last commit 2021-02-03. One endpoint, `GET /{username}`, which sends one query to the same
`https://leetcode.com/graphql` we already call and returns solved counts, question totals,
acceptance rate, ranking, reputation and `submissionCalendar`. No LICENSE file (only an MIT
badge). The public Heroku instance looks dead: open issues report 500/503/"Application error"
up to April 2026 with no maintainer reply, and a July 2025 dependency PR was never merged.

### Against what we have

Our adapter (`web/src/lib/activity/leetcode.ts`) already gets everything SPEC §6.6 needs from
LeetCode directly. The proxy lacks the parts that matter:

| Need (SPEC §6.6) | Ours | leetcode-stats-api |
|---|---|---|
| Last ~20 submissions, accepted **and failed**, with timestamps | `recentSubmissionList` + `recentAcSubmissionList` (`leetcode.ts:30-36`) | **None** |
| First-try vs failed detection | `sync.ts:20-61` | Impossible without submissions |
| Accepted / failed / untouched by difficulty | `userProfileUserQuestionProgressV2` (`leetcode.ts:39-50`) | Solved only |
| Anything we lack | | `submissionCalendar`, which is one extra field in our own query if we ever want a heatmap |

It would add a second point of failure on a dead host, a shared egress IP that is likelier to
be blocked than our ~5 users' traffic, and members' usernames sent to an unknown operator. The
better-maintained alternative, [alfa-leetcode-api](https://github.com/alfaarghya/alfa-leetcode-api)
(last commit 2026-08), sends the identical queries we do, and its public instance caches for
5 minutes and limits each IP to 120 requests/hour, so the Sync button could show stale data.

**On "No third-party proxy"**: I agree with it. The only real case for a proxy is LeetCode or
Cloudflare blocking Vercel's egress. That hasn't been observed, backoff plus manual check-ins
already cover it, and a self-hosted relay is the answer if it happens, not someone else's.

### Gaps in our adapter worth fixing instead

1. **A wrong username is invisible.** Measured live later: for a username that doesn't exist,
   `recentSubmissionList` returns `[]` and `userProfileUserQuestionProgressV2` returns empty
   lists, not an error or null, so sync just says "Up to date" forever. Only `matchedUser` errors
   ("That user does not exist."). Fixed in #16 by asking for `matchedUser` in the same query and
   returning `unknown_user`, which the Sync button explains.
2. **A LeetCode relabel would silently flip every solve to failed.** `"Accepted"` is hardcoded
   (`merge.ts:15`, `sync.ts:30`) and GraphQL errors aren't tagged for Sentry. Report unknown
   `statusDisplay` values and GraphQL errors to Sentry.
3. **Untested from Vercel.** Make one call from a preview deploy in `bom1` before turning on
   `LEETCODE_SYNC_ENABLED`.

---

## Area 3: Letta vs Mem0 vs Zep, against `coach_memory`

The Medium comparison was blocked here; its content came from search summaries. Findings below
are mostly from reading the cloned repos.

### What we built

- **Table** `coach_memory` (`supabase/migrations/20260928000010_coach.sql:33`): kind, text ≤500
  chars, evidence list, status (active / improving / resolved), source (user / coach), owner-only
  under RLS.
- **Extraction** (`web/src/lib/coach/memory.ts:47-104`): one Flash call at temperature 0 with
  `NO_THINKING` after each thread, review or mock. Input: a short system prompt, the full current
  memory block, and the first 12,000 characters of the new material. Output: up to 8 new facts
  plus ids of known facts seen again. Roughly 4.3k tokens in, 300–600 out, ~$0.0018 each,
  ~$0.55/month at ~300 extractions.
- **Merge** (`memory-rules.ts:27-41`): a new fact is dropped only on an exact normalized-text
  match; seen facts go back to active with new evidence.
- **Aging** (`memory-rules.ts:48-58`): weekly, habits only: improving after 14 quiet days,
  resolved after 28. Goals and context never age.
- **Injection**: every active and improving fact goes into every coach prompt, with its UUID.
  A 30-fact block is ~1,100 tokens, ~70% of which is UUIDs.

At tens of facts per user, the whole block fits in the prompt, so retrieval (the main thing
these services sell) solves a problem we don't have yet.

### Per service

**Mem0** ([repo](https://github.com/mem0ai/mem0)). The open-source version's `add()` now only
adds facts; it never updates or deletes, so it handles contradictions worse than we could with
one schema change. Graph memory is Platform-only (paid). It needs an embedding provider, and
DeepSeek has none, so user text would go to a second vendor; it also sends usage telemetry to
PostHog by default. Platform is US-hosted: free tier 10k adds/month, Starter ~$19–20 (search
summaries). TS SDK exists and it can store in Supabase pgvector. **Skip.**

**Zep / Graphiti** ([zep](https://github.com/getzep/zep),
[graphiti](https://github.com/getzep/graphiti)). The self-hosted Community Edition is
deprecated. Zep Cloud stores full transcripts off our infra; at our volume the likely plan is
the $25 Flex tier, 2.5× our whole AI budget (search summaries). Self-hosting Graphiti means a
Python service plus Neo4j or FalkorDB plus an embedder, and about 3 + E LLM calls per episode
(E = new facts, typically 5–15), roughly $3–6/month on top of the infra. DeepSeek isn't
documented for its bring-your-own-LLM. Its one real advantage, retiring contradicted facts with
validity dates, fits in a couple of columns in our table. **Skip.**

**Letta** ([repo](https://github.com/letta-ai/letta)). The V1 server has moved to an archive
branch; Letta is now an agent harness (letta-code). Adopting it would replace our coach loop,
tools, Confirm/Dismiss proposals and budget metering, not just memory. DeepSeek support is
unverified. **Skip.**

**Does the SPEC decision still hold?** Yes, more clearly than when it was made. Each service
would send coach threads or memory (the most private data we hold) to a new processor, cost
between a quarter and several times our monthly AI budget, and in two of three cases handle
contradictions no better than we can.

**Migration, if we ever did it**, would mean: an adapter behind `listMemory` / `extractMemory`
/ `memoryBlock` in `memory.ts`; one namespace per user; a backfill of existing rows; replacing
the "What Coach knows" edit and delete paths (`memory-edit.ts`) with the service's API; and a
deletion path for when a user leaves. About 2–3 days plus a new vendor in the privacy notes.

### Gaps in our memory worth fixing instead

1. **Contradicted facts both stay active** (`memory-rules.ts:27-41`). "Amazon interview Nov 20"
   and "moved to Dec 5" both reach the prompt. Add a `replaces` field to the extraction schema,
   as the chat `save_memory` tool already has (`tools.ts:180`).
2. **Goals and context never expire** (`memory-rules.ts:52`), so past-dated goals stay forever.
3. **The aging clock resets itself.** `ageMemory` updates `status` (`memory.ts:112-115`), and the
   `coach_memory_touch` trigger (migration line 147) bumps `updated_at`, which is also what
   `ageFacts` measures quiet time from. So "resolved after 28 days" really lands at ~42+ days.
   `check-coach.ts` jumps straight from a fresh row to 30 days and misses it. Fix: a
   `last_seen_at` column set only when new evidence arrives.
4. **Deleted facts come back.** `deleteFact` hard-deletes (`memory-edit.ts:26-31`), so the next
   extraction can re-learn what the user just removed. A `dismissed` status fixes it.
5. **Long threads lose their ending** (`memory.ts:75` keeps the first 12,000 characters, and
   conclusions are usually at the end). Keep head plus tail.
6. **UUIDs are ~70% of the memory block's tokens.** Short per-prompt aliases (`[m1]`) would cut
   it; the chat tool's `replaces` would need the alias map.

---

## What to do instead (ranked)

Items 1, 2 (gaps 1–4) and the first LeetCode gap were fixed in the same PR as this doc (#16),
after the owner asked for them. Item 1 turned out to be a non-issue once measured (see
"Measured later"); the guard stays because it costs nothing.

1. ~~**Count DeepSeek thinking tokens in the web cost meter.**~~ Measured: no gap. `recordUsage` / `trackCoachUsage`
   (`web/src/lib/ai/usage.ts:18`, `web/src/lib/coach/model.ts:25`) record only
   `inputTokens` / `outputTokens`. `@ai-sdk/deepseek@3.0.54` sets
   `outputTokens.total = completion_tokens` and never reads `total_tokens` (checked in its
   `dist/index.js`). The pipeline already fixed this (`pipeline/src/pipeline/llm.py:135-143`);
   the web app didn't. Grading, memory, weekly and mock scoring pass `NO_THINKING` and are fine,
   but **coach chat** (`app/api/coach/chat/route.ts:123`) and **solution review**
   (`coach/solution-review.ts:89`) run Pro with thinking on. If DeepSeek still leaves thinking out
   of `completion_tokens` (the handoff says it did, 5× under the bill), the budget guard trips
   late. Fix: add `usage.raw.total_tokens − in − out` as the pipeline does. Confirm with one real
   coach call first. This is a bigger lever than any model swap in this doc.
2. **Memory contradictions and aging**: items 1–4 of the Area 3 list. Small, local, keeps data
   in our database.
3. **LeetCode adapter hardening**: the three items in Area 2.
4. **Optional**: run the Jev grading spike when someone has a Gateway key handy.
5. **SPEC edits**: mark the §3 Laya row closed (skipped, reasons here) and record in the Coach
   memory row that Zep, Letta and Mem0 were evaluated on 2026-09-27 and skipped.

## Sources

- Laya: https://github.com/NandhaKishorM/laya
- Jev (blocked sites, via search): https://typesafe.ai/blog/introducing-system-one-models-and-jev,
  https://www.jevai.org/, https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway,
  https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk, https://www.datacamp.com/blog/system-one-models-jev,
  https://flaviocopes.com/jev/, https://docs.typesafe.ai/models, https://www.eesel.ai/blog/typesafe-jev-pricing,
  https://jevaiguide.com/faq/does-jev-train-on-your-data/
- Jev benchmarks: https://github.com/AbdelStark/jev-benchmarks, https://docs.litellm.ai/blog/jev-auto-router-benchmark,
  https://arxiv.org/abs/2609.29769, https://arxiv.org/html/2609.26550v1
- DeepSeek pricing: https://benchlm.ai/deepseek/api-pricing, https://www.aipricing.guru/deepseek-pricing/
- npm source read directly: `ai@7.0.116`, `@ai-sdk/deepseek@3.0.54`, `@ai-sdk/gateway@4.0.96`, `@ai-sdk/typesafe-ai@3.0.8`
- LeetCode: https://github.com/JeremyTsaii/leetcode-stats-api (and its issues, e.g. #18),
  https://github.com/alfaarghya/alfa-leetcode-api
- Memory: https://medium.com/asymptotic-spaghetti-integration/from-beta-to-battle-tested-picking-between-letta-mem0-zep-for-ai-memory-6850ca8703d1
  (blocked; via search), https://github.com/mem0ai/mem0, https://github.com/getzep/graphiti,
  https://github.com/getzep/zep, https://github.com/letta-ai/letta, https://github.com/letta-ai/letta-code,
  https://www.getzep.com/pricing/, https://help.getzep.com/bring-your-own-llm, https://docs.letta.com/pricing
