# Working on 90x — read this before any brief

90x is a small, invite-only interview-prep app (Aman and friends). You are one of several agents building it in parallel; another agent (the "lead") reviews your pull request before it is merged. Follow this file and your brief exactly.

## Decide, don't ask

- **Don't ask the owner questions** — he isn't answering them. When something in the brief is ambiguous, contradicts the code, or needs a product decision, pick the option closest to the spec and the plan's Decisions, keep going, and list it under **Decisions** in the PR description with what it would cost if wrong. The lead reviews every decision before merging.
- Never widen scope: do only what the brief says. Ideas for more go under **Suggestions** in the PR.

## Source of truth

1. Your brief (`.planning/briefs/<name>.md`) — exact interfaces and definition of done.
2. The active plan (`.planning/plans/2026-09-27-part4-feed.md`), especially its **Decisions** section.
3. `.planning/SPEC.md` — product spec. The brief wins over the plan, the plan over the spec.
4. `web/AGENTS.md`: **this is Next.js 16**, APIs differ from older versions. Before writing framework code (routing files, `error.tsx`, `loading.tsx`, server actions, config), read the matching guide under `web/node_modules/next/dist/docs/`. Example: error boundaries receive `retry`, not `reset`; `middleware` is `proxy.ts`.

## Setup

- Everything app-side lives in `web/` (Next.js 16 App Router, React 19 with React Compiler, TypeScript strict + `noUncheckedIndexedAccess`, Tailwind v4, Drizzle, Supabase, Bun). `bun install` in `web/`.
- You have **no secrets, no database, no `.env.local`**. Don't try to connect to Supabase/Upstash/AI providers; don't create env files. Code that needs them must still typecheck and build.
- Never commit secrets, `.env*`, `.data/`, or generated files you didn't regenerate on purpose (`web/src/db/pulled/**`, `web/src/lib/supabase/database.types.ts` are generated — read them, don't edit them).
- Don't add or change SQL migrations (`supabase/migrations/`) — ask instead.

## How we write code

- Match the surrounding code: small focused files, pure functions for logic (in `web/src/lib/<area>/`), server code marked `import "server-only"`.
- Comments: short, explain **why**, not what. No AI-slop prose, no emoji, no banners.
- No `any`, no non-null `!` unless the invariant is local and obvious. Prefer guards and early returns.
- Names say what things are; no abbreviations beyond common ones.
- **Security:** server code uses Drizzle (`@/db`) over a connection that **bypasses row-level security**. Every query must be scoped to the signed-in user's id (from `requireViewer()` in `@/lib/auth/viewer`) or be admin-only behind `viewer.isAdmin` (return `notFound()` for non-admins, like `web/src/app/admin/users/page.tsx`).
- **Server actions** return `FormState` (`{ ok?, error?, note? }` from `@/components/form`) and never throw to the UI: wrap work in try/catch, log with `console.error`, return a short human error. Validate input with Zod.
- **UI rules (spec §7):**
  - Only the six text sizes: `text-display`, `text-title`, `text-heading`, `text-body`, `text-small`, `text-tag` (plus `text-dial` for the readiness dial). No `text-sm/xs/lg`, no `text-[13px]`.
  - Colours only from tokens: `text-text`, `text-text-2`, `text-mute`, `bg-surface`, `bg-surface-2`, `border-line`, `border-line-2`, `text-cyan`/`bg-cyan`/`bg-cyan-bg`, `text-on-cyan`, topic colours `bg-topic-dsa|sd|cs|java|sql`, status `text-ok|warn|bad`. No hex, no Tailwind palette colours.
  - Borders on cards, no shadows (except floating layers). Dark theme only.
  - No native `<select>`/checkbox on desktop: use `ChipGroup`/`Switch` from `@/components/chip-group` or buttons.
  - Every page segment has `loading.tsx` (skeleton shaped like the page, from `@/components/skeleton`) and `error.tsx` (`RouteError` from `@/components/route-error`). Empty data shows `EmptyState` (`@/components/empty-state`), never a blank area.
  - Buttons that submit use `SubmitButton` / `useServerAction` from `@/components/form` (pending label, `aria-busy`, inline error).
  - Mobile first (390px) and desktop (two columns where the mockups do). Mockups: `.planning/mockups/`.
- Copy: short, plain, second person ("You missed…"), no exclamation marks.

## Tests and verification (all must pass before the PR)

TDD for logic: write the test, run it, see it fail, implement, see it pass. Then from `web/`:

```bash
bun run typecheck      # next typegen + tsc
bun run lint           # ESLint (zero warnings) + oxlint (deny warnings)
bun run test           # Vitest
bunx oxfmt             # format (imports and Tailwind classes are sorted by it)
bun run format:check
bun run check:tokens   # design-token rules; the ratchet ceiling may not rise
bun run check:dead     # knip: nothing exported and unused
bun run build          # needs dummy env, see below
```

Build with dummy env (never real values):
```bash
DATABASE_URL=postgresql://ci:ci@localhost:5432/ci DIRECT_URL=postgresql://ci:ci@localhost:5432/ci \
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321 NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=ci \
NEXT_PUBLIC_APP_URL=http://localhost:3000 bun run build
```

`check:rls`, `check:tracker` and anything touching the database cannot run in your environment; say so in the PR and the lead runs them.

## Git and PR

- Branch from `main` with the name in your brief (if your session is pinned to its own branch name, use that and say so in the PR). Small commits, message = what changed and why, in plain English. End every commit message with:
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```
- Never push to `main`, never merge, never force-push someone else's branch, never skip hooks (`--no-verify`).
- Open a PR to `main`. Description sections: **What** (one line per file/area), **Decisions** (anything you interpreted, with cost if wrong), **Checks** (each command above with pass/fail), **Not verified** (what needs the database or a browser), **Suggestions** (optional).
