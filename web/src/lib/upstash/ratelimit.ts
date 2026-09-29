// Per-user ceilings on the paid AI actions. Pure config and decision, kept
// separate from the Redis wrapper (rate-limit.ts) so it is unit-testable, the
// same way chat-rules.ts sits beside coach/rate-limit.ts.

export type SlotKind = "review" | "mock" | "grade";

/** Matches @upstash/ratelimit's `Duration` (its type is not exported). */
type Window = `${number}${"" | " "}${"ms" | "s" | "m" | "h" | "d"}`;

export const SLOT_LIMITS = {
  // A solution review is the expensive model; ten an hour is generous.
  review: { tokens: 10, window: "1 h" },
  // Mocks are one-at-a-time with a scoring lock, so twenty an hour is a floor.
  mock: { tokens: 20, window: "1 h" },
  // Grading is the fast model, but a wrong-answer flood still spends.
  grade: { tokens: 120, window: "1 h" },
} as const satisfies Record<SlotKind, { tokens: number; window: Window }>;

/**
 * The decision from a limiter's result. `result` is null when the limiter
 * itself failed. `reason` is @upstash/ratelimit's own signal for why the result
 * is what it is; `"timeout"` means it could not reach Redis, which must be a
 * refusal, not a pass. Pure so it is testable without Redis.
 */
export function slotDecision(
  result: { success: boolean; reset?: number; reason?: string } | null,
  now = Date.now(),
): { allowed: boolean; retryAfterSec: number } {
  // Fail closed: a paid action must not run when we cannot meter it. A hung
  // Redis makes @upstash/ratelimit answer success:true with reason "timeout",
  // which is exactly the case that must refuse rather than pass. The coach
  // chat limiter fails open instead, and SECURITY.md records both decisions.
  if (!result || result.reason === "timeout") return { allowed: false, retryAfterSec: 0 };
  if (result.success) return { allowed: true, retryAfterSec: 0 };
  return { allowed: false, retryAfterSec: Math.max(1, Math.ceil(((result.reset ?? now) - now) / 1000)) };
}
