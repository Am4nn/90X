import "server-only";
import { Ratelimit } from "@upstash/ratelimit";
import { redis } from "@/lib/upstash/redis";
import { SLOT_LIMITS, slotDecision, type SlotKind } from "./ratelimit";

/**
 * Takes one slot from a paid action's per-user allowance. The coach chat has
 * its own limiter (lib/coach/rate-limit.ts); this covers solution review, mock
 * scoring and grading, which had no ceiling and so let one account burn the
 * shared monthly budget. Fails closed, unlike the chat limiter: when the meter
 * is down, a paid action is refused rather than run unmetered.
 */
const limiters = new Map<SlotKind, Ratelimit>();

function limiterFor(kind: SlotKind): Ratelimit {
  let limiter = limiters.get(kind);
  if (!limiter) {
    const { tokens, window } = SLOT_LIMITS[kind];
    limiter = new Ratelimit({
      redis: redis(),
      limiter: Ratelimit.slidingWindow(tokens, window),
      prefix: `90x:rl:${kind}`,
    });
    limiters.set(kind, limiter);
  }
  return limiter;
}

export async function takeSlot(userId: string, kind: SlotKind): Promise<{ allowed: boolean; retryAfterSec: number }> {
  try {
    const { success, reset, reason } = await limiterFor(kind).limit(userId);
    return slotDecision({ success, reset, reason });
  } catch (e) {
    console.error(`rate limit unavailable for ${kind}`, e);
    return slotDecision(null);
  }
}
