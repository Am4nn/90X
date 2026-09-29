import { describe, expect, it } from "vitest";
import { SLOT_LIMITS, slotDecision } from "./ratelimit";

describe("slotDecision", () => {
  const now = 1_700_000_000_000;

  it("allows within the window", () => {
    expect(slotDecision({ success: true, reset: now + 60_000 }, now)).toEqual({ allowed: true, retryAfterSec: 0 });
  });

  it("refuses past the window and reports the wait", () => {
    expect(slotDecision({ success: false, reset: now + 60_000 }, now)).toEqual({ allowed: false, retryAfterSec: 60 });
  });

  it("fails closed when the limiter itself failed", () => {
    // A paid action must not run when we cannot meter it (decision, not accident).
    expect(slotDecision(null, now)).toEqual({ allowed: false, retryAfterSec: 0 });
  });

  it("never reports a sub-second retry", () => {
    expect(slotDecision({ success: false, reset: now + 200 }, now).retryAfterSec).toBe(1);
  });
});

describe("SLOT_LIMITS", () => {
  it("has a ceiling for every paid action", () => {
    expect(Object.keys(SLOT_LIMITS).toSorted()).toEqual(["grade", "mock", "review"]);
    for (const kind of Object.values(SLOT_LIMITS)) {
      expect(kind.tokens).toBeGreaterThan(0);
    }
  });
});
