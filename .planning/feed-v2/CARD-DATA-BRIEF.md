# What a Feed card shows — data brief

For a designer working on the Feed card. This says **what is on screen and what the
reader does with it**. It says nothing about layout, hierarchy or treatment; those
are yours.

## The product

90x is interview preparation. The Feed asks one card at a time, grades the answer,
and schedules when to ask it again. The reader is an engineer preparing for
interviews, usually on a phone, usually in short sittings between other work.

**3,761 cards are live** across eight areas: DSA, system design, LLD, Java, SQL,
CS fundamentals, AI, behavioural.

## Theme

The identity is **"The Prep Console"**: an instrument panel for one job, getting
ready. Dark only. One signal colour that means "this is an action" or "you are
here". Topic and status colours are earned by meaning and never swapped around.
Two typefaces, six text sizes.

The tone matters more than any of that: **the console never cheerleads and never
scolds.** The product grades you and tells you the truth about your readiness, so
there is no praise, no confetti, no streak celebration. A wrong answer shows the
right one plainly and moves on.

Tokens, faces and the full brief are in `DESIGN.md` at the repo root.

## Every card has

- **Topic** — e.g. "Transactions & ACID", and the area it belongs to
- **Difficulty** — Easy, Medium or Hard
- **Prompt** — the question. One sentence to a short paragraph; code snippets appear
  inside it on some cards
- **Why this card** — one line saying why it was served: new, due for review, or
  picked because the topic is weak
- **Three things the reader can always do** — answer, skip to see the answer, or say
  "new to me". On a topic they have history with, also "I already know this"

## After answering, every card shows

- Whether it was right, and a score as a percentage
- The answer, written out
- **The question again, marked up** — their answer beside the right one, in the
  card's own shape (this is new; see the "answered" state for each primitive below)
- When it will next be asked
- Source links, where the card came from

## The eleven primitives

Counts are live cards. Limits are enforced by the pipeline — a card outside them is
rejected before it ever reaches a reader, so these are hard bounds, not guidance.

### 1. pick_one — 1,480 cards
One question, **exactly 4 options**, one is right.
*Reader:* taps one option. *Answered:* right one marked, theirs marked if different.

### 2. match — 406 cards
Two sides: **3–6 terms** on the left, **3–6 meanings** on the right. A one-to-one
pairing.
*Reader:* taps a term to arm it, taps a meaning to lock the pair. Tapping a locked
term unlocks it. **Never drag.** *Answered:* each term with what they paired it to,
and the right meaning where they differ.

### 3. order — 385 cards
**3–6 steps**, to be put in a workable order.
*Reader:* arranges the steps. **Never drag.**
*Important:* the card stores the ordering rules it claims, not one blessed sequence,
so several orders can be right. *Answered:* their order, with the pairs they got the
wrong way round named.

### 4. claim_grid — 334 cards
**3–4 statements**, each marked true or false independently. The question lives in
the statements; the prompt is usually just "Mark each statement as true or false."
*Reader:* sets a verdict per statement. *Answered:* each statement marked right or
wrong.

### 5. bucket — 297 cards
**3–8 items** to be sorted into **2–3 columns**.
*Reader:* taps an item to arm it, taps a column to place it. An item can be moved.
**Never drag.** *Answered:* the columns holding what they put in them, each item
marked, with where a misplaced one belonged.

### 6. self_rate — 224 cards
A question with no options at all. The reader recalls the answer in their head.
*Reader:* "Missed it" or "Got it" — the only primitive the reader grades themselves.
*Answered:* the answer, and what they said.

### 7. tap_in_place — 218 cards
**4–14 lines**, usually a code snippet. One line is the answer — the bug, the
insertion point, the line that fails.
*Reader:* taps a line. *Answered:* the right line marked, theirs marked if different.

### 8. assemble — 181 cards
**4–12 tokens** (words or code fragments) to be built into a line. Some parts may be
pre-placed and fixed.
*Reader:* taps tokens to place them, taps again to take them back. **Never drag.**
*Answered:* what they built, against what was right.

### 9. grid_toggle — 110 cards
A small truth grid: **2–5 rows × 2–3 columns**. Three columns is the hard ceiling —
wider does not fit a phone.
*Reader:* ticks cells. *Answered:* every cell marked, distinguishing "ticked and
shouldn't be" from "not ticked and should be".

### 10. numeric — 98 cards
A question whose answer is a number. Judged against an expected value and a
tolerance. The card knows whether decimals and negatives are allowed.
*Reader:* enters a number. *Answered:* their value against the expected one.

### 11. compose — 28 cards
A written answer, mostly behavioural questions. **3–4 rubric points are shown before
answering**, so the reader knows what to cover. Capped around 300 characters, with a
floor of about 40. Graded by a model against the rubric.
*Reader:* types an answer. *Answered:* each rubric point marked covered or missed.
If the grader is unavailable, the reader marks themselves against the rubric.

## Constraints worth knowing before designing

1. **Phone first.** Most sittings are on a phone. Three columns is the widest
   anything gets; prompts and options are frequently two or three lines, not four
   words.
2. **Tap to place, never drag.** Every arranging primitive works by tapping to arm
   and tapping to place. This is deliberate: drag-and-drop fails on touch and for
   anyone with limited dexterity.
3. **Never mark an answer with colour alone.** A glyph and a word as well, so the
   result reads the same to someone who cannot tell the two colours apart.
4. **Prompts can carry code.** Any primitive may have a fenced snippet in its
   prompt; `tap_in_place` is entirely code.
5. **The answered state matters as much as the asking state.** The miss is where the
   learning is, and the reader should not have to rebuild the question from memory
   to understand what they got wrong.
