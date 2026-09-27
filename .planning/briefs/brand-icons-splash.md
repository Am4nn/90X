# Brief K — Favicon, app icons, link previews, iOS launch images, loading splash

**Read `.planning/briefs/README.md` first.** This brief adds only what is specific to this task.

Branch: your pinned branch. PR to `main`.

## Why
90x is used as an installed app on phones and shared as a link in chats. Today the favicon is Next's default `favicon.ico`, a pasted link shows a bare domain, iOS shows a white screen on every cold start (no launch images), and the app has no branded splash while it loads. Our sibling project Curfew does all of this properly — copy its approach (described below; you can't read its repo).

## What exists
- Brand: `web/src/components/brand.tsx` — "90" + cyan "x" in Sora 700. Tokens in `web/src/app/globals.css` (bg `#0a0c10`, surface `#0f1218`, accent `#67e8f9`, text `#e6e9ef`, mute `#7d8594`). Fonts: `web/src/app/fonts/` (woff2 only) and `web/scripts/fetch-fonts.ts`.
- `web/scripts/make-icons.ts` + `web/public/icons/*` (192, 512, maskable 512, apple-touch 180, from PR #9), `web/src/app/manifest.ts`, `web/src/app/layout.tsx` (metadata, `appleWebApp`), `web/public/sw.js` (caches `/icons/*`, favicon, manifest — keep that working).
- Next 16 file conventions — read `web/node_modules/next/dist/docs/` for `icon`, `apple-icon`, `opengraph-image`, `twitter-image`, `robots`, `sitemap`, `manifest` and `metadataBase` before coding.

## Build

### 1. One mark, everywhere
- `web/src/app/icon.svg`: the favicon as SVG (the "90x" mark on the dark ground, cyan x; legible at 16px — if "90x" is unreadable that small, use a simplified mark such as a cyan "x" in a rounded dark square, and use it only for the tiny sizes; explain in the PR).
- Replace `web/src/app/favicon.ico` with a real multi-size ICO (16, 32, 48) generated from the same mark (script output committed).
- `apple-icon` (180, no transparency, mark at ~58% of the tile) and manifest icons 192/512 + maskable 192/512 (mark inside the safe circle: ~22% inset), all from `make-icons.ts` so every icon comes from one drawing function. Keep file names the manifest and SW expect, or update both.

### 2. iOS launch images (the white-screen fix)
- Extend `make-icons.ts` to render launch PNGs to `web/public/splash/` for every iPhone still getting iOS updates, portrait, at exact device pixels: 440×956@3, 402×874@3, 430×932@3, 393×852@3, 428×926@3, 390×844@3, 375×812@3, 414×896@3, 414×896@2, 375×667@2. Each: the mark centred on `#0a0c10` at ~22% of the short side.
- In `layout.tsx`, render `<link rel="apple-touch-startup-image" media="(device-width: Wpx) and (device-height: Hpx) and (-webkit-device-pixel-ratio: S)" href="/splash/splash-WxH@Sx.png">` for each (the metadata API has no field for it; React hoists `<link>`s into `<head>`). The media query must name all three values or iOS ignores it.
- Android uses the manifest: set `background_color` `#0a0c10`, `theme_color` `#0a0c10`, icons as above.

### 3. Link previews and search
- `web/src/app/opengraph-image.tsx` (and `twitter-image.tsx` re-using it): 1200×630, drawn with `ImageResponse` — the mark, "90x", one line "Interview-ready in 90 days, with friends." and a subtle 90-square grid motif in the accent colour. Satori can't read woff2: add Sora 700 and Manrope 500 **TTF** files (extend `fetch-fonts.ts` to also fetch TTFs into `web/assets/fonts/`, committed) and load them with `readFile`. Never show any user data.
- `metadata`: `metadataBase` from `NEXT_PUBLIC_APP_URL` (fallback `https://90x.amanarya.com`), title template stays `%s · 90x`, a real `description`, `openGraph` (siteName, type, locale) and `twitter` (`summary_large_image`).
- `web/src/app/robots.ts`: invite-only app — allow `/` and `/sign-in`, disallow everything else (`/api/`, app routes, `/admin`, `/setup`, `/pending`, `/offline`), with a comment that this is not access control. `web/src/app/sitemap.ts`: just the sign-in page.
- App pages behind sign-in should carry `robots: { index: false }` via the `(app)` layout's metadata; the sign-in page stays indexable.

### 4. Loading splash (branded, fast)
- A splash shown on **cold start** (first load of the app in a tab or when launched from the Home Screen) until the app shell has painted and hydrated: full-screen `#0a0c10`, the mark centred, a short tasteful animation (e.g. the cyan "x" draws its two strokes, or the mark fades/scales in with a thin progress line under it), then fades out over ~200ms.
- Must be **server-rendered inline** in `layout.tsx` (a fixed div + small CSS in `globals.css`, no image request, no layout shift) so it shows before any JS, and removed by a tiny client component after hydration (and immediately if JS is slow to arrive? No — keep it until hydration, but cap at 2.5s with a CSS animation that fades it out regardless, so a slow network never traps the user behind it).
- Show it once per session: the client component sets a `sessionStorage` flag and an inline script in `<head>` adds a class that hides the splash when the flag is already set (so in-app navigations and reloads within a session don't flash it). Wrap storage access in try/catch.
- `prefers-reduced-motion`: no animation, just the mark and a quick fade.
- Route-level `loading.tsx` skeletons stay as they are (they're for navigations, not cold start).

### 5. Checks
- A small Vitest test for any pure helpers (e.g. splash table → media query strings).
- `e2e`: add a Playwright check that `/sign-in` serves an `og:image` meta, `/icon.svg` and `/manifest.webmanifest` return 200, and a splash link exists for 390×844@3.
- All README checks. Screenshots or a short description of the OG card and splash in the PR.
