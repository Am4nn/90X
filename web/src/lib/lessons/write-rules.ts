// The parts of writing a lesson that are pure string work: what counts as usable
// source material, whether there is enough of it, and how the model's fields
// become Markdown.
//
// Separate from `./write.ts` because that module is `server-only` (it reaches
// the database, Redis and a model) and Vitest cannot import a server-only
// module. Same split as `coach/chat-rules.ts` beside `coach/model.ts`, and it
// means the gate that enforces the source rule is testable with no vector
// index, no Redis and no model.

import { z } from "zod";

export type Passage = { title: string; text: string; ref: string };

/** A hit below this adds nothing to a lesson. */
const RELEVANCE_FLOOR = 0.3;
/** Two passages is not a lesson's worth of material, however long they are. */
const MIN_PASSAGES = 3;
/** Matches the pipeline's MIN_CONTEXT: under this there is nothing to write from. */
const MIN_CONTEXT_CHARS = 400;
const MAX_CONTEXT_CHARS = 14_000;
export const PASSAGES = 8;

/** A lesson is three model calls. This many a day per user, then it refuses. */
export const LESSONS_PER_DAY = 3;

const FollowUp = z.object({
  question: z.string().min(10).max(300),
  answer: z.string().min(20).max(1200),
});

/** The fields the model fills. We build the Markdown, so every lesson reads the same way. */
export const LessonSchema = z.object({
  title: z.string().min(3).max(120),
  summary: z.string().min(20).max(200),
  whatItIs: z.string().min(60),
  whyAsked: z.string().min(40),
  coreIdea: z.string().min(80),
  keyPoints: z.array(z.string().min(10)).min(3).max(5),
  sixtySecondAnswer: z.string().min(200),
  followUps: z.array(FollowUp).min(3).max(5),
  workedExample: z.string().min(80),
  traps: z.array(z.string().min(10)).min(2).max(4),
});
export type Lesson = z.infer<typeof LessonSchema>;

/** Fewer claims than this is not a fact check. A 700-word lesson has many more,
 *  so an empty or near-empty list means the checker no-opped rather than that
 *  the draft was clean, and the caller must refuse rather than publish. */
export const MIN_CLAIMS_CHECKED = 4;

export const FactCheckSchema = z.object({
  claims: z.array(z.object({ claim: z.string().max(400), supported: z.boolean(), why: z.string().max(300) })).max(20),
});

/**
 * The one place a Coach-written lesson becomes Markdown.
 *
 * A faithful port of `render()` in `pipeline/src/pipeline/lessons/write.py`,
 * headings and order included. It has to be: 273 lessons in the Library already
 * have this shape, and a lesson that opened with a "## What it is" heading and
 * called its bullets "Worth remembering" would read as a different app. The
 * first section deliberately has no heading — the body opens with it — and the
 * follow-up ladder is part of the lesson, with its answers, not just the
 * questions the contract checks.
 */
export function renderLesson(lesson: Lesson): string {
  const ladder = lesson.followUps.map((f) => `**${f.question.trim()}**\n\n${f.answer.trim()}`).join("\n\n");
  return [
    lesson.whatItIs.trim(),
    "## Why interviewers ask this",
    lesson.whyAsked.trim(),
    "## The core idea",
    lesson.coreIdea.trim(),
    "## Key points",
    lesson.keyPoints.map((p) => `- ${p.trim()}`).join("\n"),
    "## Your 60-second answer",
    lesson.sixtySecondAnswer.trim(),
    "## If they dig deeper",
    ladder,
    "## Worked example",
    lesson.workedExample.trim(),
    "## Common traps",
    lesson.traps.map((t) => `- ${t.trim()}`).join("\n"),
  ].join("\n\n");
}

/**
 * Turn vector hits into passages, dropping anything too weak to write from.
 * A missing score is not a low one — the index does not always return one — so
 * only an explicitly low score is rejected.
 */
export function usablePassages(hits: unknown[]): Passage[] {
  const out: Passage[] = [];
  for (const hit of hits) {
    if (typeof hit !== "object" || hit === null) continue;
    const h = hit as { score?: unknown; data?: unknown; metadata?: Record<string, unknown> };
    if (typeof h.score === "number" && h.score < RELEVANCE_FLOOR) continue;
    const text = typeof h.data === "string" ? h.data.trim() : "";
    if (!text) continue;
    const meta = h.metadata ?? {};
    out.push({
      title: typeof meta.title === "string" ? meta.title : "Untitled",
      text,
      ref: typeof meta.source_id === "string" ? meta.source_id : typeof meta.url === "string" ? meta.url : "library",
    });
  }
  return out.slice(0, PASSAGES);
}

/**
 * True when there is genuinely enough downloaded material to write from.
 *
 * This is the source rule in one function. It runs before a single token is
 * generated, and a false here means the Coach says the library does not cover
 * the topic rather than writing it from the model's own memory.
 */
export function enoughToWriteFrom(passages: Passage[]): boolean {
  if (passages.length < MIN_PASSAGES) return false;
  return passages.reduce((n, p) => n + p.text.length, 0) >= MIN_CONTEXT_CHARS;
}

/** The passages as one prompt block, stopping before the context budget. */
export function contextOf(passages: Passage[]): string {
  let used = 0;
  const parts: string[] = [];
  for (const p of passages) {
    const block = `### ${p.title}\n${p.text}`;
    if (used + block.length > MAX_CONTEXT_CHARS) break;
    parts.push(block);
    used += block.length;
  }
  return parts.join("\n\n");
}
