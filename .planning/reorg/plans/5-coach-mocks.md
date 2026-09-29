# Unit 5 — the mock picker and the behavioural empty state

**Branch** `coach-mocks` · **Worktree** `../90X-wt/5` · **Spec** `e2e/mock-picker.spec.ts`
**Brief** `.planning/reorg/coach-mocks.brief.md`

Read `.planning/reorg/plans/README.md` first.

## Scope

Two small, well-defined changes on `/coach/mocks`. Keep everything else — past mocks, the
scores, both forms' submit behaviour and their server action.

1. The design-topic picker becomes a **search input with a dropdown** instead of a wall of
   chips.
2. The behavioural form, when the reader has **no stories**, explains why it needs one
   instead of just refusing.

This is the smallest unit in the wave. Resist making it bigger.

## Files

**Create**
- `web/src/lib/coach/topic-search.ts` + `topic-search.test.ts` — the filter, pure
- `web/e2e/mock-picker.spec.ts`

**Modify**
- `web/src/components/coach/mock-picker.tsx`
- `web/src/app/(app)/coach/mocks/page.tsx` — only if the empty state needs different props

## Reuse, do not rewrite

```
DesignMockForm topics: string[]       @/components/coach/mock-picker   (client)
BehavioralMockForm stories: number    @/components/coach/mock-picker   (client)
  // both use useActionState(startMockAction, {})

startMockAction(_, form)              @/app/actions/mocks  -> FormState
  // design form posts hidden type=design + topic
  // behavioural form posts hidden type=behavioral + topic
  // validates with the `Start` zod schema, calls startMock, redirects to
  // mockThreadHref(mockId, threadId), and revalidates /coach/mocks

designTopics()                        @/lib/coach/mocks    -> string[]
  // system_design topic NAMES, case studies first, then importance, limit 24
startMock(userId, type, topic)        @/lib/coach/mocks
  // REFUSES a topic not in designTopics() or BEHAVIORAL_QUESTIONS
BEHAVIORAL_QUESTIONS                  @/lib/coach/mock-rules
listStories(userId)                   @/lib/coach/stories   // no count query exists;
                                                            // the page uses .length
ChipGroup, Switch                     @/components/chip-group
FormMessage, SubmitButton             @/components/form
EmptyState, button()
```

`chipLabel` in `mock-picker.tsx` strips a leading "Design a/an " from a topic name — the
search dropdown should show that same friendly label while still posting the raw value.

## 1. The searchable picker

Replace **the picker control only**. Everything around it stays:

- A text input filters the topics; a dropdown of matches shows while typing.
- Selecting a match fills the input and **posts exactly the value it posts today** — the
  raw topic name. `startMock` validates the topic against `designTopics()` and refuses
  anything else, so a value mangled by the label-stripping would fail server-side.
- Keep the hidden `topic` field, the `type=design` field, the validation and the action
  untouched.
- The default stays `topics[0]`, so submitting without touching the input behaves as today.
- With no topics at all, the existing `EmptyState` ("No design topics yet") stays.

**Accessibility is the substance of this change, not a finish.** A div that filters a list is
not a picker. Give the input `role="combobox"` with `aria-expanded`, `aria-controls` and
`aria-activedescendant`; the list `role="listbox"` and its rows `role="option"`. Arrow keys
move, Enter selects, Escape closes, and the selection is reachable without a mouse. The
existing `ChipGroup` is a `radiogroup` with a hidden input and is worth reading for how this
codebase wires a custom control to a form.

Put the filter in `lib/coach/topic-search.ts` as a pure function and TDD it. Match on the
**friendly label and the raw name**, case-insensitively — someone typing "url shortener"
should find "Design a URL shortener".

## 2. The behavioural empty state

Today, with no stories, the whole form is **replaced** by an `EmptyState` ("Add a story
first") linking to `/me/stories`. The reader is told what to do but not why, and the form
vanishes. Instead:

- **No stories:** a short explanation — behavioural questions ask for your own examples, so
  a mock has nothing to ask without at least one — and a link to the Story bank. The start
  action is **disabled or parked**, not hidden.
- **Has stories:** start works exactly as today, and the **Story bank link stays visible**
  so stories can be added or edited without leaving the flow.
- Do not change the story bank itself, and do not add a count query — `listStories(id)`
  with `.length` is what the page already does.

Copy: short, plain, second person, no exclamation marks.

## Do not touch

`lib/coach/mocks.ts` — a search helper may live in your new file, not in here ·
`app/actions/mocks.ts` · `lib/coach/mock-rules.ts` · `me/stories/**` and
`components/coach/story-editor.tsx` · `coach/page.tsx` (unit 1b) ·
`components/coach/chat.tsx` (unit 1d) · `coach/mocks/[id]/**` ·
plus the README's forbidden list.

## Tests

`lib/coach/topic-search.test.ts` — TDD, before the component:

- an empty query returns every topic, in the order given
- matching is case-insensitive
- a query matching the stripped label ("url shortener") finds the full name
- a query matching nothing returns an empty list
- the raw value survives the round trip: what the filter returns is what gets posted

`e2e/mock-picker.spec.ts`:

- Typing filters the dropdown; selecting fills the input; submitting starts a design mock
  and lands on the mock thread.
- Keyboard only: arrow down, Enter, and the mock starts.
- Submitting without touching the input still starts a mock with the default topic.
- With no stories, the behavioural section explains why and links to the story bank, and
  the start action does not submit.
- With a story seeded, the behavioural form starts and the story-bank link is still there.
- Past mocks and their scores are still listed.

## Traps

- **`startMock` refuses an unknown topic.** Post the raw name, never the stripped label.
- `startMockAction` **redirects** on success. A Playwright assertion that waits for a
  message on the same page will hang.
- Both forms share `useActionState(startMockAction, {})`; a single `FormState` is shown per
  form. Do not merge them into one form.
- The design chips come from `designTopics()`, which **excludes** `sd-design-case-studies`
  and caps at 24. The search is over that list, not over all topics — do not widen the
  query to make search feel better.
- `BEHAVIORAL_QUESTIONS` is a constant, not a query, and its chips are unchanged.
- No native `select` on desktop — this is exactly the rule the dropdown must respect.
- Six text sizes, token colours, borders not shadows.

## Verification

The README's full list, plus `bun run check:coach-tools`. Screenshots at 390px and 1440px
of the picker closed, the picker open with matches, the behavioural section with no stories,
and with one.
