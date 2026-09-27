import { describe, expect, it } from "vitest";
import { answersUntilKnown, canDeclareKnown } from "./declare";

const answers = (correct: number, wrong = 0) => [
  ...Array.from({ length: correct }, () => ({ outcome: "correct" as const })),
  ...Array.from({ length: wrong }, () => ({ outcome: "wrong" as const })),
];

describe("canDeclareKnown", () => {
  it("needs a third of the topic's cards, not a fixed count", () => {
    // A topic holds 8-12 cards. Requiring ten answers would mean answering
    // nearly every card before the button appears, leaving nothing to retire.
    expect(canDeclareKnown({ answers: answers(4), cardsInTopic: 12 })).toBe(true);
    expect(canDeclareKnown({ answers: answers(3), cardsInTopic: 12 })).toBe(false);
    expect(canDeclareKnown({ answers: answers(3), cardsInTopic: 8 })).toBe(true);
  });

  it("never fires on one lucky answer", () => {
    expect(canDeclareKnown({ answers: answers(1), cardsInTopic: 3 })).toBe(false);
    expect(canDeclareKnown({ answers: answers(2), cardsInTopic: 3 })).toBe(false);
  });

  it("holds the accuracy bar", () => {
    expect(canDeclareKnown({ answers: answers(4, 1), cardsInTopic: 9 })).toBe(true);
    expect(canDeclareKnown({ answers: answers(3, 2), cardsInTopic: 9 })).toBe(false);
  });

  it("ignores declarations, which are not evidence", () => {
    const declared = [...answers(3), { outcome: "new_to_me" as const }, { outcome: "known" as const }];
    expect(canDeclareKnown({ answers: declared, cardsInTopic: 8 })).toBe(true);
    // Declarations alone can never unlock it.
    expect(canDeclareKnown({ answers: [{ outcome: "new_to_me" }, { outcome: "known" }], cardsInTopic: 3 })).toBe(false);
  });

  it("holds a skip against you", () => {
    // Answering three and skipping five is not evidence you know the topic,
    // it is evidence you avoided most of it.
    const avoided = [...answers(3), ...Array.from({ length: 5 }, () => ({ outcome: "skipped" as const }))];
    expect(canDeclareKnown({ answers: avoided, cardsInTopic: 8 })).toBe(false);
    // One skip among four clean answers still clears 80%.
    expect(canDeclareKnown({ answers: [...answers(4), { outcome: "skipped" }], cardsInTopic: 8 })).toBe(true);
  });

  it("says how many answers are still needed", () => {
    expect(answersUntilKnown({ answers: answers(1), cardsInTopic: 12 })).toBe(3);
    expect(answersUntilKnown({ answers: answers(4), cardsInTopic: 12 })).toBe(0);
  });
});
