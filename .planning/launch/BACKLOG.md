# Launch backlog (captured 2026-10-03, verbatim intent from Aman)

Status: **selection and clarifying round only.** No planning, no implementation yet.
Feed v2 MVP is complete. Goal: public launch (LinkedIn post) without exhausting hosting or AI limits.

| # | Item | What I understood | Found in code |
|---|---|---|---|
| 1 | Feed card design | Improve the look of feed cards | designer brief exists: `.planning/feed-v2/CARD-DATA-BRIEF.md` |
| 2 | Recommendation balance | Better mix of the 11 primitives shown to a user | `web/src/lib/feed/service.ts` |
| 3 | Question of the day | One question on Today, same for all users, reusing feed cards, "better than feed" (how: undecided) | new |
| 4 | Per-card feedback | Low-key rating on each card (4 levels: good / normal / bad / should-be-removed); admin sees a simple aggregated view; feeds card curation | admin has `/admin/cards/flagged` today |
| 5 | Public launch hardening | BYOK, free-tier limits, anti-scraping, protect hosting and AI spend | new |
| 6 | One more "hook" feature | Something as sticky as Feed; maybe competitive; decided after the rest | new |
| 7 | Retention loop | Reasons to come back daily (competitive / social) | overlaps 6 and 12 |
| 8 | Coach summary recovery | Once dismissed on mobile Today it cannot be seen again until next week. Keep it reachable from Me and Coach as "weekly digest" | Today page |
| 9 | Remove Roadmaps from UI | Remove List/Roadmap toggle and the roadmap link at the bottom of Library. Keep the data for the agent/topic references | roadmap code in `components/library/*`, `lib/library/roadmap.ts`, `library/page.tsx` L162-192, `lib/tracker/planner.ts` |
| 10 | Library > DSA > Patterns | Layout is ugly on desktop, worse on mobile. Only 24 patterns: expected or split finer? Remove "No toggle on DSA" note | `components/library/pattern-map.tsx`, `library/page.tsx` L88-117 |
| 11 | Admin hardening | Guard before public release so no user or attacker reaches app data | pages gate on `viewer.isAdmin` -> `notFound()`; server DB connection bypasses RLS |
| 12 | Missions on Today | Review how they are generated; why several "read 10 cards" tasks. Choose: fixed daily mission (10 cards) vs AI-directed | `lib/tracker/template.ts`, `planner.ts`; slot types new_problem/review/topic/cards |
| 13 | DSA sheets | Coach gives standard sheet questions at start (basics), plus "give me more" once the day's missions are done. Reference: hynts.in/preparation/dsa-sheets | new; `queueProblems` in `lib/coach/missions.ts` already adds extra problems |
| 14 | XP | Points for missions, feed cards, extra work | new |
| 16 | Remove the x% on answered cards | Grading stays 0 or 1 (no partial credit). Drop the percentage shown after an answer; show right or wrong only | feed answer result UI (`components/feed/primitive/review.tsx`) |
| 17 | Assemble cards reject equivalent answers | Screenshot: 'Assemble the statement that returns x plus one' marks `return 1 + x ;` wrong; key is only `return x + 1 ;`. Commutative orders are correct. | assemble grading (`picked` order) and the gate's `one_answer` verdict |
| 15 | What else before launch? | I suggest additions below | |

## Suggested additions for item 15 (to be accepted or dropped)
- Signup/abuse controls: email verification, rate limits per user and per IP, bot protection on signup.
- Cost monitoring + kill switch: daily AI spend alarm, per-user daily AI cap, global circuit breaker.
- Legal basics: privacy policy, terms, data deletion/export, cookie notice.
- Error and uptime monitoring, plus a backup/restore test for the database.
- Load test of Feed and Today at expected LinkedIn-spike traffic.
- Landing page / logged-out experience for people arriving from the post.
- Share cards (result image/link) so the LinkedIn traffic compounds.
- Analytics (activation, D1/D7 return) so the launch can be judged.
- Support path: where a user reports a problem.
- Mobile/PWA install and push-notification polish.

## Decisions so far
- **Launch gate:** every item above is before the LinkedIn post, including #3, #6, #7, #14.
- **#12 Missions:** hybrid. Weekly AI plan from the coach (one call per active user per week); daily missions come from that plan by fixed rules, no AI call: one "10 cards" mission, due reviews, next problem. Also fixes the duplicate "read 10 cards" missions.
- **#9 Roadmaps:** hide the roadmap UI and toggle (and the link at the bottom of Library); keep roadmap data, planner and coach references.
- **#5 Access:** sign-in required for Feed. No daily card limit for logged-in users. Limits apply to AI features (Coach, compose grading). A few anonymous sample cards (option 2) is acceptable if scraping risk is controlled; to decide at hardening.
- **#5 BYOK:** several providers via the Vercel AI SDK; show the user an estimated monthly cost per provider key.
- **#4 Feedback UX:** Aman will mock it. No mock from me. Four levels good / normal / bad / should-be-removed (names TBD); admin gets a simple aggregated view.
- **#13 DSA sheet:** one curated ~75-problem sheet mapped to the library, plus a "more problems" option once the day's missions are done.
- **#10 Patterns:** measure problems per pattern first, then recommend keep or split. Remove the "No toggle on DSA" note.
- **#3 QOTD:** rule-based pick from the live corpus with admin override; no AI at pick time.
- **#6/#7 Hook:** streaks + XP leagues and a daily shareable result are in; plus a brainstorm round for more ideas.

- **#16 Percent:** no partial credit. Grading stays all-or-nothing; remove the % from the answered card.

- **#17 Assemble equivalents:** confirmed bug by Aman's screenshot (1 + x is correct). Needs a measurement of how many assemble cards have more than one valid order before choosing a fix.

## Proposed order (for Aman to confirm; not a plan)
1. **Safety first (blocks everything public):** #11 admin guard, #5 limits/anti-scrape/BYOK, plus cost kill-switch from the additions list.
2. **Cleanup that is quick and removes known ugliness:** #9 roadmap UI, #10 patterns, #8 coach summary in Me/Coach.
3. **Today foundations:** #12 missions (weekly plan + daily rules), then #14 XP, since missions and feed cards award it.
4. **Feed quality:** #2 balance, #4 feedback, #1 design (design waits on Aman's external designer).
5. **Growth features:** #3 question of the day, #13 DSA sheet, #7/#6 streaks, leagues, share card; brainstorm hook ideas.
6. **Launch checks:** item 15 additions (legal, monitoring, load test, landing page, analytics).

## Still open
- Final names for the 4 feedback levels.
- Which 15 additions to accept.
- Anonymous sample cards: yes or no.

