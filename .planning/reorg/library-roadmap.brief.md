# Brief — Library Roadmap toggle

**Branch:** `library-roadmap` (or your session's branch; say so in the PR).
**Read first:** `.planning/briefs/README.md`.

## Rule one: this is an add-on

The mocks in `.planning/reorg/mocks/` are **visual references, not final designs**. **Library
keeps today's behaviour as its default** — same area tabs, same Pattern Map for DSA, same topic
cards and roadmap accordions for the other areas. This brief **adds a toggle**; it does not replace
anything. If in doubt, leave today's behaviour alone.

## What to add

A **`List / Roadmap` toggle**, above the content, on the areas that have a roadmap (system design,
CS, Java, SQL, LLD, AI, behavioural — i.e. **not DSA**):

- **Default = List**, which is exactly today's UI. Users see no change unless they switch.
- Switch to **Roadmap** → a roadmap.sh-style graph:
  - a vertical **spine** of main topics, **dashed branches** out to sub-topics,
  - the selected/current node highlighted in the accent,
  - a **tick** for covered nodes,
  - **dashed nodes are lessons we haven't written yet** — still tickable, labelled "soon".
- Tapping a solid node opens its lesson; the toggle is a **segmented control**, not chips.

## Where

- `web/src/app/(app)/library/page.tsx` — the non-DSA branch.
- A new client component `web/src/components/library/roadmap-graph.tsx` (the graph), and the toggle
  itself (reuse a segmented-control pattern; there is none today, so a small one is fine).
- Data: reuse `roadmapsFor` (`lib/library/roadmap.ts`) and `areaTopics`. Do **not** add migrations.
- The graph is a **rendering of existing roadmap tiers and topic links** — no new content, and no
  pretending a node has a lesson when it does not.

## What not to change

- DSA: no toggle. Pattern Map (`components/library/pattern-map.tsx`) and the problem list stay.
- The area tabs (`AreaTabs` in `library/page.tsx`) stay exactly as they are — note they are a
  bordered container with rounded items, **not** pill tags.
- `loading.tsx` / `error.tsx` stay shaped like the page.

## Verification

From `web/`: `typecheck`, `lint`, `test`, `format:check`, `check:tokens`, `check:dead`, `build`.
Add a unit test for any pure layout helper. Screenshots at 390px and 1440px, both toggle states.
