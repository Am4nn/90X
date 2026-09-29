# Me/Coach reorg — everything in one place

This folder is the whole piece of work: the plan, the decision log, the mocks, and the five
implementation briefs. Point a session at **this folder** and it has all the context.

## Rule one

The mocks are **visual references, not final designs**. This is an **add-on**: keep today's
behaviour and features, add and refactor around them, never rewrite a page from scratch. Every
brief opens with the same rule.

## Read in this order

1. **`DECISIONS.md`** — every choice we made, screen by screen, in the words that settled it.
2. **`PLAN.md`** — the strategy, the target information architecture, and the route/file map.
3. **`mocks/index.html`** — the visuals (open in a browser; see below).
4. **`*.brief.md`** — the five implementation briefs, one per branch/PR.

## Viewing the mocks

Open `mocks/index.html` directly, or serve the folder:

```bash
python -m http.server 8777 --directory ".planning/reorg/mocks"
# then http://127.0.0.1:8777/index.html
```

The index is interactive: click a choice per screen, add a note, then **Copy picks + notes**.

## The briefs (build order)

| Order | Brief | Branch | Touches |
|---|---|---|---|
| 1 | `me-coach-reorg.brief.md` | `me-coach-reorg` | shell/nav · Friends · Me · Settings · Coach · Lessons · Today · Ren · chat |
| 2 | `library-roadmap.brief.md` | `library-roadmap` | Library toggle + roadmap graph |
| 3 | `dsa-problem-page.brief.md` | `problem-page` | problem page, LeetCode-first |
| 4 | `plan.brief.md` | `plan-setup` | Plan + Set up |
| 5 | `coach-mocks.brief.md` | `coach-mocks` | mocks picker + behavioural empty state |

Do **1 first** — it changes the shell the others sit inside. Then 2–5 in parallel. The house rules
(how we code, checks, PR format) live in `.planning/briefs/README.md`.

## Scope

**In:** shell/nav, Me, Friends, Settings, Coach, Lessons, Today, Library, the problem page, Plan,
Set up, Coach mocks, and the chat.

**Out:** **Feed** (no changes at all), **Story bank** (keep today's tags and actions).

## In one line

Me stops being a junk drawer; Friends gets its own home (a desktop tab, reached from Me on a
phone); a real Lessons page and a Settings page appear; the Coach's weekly read leads Today;
Library gains a Roadmap view without losing today's; the problem page goes LeetCode-first; Plan
gets a level and a preview; and the coach is **Ren**.
