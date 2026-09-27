import type { Outcome } from "./grade";

// The two things a card cannot work out about its reader (decision 2026-09-28).
//
// "New to me" is always available: the reader is telling us this is their
// first encounter, which no amount of stored progress can infer, because
// topic_progress only knows what they studied inside 90x.
//
// "I already know this" is earned, because it retires a card. The bar is
// proportional: a topic holds 8-12 cards, so an absolute count of ten would
// mean answering nearly all of them before the button appeared, leaving
// nothing to retire and making the feature pointless.

export const DECLARED: Outcome[] = ["new_to_me", "known"];

export const MIN_ACCURACY = 0.8;
export const MIN_ANSWERS = 3;
/** ...and this share of the topic's cards, so the bar scales with topic size. */
export const MIN_SHARE = 1 / 3;

export type TopicRecord = { answers: { outcome: Outcome }[]; cardsInTopic: number };

// A skip counts against you here, unlike in accuracy. Answering three cards
// and skipping five is not evidence that you know the topic; it is evidence
// you avoided most of it. Declarations are still ignored, since they say
// nothing either way.
const isAttempt = (outcome: Outcome) => outcome === "correct" || outcome === "wrong" || outcome === "skipped";

/** Whether the reader has earned the right to retire a card on this topic. */
export function canDeclareKnown({ answers, cardsInTopic }: TopicRecord): boolean {
  const tried = answers.filter((a) => isAttempt(a.outcome));
  if (tried.length < MIN_ANSWERS) return false;
  if (cardsInTopic > 0 && tried.length < Math.ceil(cardsInTopic * MIN_SHARE)) return false;
  const correct = tried.filter((a) => a.outcome === "correct").length;
  return correct / tried.length >= MIN_ACCURACY;
}

/** How many more answers are needed, for the UI to explain the lock. */
export function answersUntilKnown({ answers, cardsInTopic }: TopicRecord): number {
  const graded = answers.filter((a) => isAttempt(a.outcome)).length;
  const needed = Math.max(MIN_ANSWERS, cardsInTopic > 0 ? Math.ceil(cardsInTopic * MIN_SHARE) : 0);
  return Math.max(0, needed - graded);
}
