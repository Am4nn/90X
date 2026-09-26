import { describe, expect, it } from "vitest";
import { batchVerdict, pickReviewSample } from "./review-sample";

const make = (n: number, risk: (i: number) => number | null = (i) => i / n) =>
  Array.from({ length: n }, (_, i) => ({ id: `c${String(i).padStart(3, "0")}`, risk: risk(i) }));

describe("pickReviewSample", () => {
  it("returns every card when the batch is smaller than the sample", () => {
    expect(pickReviewSample(make(5), 1)).toHaveLength(5);
  });

  it("takes the riskiest half first (lowest risk), then fills the rest", () => {
    const sample = pickReviewSample(make(100), 7);
    expect(sample).toHaveLength(20);
    expect(sample.slice(0, 10)).toEqual(make(10).map((c) => c.id));
    expect(new Set(sample).size).toBe(20);
  });

  it("treats a missing risk as safest", () => {
    const cards = make(30, (i) => (i < 25 ? null : 0.5));
    const sample = pickReviewSample(cards, 3);
    expect(sample.slice(0, 5)).toEqual(["c025", "c026", "c027", "c028", "c029"]);
  });

  it("is stable for a seed and independent of input order", () => {
    const cards = make(100);
    const a = pickReviewSample(cards, 42);
    expect(pickReviewSample([...cards].reverse(), 42)).toEqual(a);
    expect(pickReviewSample(cards, 43)).not.toEqual(a);
  });

  it("never repeats a card that appears twice in the input", () => {
    const cards = make(15);
    expect(pickReviewSample([...cards, ...cards], 1)).toHaveLength(15);
  });
});

describe("batchVerdict", () => {
  const verdicts = (good: number, bad: number) => [...Array<"good">(good).fill("good"), ...Array<"bad">(bad).fill("bad")];

  it("stays pending until the whole sample is reviewed", () => {
    expect(batchVerdict(verdicts(18, 0))).toBe("pending");
  });

  it("publishes at 18 of 20 good and rejects below", () => {
    expect(batchVerdict(verdicts(18, 2))).toBe("published");
    expect(batchVerdict(verdicts(17, 3))).toBe("rejected");
  });

  it("scales the pass mark for a batch smaller than the sample", () => {
    expect(batchVerdict(verdicts(9, 1), 10)).toBe("published");
    expect(batchVerdict(verdicts(8, 2), 10)).toBe("rejected");
  });
});
