# Brief B — `/admin/cards`: batch review + flagged cards (Part 4, Task 10)

**Read `.planning/briefs/README.md` first** — it has how we write code, verify, open PRs, and when to ask. This brief adds only what is specific to this task.

Branch: `admin-cards` from `main`. PR to `main` when done.

## Why

~8,500 AI-generated cards sit in Supabase as **drafts**. The admin (Aman) approves them in ~15 batches: for each batch he sees 20 cards, the riskiest first, and marks each Good or Bad. 18 of 20 good publishes the whole batch (its cards go live in the Feed); fewer rejects it (the pipeline regenerates it later). Cards users flag twice are hidden and wait here too.

## Data you use (already migrated; types in `web/src/db/pulled/schema.ts`, import from `@/db/schema`)

- `card_batches`: `id, domain, label (text|null), topicSlugs, aiPassRate, samplePassRate, status ('draft'|'published'|'rejected'), reviewedBy, reviewedAt, createdAt`.
- `cards`: `id, batchId, topicSlug, problemSlug, documentId, format, difficulty, promptMd, options (jsonb string[]|null), answerMd, keyPoints (jsonb string[]), sourceRefs (jsonb [{kind,id,title}]), quality (jsonb {correct,clear,relevant,issues}), status ('draft'|'live'|'retired'), hidden (bool), risk (real|null), flagCount`.
- `batch_review_items`: `batchId, cardId, verdict ('good'|'bad'), note, decidedBy, createdAt` — PK (batchId, cardId).
- `card_flags`: `userId, cardId, reason, createdAt`.
- `topics`: `slug, name, domain`. `profiles`: `userId, name`.
- Use `db` from `@/db` (server connection). **Every page and action checks `viewer.isAdmin`** (`requireViewer()`; `notFound()` for non-admins, like `web/src/app/admin/users/page.tsx`).

## Sampling rules

Use `web/src/lib/feed/review-sample.ts` with exactly these exports (another agent writes and tests the real module in parallel on branch `feed-logic`):
```ts
export const SAMPLE_SIZE = 20;
export const PASS_AT = 18;
export function pickReviewSample(cards: { id: string; risk: number | null }[], seed: number, size?: number): string[];
export function batchVerdict(verdicts: ("good" | "bad")[], size?: number, passAt?: number): "pending" | "published" | "rejected";
```
If that file isn't on `main` when you start, create it on your branch with these signatures and a simple correct implementation (riskiest half + seeded random rest; verdict pending until `min(size, batch card count)` verdicts, published when goods ≥ `ceil(passAt / size * n)`), with a short test. The lead resolves the merge.

Seed = a stable number from the batch id (e.g. sum of char codes), so the same batch always shows the same 20 cards.

## What to build

1. **`web/src/lib/admin/cards.ts`** (`server-only`): queries
   - `listBatches()` → per batch: id, label (fallback: domain), domain, card count, draft count, AI pass rate, status, verdicts so far (good/bad counts), reviewedAt.
   - `batchForReview(batchId)` → batch + its 20 sample cards (via `pickReviewSample`) with topic name and any existing verdict per card.
   - `flaggedCards()` → hidden cards with flag reasons (joined `card_flags`, newest first) and flag count.
2. **`web/src/app/admin/cards/actions.ts`** (`"use server"`, admin-only, Zod-validated, `FormState` results):
   - `recordVerdict(batchId, cardId, verdict, note?)` — upsert into `batch_review_items` (with `decidedBy = viewer.id`), then compute `batchVerdict` over that batch's verdicts for the sample. When it becomes `published`: set batch `status='published'`, `samplePassRate`, `reviewedBy`, `reviewedAt`, and all its cards with `status='draft'` → `'live'` (in one transaction). When `rejected`: batch `status='rejected'` (cards stay draft). Return `{ ok, note }` saying what happened.
   - `undoVerdict(batchId, cardId)` — only while the batch is still `draft`.
   - `resolveFlag(cardId, action: 'keep' | 'retire')` — keep: `hidden=false`, delete its `card_flags`, `flagCount=0`; retire: `status='retired'`.
   - `revalidatePath` the admin pages after each.
3. **Pages** (each with `loading.tsx` + `error.tsx`):
   - `web/src/app/admin/cards/page.tsx` — list of batches grouped by area (DSA, Design, CS, Java, SQL): label, count, AI pass rate, a progress bar of verdicts (e.g. 12/20), status chip (Draft / Published / Rejected). Link to each batch. A second section: **Flagged** with count and link.
   - `web/src/app/admin/cards/[batchId]/page.tsx` — one card at a time (client component for navigation): area dot + topic, format, difficulty, prompt (use `Markdown` from `@/components/markdown`), options if any, answer, key points, source ref title, and the AI reviewer's scores and issues (from `quality`) highlighted when any score < 5. Buttons **Good** / **Bad** (+ optional note field for Bad), **Prev/Next**. Keyboard: `G` good, `B` bad, `←`/`→` navigate. Header shows "12 of 20 reviewed · 11 good" and the outcome once decided. Optimistic update of the verdict (`useOptimistic`), errors inline.
   - `web/src/app/admin/cards/flagged/page.tsx` — list of hidden cards with prompt, answer, reasons; **Keep** / **Retire** buttons.
   - Add a small link row to `/admin/users` and `/admin/cards` (e.g. in both page headers: "Users · Cards") so the admin can move between them.
4. Tests: pure helpers you add (e.g. a function that computes the header counts or seed-from-id) get Vitest tests. Database code can't be tested in your environment — say so in the PR.

## Definition of done

- Pages, actions and queries above, admin-gated, with loading/error/empty states, mobile and desktop layouts.
- All checks from README pass (typecheck, lint, test, format:check, check:tokens, check:dead, build with dummy env).
- PR description per README, including a short "How to test" for the lead (which URL, what to click, what should change in the database).
