# Unit 2 — the Library's Roadmap view

**Branch** `library-roadmap` · **Worktree** `../90X-wt/2` · **Spec** `e2e/roadmap.spec.ts`
**Brief** `.planning/reorg/library-roadmap.brief.md`

Read `.planning/reorg/plans/README.md` first.

## Scope

Library keeps everything it does today. This unit **adds** a `List / Roadmap` toggle on the
areas that have a roadmap, and a roadmap.sh-style graph behind it. Default is List, which
is byte-for-byte today's UI: a user who never touches the toggle sees no change.

**DSA gets no toggle** — it has no roadmap; its Pattern Map stays exactly as it is.

## Files

**Create**
- `web/src/components/library/roadmap-graph.tsx` — the graph
- `web/src/components/ui/segmented.tsx` — the toggle
- `web/src/lib/library/graph-layout.ts` — pure layout maths
- `web/src/lib/library/graph-layout.test.ts`
- `web/e2e/roadmap.spec.ts`

**Modify**
- `web/src/app/(app)/library/page.tsx` — the non-DSA branch only
- `web/src/lib/library/roadmap.ts` — **export the `RoadmapNode` type** (it is currently
  internal, and the graph component needs it). That is the only change to this file.

## Reuse, do not rewrite

```
roadmapsFor(userId, domain)          @/lib/library/roadmap
  -> Roadmap[]  { roadmap: string, nodes: RoadmapNode[], done: number }
  RoadmapNode = { id, label, kind, topicSlug: string|null, hasLesson: boolean, done: boolean }
  // NOT exported yet — export the type, change nothing else.

areaTopics(domain)                   @/lib/library/queries
AREAS, AreaKey                       @/lib/library/queries
RoadmapList roadmaps                 @/components/library/roadmap   (client, useOptimistic)
tickRoadmapNodeAction                @/app/actions/today
chip(on), button()                   @/components/button-styles
EmptyState, PageHeader
```

## What the data actually is — read this before designing the graph

`roadmapsFor` returns a **flat node list**. There are no tiers and no parent pointers:

- `kind` is only `'topic'` or `'subtopic'` (a database check constraint).
- Nodes are ordered by `roadmap`, then `sort`.
- `hasLesson` is true when a `lessons` row exists for the node's `topicSlug`. A node with a
  null `topicSlug` is always `hasLesson: false`.
- `done` comes from the user's `roadmap_progress` rows.

So the mock's structure maps onto the data like this, and **no new data is needed**:

| Mock | Data |
|---|---|
| The spine | `kind === 'topic'`, in `sort` order |
| Dashed branches off it | the `kind === 'subtopic'` nodes that follow, in order |
| Solid node, tappable to a lesson | `hasLesson: true` → link `/library/topic/<topicSlug>` |
| Dashed node, "soon", still tickable | `hasLesson: false` |
| Tick | `done: true` |
| Highlighted path | the current node |

**Sub-topics belong to the preceding topic by order.** There is no parent field, so that
grouping is an assumption — write it as one function in `graph-layout.ts`, test it, and say
so in the PR under **Decisions**.

## What to build

**The toggle** (`components/ui/segmented.tsx`) — a real segmented control, **not chips**.
There is nothing like it today; `ChipGroup` is rounded-full pills and the brief rules those
out. Copy the look of `AreaTabs` inside `library/page.tsx`: a bordered container
(`rounded-xl border border-line bg-surface p-1`) with rounded items, the active one
`bg-surface-2 text-text` and the rest `text-mute`. Keep it small and general —
`{ options, value, name }` — and drive it by URL so the page stays a server component:
`?view=roadmap`, default List when the parameter is absent or unrecognised.

**The graph** (`roadmap-graph.tsx`) — a rendering of the tiers and links already in the
database. It may be a server component if it needs no state; the ticks are the one
interactive part, and `RoadmapList` already owns that behaviour through
`tickRoadmapNodeAction` with `useOptimistic`. **Reuse that action.** Do not write a second
tick path, and do not let a node claim a lesson it does not have.

Put the maths — grouping, ordering, spine-versus-branch, coordinates if you use SVG — in
`graph-layout.ts` as pure functions, and TDD them. The component should be layout plus
markup only. This is the unit's one genuinely testable piece and the brief asks for it.

**Where the toggle shows:** only in the non-DSA branch, and only when
`roadmaps.length > 0`. Areas with no roadmap rows get no toggle rather than an empty
Roadmap view.

## What must not change

- **DSA and competitive branches**: untouched. No toggle, `PatternMap` and `ProblemList` as
  they are.
- **`AreaTabs`**: exactly as it is. It is a bordered container with rounded items, **not**
  pill tags. (The child-topic links further down the page *are* rounded-full pills; those
  are not AreaTabs and are also unchanged.)
- The List view: the parent-topic card grid, the child pills, the search branch
  (`?q=` → `searchArea`), and `RoadmapList` below them. All unchanged.
- `loading.tsx` / `error.tsx` stay shaped like the page.

## Do not touch

`components/library/pattern-map.tsx`, `map-scroller.tsx`, `problem-list.tsx`,
`checkin-panel.tsx` · `library/problem/**` (unit 3) · `library/topic/**` ·
`lib/library/queries.ts` · `app/actions/today.ts` (call `tickRoadmapNodeAction`, do not
edit it) · plus the README's forbidden list.

## Tests

`lib/library/graph-layout.test.ts` — TDD, before the component:

- a flat list of one topic then two subtopics groups into one spine node with two branches
- a subtopic before any topic does not crash and does not vanish
- `hasLesson: false` is marked "soon" and still tickable
- ordering follows `sort`, not the array's incidental order

`e2e/roadmap.spec.ts`:

- On a non-DSA area the toggle shows and **List is default** — the page looks as it does
  today.
- Switching to Roadmap renders the graph; the URL carries `?view=roadmap` and a reload
  keeps it.
- A node with a lesson links to `/library/topic/<slug>`; a "soon" node does not.
- Ticking a node in the Roadmap view persists after a reload.
- **On DSA there is no toggle** and the Pattern Map is still there.

## Traps

- **`RoadmapNode` is not exported.** Export the type; do not copy it into your component.
- A node's `topicSlug` can be null. `hasLesson` is then false — but guard the link anyway
  rather than building `/library/topic/null`.
- `roadmapsFor` takes `(userId, domain)` in that order and is `server-only`.
- `RoadmapList` is a client component using `useOptimistic`; if your graph needs the same,
  read how it does it rather than inventing a second pattern.
- Six text sizes, token colours, borders not shadows. An SVG graph is where hex codes creep
  in — `check:tokens` will catch them and you may not raise the ceiling.
- Mobile first: the graph has to be usable at 390px. A spine that needs horizontal
  scrolling is acceptable if `AreaTabs`'s `overflow-x-auto` pattern is followed; a graph
  that overflows the viewport silently is not.

## Verification

The README's full list. No database check is specific to this unit, but run
`bun run check:tracker` anyway since ticking touches progress. Screenshots at 390px and
1440px, **both toggle states**, plus DSA at 1440px to show it is unchanged.
