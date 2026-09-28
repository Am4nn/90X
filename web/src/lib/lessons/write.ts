import "server-only";
import { generateText, Output } from "ai";
import { eq, sql } from "drizzle-orm";
import { db } from "@/db";
import { lessons, topics } from "@/db/schema";
import { coachModel, trackCoachUsage } from "@/lib/coach/model";
import { searchKnowledge } from "@/lib/coach/tools-data";
import { key } from "@/lib/upstash/keys";
import { redis } from "@/lib/upstash/redis";
import { checkLesson, MAX_WORDS, MIN_WORDS, wordCount } from "./contract";
import {
  contextOf,
  enoughToWriteFrom,
  FactCheckSchema,
  type Lesson,
  LESSONS_PER_DAY,
  LessonSchema,
  MIN_CLAIMS_CHECKED,
  type Passage,
  PASSAGES,
  renderLesson,
  usablePassages,
} from "./write-rules";

// The Coach writing a lesson for a topic that has none.
//
// The pipeline writes a lesson per topic from the downloaded corpus. A topic it
// could not source stays empty, and new topics reach the taxonomy faster than a
// pipeline run does — so the Coach can be asked something the Library does not
// cover. This writes that lesson instead of answering from the model's memory,
// through the same three gates the pipeline uses:
//
//   1. Material first. `searchKnowledge` queries the vector index over the same
//      corpus the pipeline read. Nothing above the floor means no lesson, and
//      that is checked before a single token is generated.
//   2. The structural contract in `./contract.ts`, ported from the pipeline.
//   3. A fact check by a second call that sees only the passages and has to find
//      each claim in them.
//
// A draft that fails 2 or 3 is not stored and not shown. The Coach then says it
// could not write one, which is a worse answer than a lesson and a much better
// answer than a confident invention — the one failure mode nothing downstream
// can catch, because an invented lesson satisfies every structural rule and
// reads perfectly well.

const DAY_SECONDS = 24 * 60 * 60;

export type WriteResult =
  | { ok: true; topicSlug: string; title: string; words: number }
  | {
      ok: false;
      reason: "no-topic" | "already-written" | "no-source" | "rate-limited" | "contract" | "false-claims" | "failed";
      detail: string;
    };

/**
 * Take one of the day's allowance.
 *
 * Unlike the chat rate limit, a Redis failure here **refuses**. That limiter
 * protects a conversation's pace and letting a message through costs one call;
 * this one is the only thing between a single chat and an unbounded number of
 * three-call lesson writes. And there is always a good fallback: the Coach
 * answers from the lessons that already exist.
 */
async function takeLessonSlot(userId: string): Promise<{ allowed: boolean; used: number }> {
  const k = key("coach", "lesson-writes", userId, new Date().toISOString().slice(0, 10));
  try {
    const used = await redis().incr(k);
    // Expire every time, not only on the first. `incr` creates the key with no
    // TTL, so a failure between the two calls would leave it there forever and
    // lock the user out of writing lessons for good. The key is date-stamped,
    // so refreshing its TTL cannot extend today's window - the TTL is only
    // garbage collection, and setting it twice is cheaper than that bug.
    await redis().expire(k, DAY_SECONDS);
    return { allowed: used <= LESSONS_PER_DAY, used };
  } catch (e) {
    console.error("lesson write allowance unavailable", e);
    return { allowed: false, used: LESSONS_PER_DAY };
  }
}

const SYSTEM = `You write one study lesson for an interview-prep app, from the passages given and nothing else.

Rules that are checked after you answer, so breaking one wastes the attempt:
- Every claim must be supported by the passages. If they do not cover something, leave it out. Do not fill gaps from your own knowledge.
- Never refer to the passages, the text, the document, the article or the source. The reader never sees them. Write as if you know the subject.
- No HTML, no Markdown tables, no links, no URLs on their own line.
- ${MIN_WORDS}-${MAX_WORDS} words for the whole lesson, counting the follow-up answers, which are part of it. Aim for 900.
- Each follow-up is what an interviewer actually says. It may set the scene and then ask, but it must never answer itself.
- Plain prose. Short sentences. No filler and no encouragement.`;

async function generate(userId: string, topicName: string, passages: Passage[]): Promise<Lesson | null> {
  const { model } = await coachModel();
  const prompt = `Topic: ${topicName}\n\nPassages:\n\n${contextOf(passages)}`;
  // Invalid structured output gets one retry, the same as solution review.
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const result = await generateText({ model, system: SYSTEM, prompt, output: Output.object({ schema: LessonSchema }) });
      await trackCoachUsage(userId, "coach.write-lesson", model, result);
      return result.output;
    } catch (e) {
      console.error(`lesson write attempt ${attempt + 1} failed`, e);
    }
  }
  return null;
}

/**
 * A second call that sees the passages and the draft, and nothing else.
 *
 * It is asked to find each claim in the passages, not to judge whether the claim
 * is true. A model asked the second question answers from its own knowledge,
 * which is exactly the failure this module exists to prevent.
 *
 * Returns the unsupported claims, or null for "not checked" — which the caller
 * refuses on. Too few claims counts as not checked: a model that returns an
 * empty list would otherwise pass every draft in silence, and a gate that can
 * no-op is worse than no gate, because it reads as a pass.
 */
async function factCheck(userId: string, bodyMd: string, passages: Passage[]): Promise<string[] | null> {
  const { model } = await coachModel();
  try {
    const result = await generateText({
      model,
      system:
        "You check a draft against source passages. For each substantive factual claim in the draft, say whether the passages support it. " +
        "Supported means the passages state it or directly imply it. Your own knowledge is not evidence: a claim you believe is true but " +
        "cannot find in the passages is unsupported. Ignore phrasing, structure and style.",
      prompt: `Passages:\n\n${contextOf(passages)}\n\n---\n\nDraft:\n\n${bodyMd}`,
      output: Output.object({ schema: FactCheckSchema }),
    });
    await trackCoachUsage(userId, "coach.write-lesson.verify", model, result);
    const { claims } = result.output;
    if (claims.length < MIN_CLAIMS_CHECKED) {
      console.error("lesson fact check returned too few claims to be a check", { claims: claims.length });
      return null;
    }
    return claims.filter((c) => !c.supported).map((c) => `${c.claim} — ${c.why}`);
  } catch (e) {
    console.error("lesson fact check failed", e);
    return null; // Unchecked is not the same as clean; the caller refuses.
  }
}

/**
 * Write a lesson for `topicSlug` if the corpus has the material for one.
 *
 * Refuses rather than overwriting: a topic the pipeline has already written is
 * the pipeline's, and rewriting it here would trade a fact-checked lesson built
 * from the whole corpus for one built from eight passages.
 */
export async function writeLessonOnDemand(userId: string, topicSlug: string, q = db): Promise<WriteResult> {
  const [topic] = await q.select({ slug: topics.slug, name: topics.name }).from(topics).where(eq(topics.slug, topicSlug));
  if (!topic) return { ok: false, reason: "no-topic", detail: `No topic called "${topicSlug}".` };

  const [existing] = await q.select({ slug: lessons.topicSlug }).from(lessons).where(eq(lessons.topicSlug, topicSlug));
  if (existing) return { ok: false, reason: "already-written", detail: `${topic.name} already has a lesson. Read it instead.` };

  // Material before anything else, including before the allowance: a topic with
  // no source should not cost the user one of their three.
  let passages: Passage[];
  try {
    passages = usablePassages(await searchKnowledge(topic.name, PASSAGES));
  } catch (e) {
    console.error("lesson write search failed", e);
    return { ok: false, reason: "failed", detail: "The library search failed, so there was nothing to write from." };
  }
  if (!enoughToWriteFrom(passages))
    return {
      ok: false,
      reason: "no-source",
      detail: `The library has no material on ${topic.name}, so there is nothing to write a lesson from.`,
    };

  const slot = await takeLessonSlot(userId);
  if (!slot.allowed)
    return { ok: false, reason: "rate-limited", detail: `That is ${LESSONS_PER_DAY} written lessons today, which is the limit.` };

  const lesson = await generate(userId, topic.name, passages);
  if (!lesson) return { ok: false, reason: "failed", detail: "Writing the lesson failed twice, so nothing was saved." };

  const bodyMd = renderLesson(lesson);
  const broken = checkLesson(
    bodyMd,
    lesson.followUps.map((f) => f.question),
  );
  if (broken.length) {
    console.error("coach lesson failed the contract", { topicSlug, broken });
    return { ok: false, reason: "contract", detail: `The draft did not pass the lesson rules: ${broken[0]}` };
  }

  const unsupported = await factCheck(userId, bodyMd, passages);
  if (unsupported === null) return { ok: false, reason: "failed", detail: "The draft could not be fact-checked, so it was not saved." };
  if (unsupported.length) {
    console.error("coach lesson had unsupported claims", { topicSlug, unsupported });
    return {
      ok: false,
      reason: "false-claims",
      detail: `${unsupported.length} claim${unsupported.length === 1 ? "" : "s"} in the draft are not in the sources, so it was not saved.`,
    };
  }

  const words = wordCount(bodyMd);
  const stored = await q
    .insert(lessons)
    .values({
      topicSlug,
      title: lesson.title,
      summary: lesson.summary,
      bodyMd,
      practice: {},
      sourceRefs: [...new Set(passages.map((p) => p.ref))],
      words,
      generatedAt: new Date().toISOString(),
      writtenBy: userId,
    })
    // Two chats racing on one topic: the first wins, the second is a no-op
    // rather than a crash on the primary key.
    .onConflictDoNothing()
    .returning({ slug: lessons.topicSlug });
  // Nothing returned means the other chat got there first. Saying "written" then
  // would hand the model this draft's title for a lesson that holds someone
  // else's text, and tell the reader to go and find it.
  if (!stored.length) return { ok: false, reason: "already-written", detail: `${topic.name} already has a lesson. Read it instead.` };
  return { ok: true, topicSlug, title: lesson.title, words };
}

/** Topics with no lesson at all — what the Coach can offer to write. */
export async function topicsWithoutLessons(limit = 10, q = db) {
  return q
    .select({ slug: topics.slug, name: topics.name, domain: topics.domain })
    .from(topics)
    .where(sql`not exists (select 1 from ${lessons} where ${lessons.topicSlug} = ${topics.slug})`)
    .orderBy(topics.sort)
    .limit(limit);
}
