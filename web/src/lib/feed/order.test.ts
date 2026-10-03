import { describe, expect, it } from "vitest";
import { brokenRules, onlyOrder, sampleOrder } from "./order";

describe("onlyOrder", () => {
  it("returns the sequence a chain of rules pins down", () => {
    expect(
      onlyOrder(3, [
        [0, 1],
        [1, 2],
      ]),
    ).toEqual([0, 1, 2]);
    expect(
      onlyOrder(3, [
        [2, 0],
        [0, 1],
      ]),
    ).toEqual([2, 0, 1]);
  });

  it("is null when several orders satisfy the rules", () => {
    expect(onlyOrder(3, [[0, 1]])).toBeNull();
    expect(onlyOrder(3, [])).toBeNull();
  });

  it("is null for rules that contradict themselves or point outside the list", () => {
    expect(
      onlyOrder(2, [
        [0, 1],
        [1, 0],
      ]),
    ).toBeNull();
    expect(onlyOrder(2, [[0, 5]])).toBeNull();
    expect(onlyOrder(2, [[1, 1]])).toBeNull();
  });
});

describe("brokenRules", () => {
  it("names the pairs placed the wrong way round", () => {
    expect(
      brokenRules(
        [1, 0, 2],
        [
          [0, 1],
          [1, 2],
        ],
      ),
    ).toEqual([[0, 1]]);
  });
  it("is empty for an order that keeps every rule", () => {
    expect(brokenRules([0, 1, 2], [[0, 2]])).toEqual([]);
  });
});

describe("sampleOrder", () => {
  it("returns an order that keeps the rules, smallest index first", () => {
    expect(sampleOrder(3, [[2, 0]])).toEqual([1, 2, 0]);
    expect(sampleOrder(3, [])).toEqual([0, 1, 2]);
  });
  it("is null for rules that contradict", () => {
    expect(
      sampleOrder(2, [
        [0, 1],
        [1, 0],
      ]),
    ).toBeNull();
  });
});
