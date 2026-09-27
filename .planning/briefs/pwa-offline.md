# Brief I — Installable app + offline Today and Feed

**Read `.planning/briefs/README.md` first.** This brief adds only what is specific to this task.

Branch: your pinned branch. PR to `main`.

## Why
Spec §3 **Offline**: "Read-only: today's missions and ~30 queued cards cached; answers sync and grade when back online." 90x is used on phones daily, so it should install like an app (Home Screen icon, splash, standalone window).

## What exists
- `web/src/app/manifest.ts` (minimal, favicon only), `web/public/sw.js` (web push + notification click only — keep those handlers working), push registration in `web/src/components/push/push-settings.tsx` (registers `/sw.js`).
- Today (`web/src/app/(app)/today/page.tsx`, server-rendered) and Feed (`web/src/app/(app)/feed/*`, `web/src/app/actions/feed.ts`: `getNextCard`, `submitAnswer`; card answers are graded on the server — never grade offline).
- Brand: `web/src/components/brand.tsx` ("90" + cyan "x"), tokens in `web/src/app/globals.css` (bg `#0a0c10`, accent `#67e8f9`), fonts in `web/src/app/fonts/`.

## Build
1. **Icons and install**: generate PNG app icons (192, 512, maskable 512, Apple touch 180) from a simple SVG mark ("90x" in Sora bold on the dark background, cyan x) with a small script (`web/scripts/make-icons.ts`, e.g. using `sharp`, committed output in `web/public/icons/`). Complete the manifest (name, short_name, description, start_url `/today`, display `standalone`, background/theme colours from tokens, icons incl. maskable, categories). Apple meta (apple-touch-icon, `apple-mobile-web-app-capable`, status bar style) via `layout.tsx` metadata. Check the Next 16 docs in `web/node_modules/next/dist/docs/` for `manifest` and metadata APIs.
2. **Service worker caching** (extend `public/sw.js`, keep push handlers):
   - Precache the app shell assets that make `/today` and `/feed` render offline (Next static chunks for those routes are hashed — cache on first successful fetch with a stale-while-revalidate strategy for `/_next/static/*` and fonts; network-first for HTML navigations with the last good copy as fallback; never cache `/api/*`, server actions, or auth routes).
   - An offline fallback page (`web/src/app/offline/page.tsx`, static) for routes never visited.
3. **Offline Today**: when offline, Today shows the last cached render with a small banner "You're offline. Showing today as of 10:42." Mission actions (check-in, Mark studied, skips) are disabled with a note.
4. **Offline Feed**: while online, keep ~30 upcoming cards (the CardView only — no answers exist client-side) in IndexedDB (`web/src/lib/offline/` — small wrapper, wrap every call in try/catch). Offline, the Feed serves from that cache; submitting stores the answer in an IndexedDB outbox and shows "Saved. It'll be graded when you're back online." On reconnect (`online` event and on app open) the outbox is flushed through `submitAnswer` one by one, in order; results show as a small "3 answers graded" toast/line. Duplicates must not be created (use a client-generated id per answer and have the server ignore repeats — if that needs a server change, add an optional `clientId` to the answer input and a unique check in `answerCard` via a Redis `SET NX` key `key("feed","ans",userId,clientId)` with a 1-day TTL; no migration).
5. **Tests**: Vitest for the outbox/queue logic (pure parts), and a Playwright test in `web/e2e/` that goes offline (`context.setOffline(true)`) after loading Today and checks the offline banner renders (skip Feed offline in e2e if Redis isn't available in CI yet; say so).

## Verification
All README checks pass; Lighthouse-style installability is described in the PR (manifest fields + icons present); the PR lists exactly which routes work offline and how you verified it.
