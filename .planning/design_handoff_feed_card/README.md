# Handoff: Feed card (90x)

## Overview
Redesign of the 90x Feed card across all eleven primitives, in both asking and answered states, plus the post-answer side blocks (Why this card, Today + expandable overall report) and per-card feedback (star rating, report). Repo: `Am4nn/90x`. Visual source of truth for tokens: `DESIGN.md` at the repo root ("The Prep Console").

## About the design files
`Feed Card.dc.html` is a **design reference built in HTML**, not production code. Recreate it in the existing `web/` app using its components, tokens and state patterns. Open the file in a browser (keep `support.js` next to it) to click through every card. The logic class at the bottom of the file is readable JS and documents behaviour precisely; treat it as a spec, not as code to paste.

Prototype controls at the top (View, Card picker, "Answer with sample miss", "Answer correctly", "Reset sitting") are review tooling only. Do not ship them.

## Fidelity
High fidelity. Colours, type, spacing, radii and copy are final.

## Global rules (apply to every primitive)
- Phone first; frame designed at 390×844. Desktop at 1240 wide with a 280px side column.
- Tap-to-arm / tap-to-place always works. Drag is an **addition** on match, order, bucket, assemble (see Drag below); never the only way.
- Never mark with colour alone: every right/wrong mark is glyph (✓ / ✗) + word.
- The answered state keeps the question's own shape, marked up. The reader never rebuilds the question from memory.
- Tone: no praise, no scolding. Verdict is "Correct" or "Not quite". No percentage shown on binary verdicts; compose keeps its rubric % ("2 of 3 key points, pass mark 70%").
- Min hit target 44px.

## Card anatomy (top to bottom)
1. **Verdict** (answered only): ✓/✗ ring 28px + "Correct" / "Not quite" / "Skipped" / "New to you — here's the answer" / "Marked as known". Sora 600 22px.
2. **Meta row**: area pill (24px tall, 1px #262B36 border, area colour text) + topic (Manrope 600 13px) left; difficulty right (Manrope 700 12px, #AEB5C2).
3. **Prompt**: Manrope 600 16px/1.5. Fenced code renders as `<pre>` (#0A0C10 bg, 1px #1C2029, radius 10, mono 13px/1.6).
4. **Hint** line (Manrope 500 13px, #7D8594), per primitive, changes with state.
5. **Primitive body** (see below).
6. **Actions** (asking only):
   - Row 1: grid `1fr 2fr`, gap 8: **Skip** (outlined, 1px #262B36, transparent) + **Check answer** (primary #67E8F9 bg, #06222A text; disabled = #141820 bg, #7D8594 text). Height 44, radius 12, Manrope 700 15px.
   - Row 2: centred quiet text links, Manrope 500 13px #7D8594, underline #262B36 offset 4px: "New to me" · "I already know this" (the latter only when the reader has topic history).
   - self_rate: Row 1 is "Missed it" / "Got it" (equal halves); Skip moves into the quiet row.
   - **Skip goes straight to the next card** and increments Today › Skipped. It does not reveal the answer. "New to me" reveals the answer.
7. **Answer** (answered): "ANSWER" eyebrow + text; optional "KEY POINTS" list (12px left rule #262B36). Not shown for tap_in_place (the explanation is inline).
8. **"I already know this"** result: inline prompt "Retire the N unseen cards on {topic} too?" with Retire them / Keep them.
9. **Next card**: primary button. Desktop inside the card; mobile pinned in a bar above the tab nav.

### Footer card (answered, separate card directly below)
Bg #0F1218, 1px #1C2029, radius 14, padding 4px 20px. Two rows, each min-height 56, divided by 1px #1C2029:
- Row 1: "Next review in N days" / "Next review tomorrow" (13px #AEB5C2) left; lesson link right: "{Topic} lesson ›" Manrope 600 13px #67E8F9, no chip. Cards without a lesson: "Source: {name}" 13px #7D8594.
- Row 2: **Rating**: fixed-width label (84px, so stars never shift) + 5 stars (36×44 hit, 22px glyph). Label reads "Rate this card", then Poor / Weak / Fine / Good / Excellent on hover or selection. Star fill by value: 1 #F87171, 2 #FB923C, 3 #FBBF24, 4 #A3E635, 5 #4ADE80; empty stroke #7D8594. Tap selected star again to clear. **Report** link right (#67E8F9 600 13px; "Reported" #7D8594 after sending).
- Report opens an inline single-line textarea (underline 1px #262B36, #67E8F9 on focus, grows to 120px, max 300 chars, placeholder "What's wrong with this card?") with a "Send" text button. After send: "Report sent. This card will be reviewed."

## Why this card + Today
- Why copy: new → "New card on {topic}."; due → "Due for review: you've seen this card before and it's time to recall it again."; weak → "{topic} is one of your weak spots. Another go should help it stick."
- **Desktop**: right column 280px, sticky, always visible: Why this card block, then Today block.
- **Mobile**: shown only after answering, as full blocks below the footer card (Today first, then Why this card). Never between the reader and the question.
- Block style: #0F1218, 1px #1C2029, radius 14, padding 16px 20px. Eyebrow Manrope 700 12px uppercase .06em #7D8594.
- **Today**: 3-col grid of Sora 600 22px number + 13px #7D8594 label: Answered, Correct (%), Skipped. Collapsed view shows only this.
- **Overall report** toggle: pill button below (36px, radius 999, 1px #262B36, Manrope 700 13px) "Overall report ⌄" / "Hide report ⌃" (chevron rotates 180°, .2s). Expanded content sits above the button, border-top 1px #1C2029, sections gap 28:
  - **Lifetime**: Answered, Correct %, Skipped (same style as Today) + one line comparing: "Today is N points above/below your lifetime rate of X%." / "Today matches…" / "No answers yet today."
  - **By area**: per area: dot (8px, area colour) + name (15px), % right (Sora 600 13px); 4px track #1C2029 with area-colour fill and a 1px #7D8594 tick at 70% (pass mark). Header right "Pass mark 70%".
  - **Last 7 days, correct**: 7 bars (56px tall area, radius 3 top), previous days #AEB5C2, today #67E8F9, % and day label under each.
  - Do **not** show total card counts, coverage, due counts or retired counts.

## Primitives — asking / answered

Shared option states: idle (1px #262B36, #0F1218), selected/armed (1px #67E8F9, #0E1E24), right (1px #4ADE80), wrong (1px #F87171), dimmed (1px #1C2029, text #7D8594). Mark line under content: glyph 14px + Manrope 700 12px in mark colour.

1. **pick_one**: 4 option rows (A–D letter badge, 15px text). Answered: right "✓ Correct"; their wrong pick "✗ You chose"; others dimmed. Optional two-step "Now the reason" follow-up on some cards (counts only if both right).
2. **match**: Terms as chips (letter badge + text + grip) in a wrapping row; Meanings as full-width rows with a dashed 26px slot showing the paired letter. Tap term (arms) → tap meaning (pairs); tap paired term to unpair. Answered: one row per term: "You paired …", "Right meaning …" where different, ✓ Right / ✗ Wrong pairing.
3. **order**: "Your order" numbered slots (filled: cyan) + dashed empty slots; "Steps" pool below. Tap appends; tap placed removes. Answered: their order, then "THE WRONG WAY ROUND" list ("X has to come before Y."), then the rules ("Several orders are right. Only these rules are fixed:").
4. **claim_grid**: per statement row: text left, **sliding True/False switch** right (132×44 pill, #0A0C10, 1px #262B36; thumb calc(50%−3px) slides, .24s cubic-bezier(.3,.7,.2,1)). Selected: thumb #0E1E24 + #67E8F9 border, label cyan. Tap selected side again to clear. Hint shows "N of M marked". Answered: same switch frozen at their choice, thumb border green/red, plus "✓ Right" or "✗ Wrong. It's true." under the text. Skipped/new: thumb at the truth, neutral.
5. **bucket**: "To sort" chips + column panels (name Sora 600 16px). Arm item → tap column ("Place here" hint, dashed cyan columns). Answered: columns with each item ✓ Right / ✗ Wrong column. Belongs in X.
6. **self_rate**: no body; Missed it / Got it. Answered shows "You said: …".
7. **tap_in_place**: editor panel (#0A0C10, radius 12) with header bar (file name e.g. `find_max.py`, "N lines", mono 12px #7D8594). Lines 44px tall, 44px gutter with line numbers. Picked: #0E1E24 bg, inset 3px #67E8F9 left bar, cyan number, "Your pick" tag. Answered: right line ✓ in gutter + green bar, with an **inline review comment** directly under it (1px #4ADE80, #0F1218, radius 10, max 300px): "✓ Line 2: the line that makes it wrong[, your pick]" + explanation. Wrong pick: ✗ + red bar + red "Your pick". Other lines #7D8594.
8. **assemble**: build tray (#0A0C10, dashed 52×44 empty slots, fixed prefix/suffix in #141820 grey) + token pool. Tap places/removes. Answered: what they built with ✗ on misplaced pieces, "N pieces are in the wrong place", then "RIGHT" with the full correct line.
9. **grid_toggle — "Lights"**: panel #0A0C10, 1px #1C2029, radius 14, padding 4px 14px 6px. Sticky header row of column names (Sora 600 13px #AEB5C2, centred, nowrap). Each row: label (15px) on its own line, then a cells row `repeat(n, minmax(0,1fr))` with a 1px #1C2029 horizontal rail through the middle. Each cell is a 48px-tall full-width transparent button holding a node:
   - off: 14px ring, 1.5px #262B36, fill #0A0C10
   - on: 22px filled #67E8F9 with halo `0 0 0 6px #0E1E24`
   - grow/shrink transition .18s cubic-bezier(.3,1.4,.5,1)
   - answered right: 22px #4ADE80 with dark ✓; on-but-wrong: 22px #F87171 with dark ✗; missed: 22px dashed #F87171 ring; untouched-correct: 14px ring #1C2029.
   - Row note in red: "Missed O(1)." / "O(log n) shouldn't be on." Legend at bottom uses the same node shapes.
   - No hover dependence.
10. **numeric**: 72px display (Sora 600 32px tabular, #0A0C10, radius 14, border #262B36 → #67E8F9 once typed) with static cyan caret; **on-screen keypad** 3×4 (52px keys, #141820, 1px #1C2029, Sora 600 22px, active bg #1C2029): 1–9, then `.` (if decimals) or `±` (if negatives) or blank, 0, ⌫. Physical keyboard also works (digits, `.`/`,`, Backspace, `-`, Enter = check). Max 8 digits; leading 0 replaced. Hint "Whole numbers only. No minus sign." etc. Answered: display keeps their value with ✓ In range / ✗ Out of range; if wrong, a strip "ANSWER 8 exactly" / "4.17 within 0.05".
11. **compose**: "COVER THESE" rubric box (#141820), textarea (min 140, 300 max, 40 min), counter "n / 300". Grader unavailable → reader self-marks (Missed it / Got it). Answered: their text, then each rubric point ✓ Covered / ✗ Missed, score "N of M key points, pass mark 70%".

## Drag (match, order, bucket, assemble)
Added on top of tap; tap behaviour unchanged.
- Implementation: Pointer Events (not HTML5 DnD). Activate after 6px movement; suppress the click that follows a drag.
- Mouse/pen: whole item drags. Touch: chips/tokens drag from anywhere (`touch-action:none`); long rows (order steps) drag only from the 6-dot grip so the page still scrolls.
- Every draggable shows a 6-dot grip (#7D8594) and `cursor: grab`.
- While dragging: a ghost follows the pointer (#141820, 1px #67E8F9, radius 12, shadow `0 14px 36px rgba(0,0,0,.6)`, rotate −1.5°, scale 1.03); the source fades to .35; every valid target shows a dashed #67E8F9 border, hovered target solid + #0E1E24 fill. Insert position on filled slots/tokens shown as a cyan bar (`box-shadow` −6px). Auto-scroll within 56px of the scroll container edges.
- Drops: term → meaning (replaces existing pair); step/token → slot (insert at index, others shift) or back to pool (remove); bucket item → column or back to "To sort".

## State (per card)
`phase: 'ask'|'result'`, `outcome: {kind:'correct'|'wrong'|'skip'|'new'|'known', score?, cov?, said?}`, response `r: {sel, pairs, armed, seq, v[], place[], ticks{}, text}`, two-step `whyActive/whyPick`, feedback `fbStars, fbHover, fbMode, fbText, fbSent`, drag `drag, dragOver`. Sitting: `today {a, c, s}`; report open flag. Next review: correct → card interval, wrong/new → tomorrow, known → 30 days.

## Design tokens
- Background #0A0C10 · surface #0F1218 · raised #141820 · hairline #1C2029 · strong hairline #262B36
- Text #E6E9EF · secondary #AEB5C2 · muted #7D8594
- Signal #67E8F9 · signal wash #0E1E24 · on-signal #06222A
- Right #4ADE80 · wrong #F87171
- Rating ramp #F87171 #FB923C #FBBF24 #A3E635 #4ADE80
- Areas: DSA #818CF8 · System design #C084FC · Java #FB923C · SQL #F472B6 · CS #2DD4BF · LLD/AI/Behavioural #AEB5C2 (placeholders, use DESIGN.md values if defined)
- Type: Sora (display/numbers 600–700), Manrope (UI 500–700), system mono for code. Sizes 11, 12, 13, 15, 16, 22 (+32 numeric display)
- Radii: 8 (badges), 10 (code, keys), 12 (controls), 14 (cards), 999 (pills)
- Spacing: card padding 20 (desktop content 28/32), stack gaps 8/12/16/20/28

## Assets
No images. Icons are inline SVG: check, cross, chevron, 6-dot grip, star, backspace.

## Files
- `Feed Card.dc.html`: the full prototype (template + logic class with all 22 sample cards in `CARDS`).
- `support.js`: runtime needed to open the prototype locally.
