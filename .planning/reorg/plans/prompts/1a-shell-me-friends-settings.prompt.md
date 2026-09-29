You are building **unit 1a of the 90x reorg wave: the shell, Friends, Me and Settings**.

**Worktree** `../90X-wt/1a` · **Branch** `me-shell-friends` · **Playwright spec** `web/e2e/me-reorg.spec.ts`

Other agents may be building units 1b, 1c, 1d, 3 and 4 at the same time in their own
worktrees. Never touch their files.

## Read these first, in this order

1. `.planning/reorg/plans/prompts/SETUP.md` — your environment, how to test, every gate, the
   forbidden files, the PR format. **Read it before you write any code**; it contains the
   one flag (`E2E=1`) without which no test can sign in.
2. `.planning/briefs/README.md` — how this codebase is written. Wins over everything.
3. **`.planning/reorg/plans/1a-shell-me-friends-settings.md` — your plan.** Exact files, the
   existing functions to reuse with their real signatures, the tests, the traps.
4. `.planning/reorg/plans/README.md` — the wave's cross-cutting decisions.
5. `.planning/reorg/me-coach-reorg.brief.md` — the intent, shell/Friends/Me/Settings parts.
6. `.planning/reorg/DECISIONS.md` — Navigation, Friends, Me and Settings sections.
7. `.planning/reorg/mocks/friends.html`, `me.html`, `settings.html` — visual references.
8. `web/AGENTS.md` — **this is Next.js 16**; read the guide under
   `web/node_modules/next/dist/docs/` before writing routing, `error.tsx`, `loading.tsx` or
   server-action code.

Worked examples already merged, in this exact style: `web/src/components/library/roadmap-graph.tsx`,
`web/src/components/ui/segmented.tsx`, `web/e2e/roadmap.spec.ts`, `web/e2e/mock-picker.spec.ts`.

## What you are doing

Me renders eleven blocks. Friends moves to its own route, notifications and sign-out move to
a new Settings page, and Me keeps readiness, weakest patterns, this week, and a LeetCode
block that collapses.

**This is an add-on.** Keep every existing behaviour and control. Move things, do not delete
them. Where a mock differs from today's behaviour, today wins unless your plan says
otherwise. Do not rewrite a page from scratch.

**This is the widest diff in the wave**, so it is the one most likely to collide with
another unit. Stay inside the files your plan lists.

## The five traps that will cost you most

1. **The mobile tab bar stays five tabs.** Friends is a **desktop sidebar entry only**,
   reached from Me on a phone. `PLAN.md` §5.1 and D1 say six tabs and `grid-cols-6` — those
   lines are struck, and `DECISIONS.md` wins. Building `grid-cols-6` is the single most
   likely wrong turn here.
2. **`revalidatePath`.** `me/friends-actions.ts` revalidates `/me` and `/today` today. Every
   action needs `/friends` **added** and `/today` **kept** — `PendingRequests` still renders
   on Today for someone with no campaign. `revokeAction` only revalidates `/me`; it needs
   `/friends` too. In `app/actions/push.ts`, three `revalidatePath("/me")` calls become
   `/me/settings`. **The e2e test that accepts a pending request is what proves this**, and
   it is the assertion most likely to be missing.
3. **`PendingRequests` stays on Today.** Only *Me* loses it.
4. **There is no "list my friends" query.** `scoreboard` is the only thing returning friends
   with names, and only approved, setup-done ones. Do not write a new one.
5. **`pendingFor` takes an email** and `viewer.email` is `string | null`; today's page passes
   `viewer.email ?? ""`. Keep that.

## Verification

Everything in SETUP.md, plus these database checks: `bun run check:rls`, `check:tracker`,
`check:friends`.

Your spec must be `web/e2e/me-reorg.spec.ts`, run with `--retries=0` at least three times.
Screenshots at 390px and 1440px of `/me`, `/friends` and `/me/settings`.

Report back as SETUP.md section 8 describes.
