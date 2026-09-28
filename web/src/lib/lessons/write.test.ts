import { describe, expect, it } from "vitest";
import { checkLesson } from "./contract";
import { enoughToWriteFrom, type Passage, renderLesson, usablePassages } from "./write-rules";

// The source gate and the renderer, without a vector index or a model. These are
// the two pieces that decide whether a lesson gets written at all, so they are
// the two that must be testable on their own.

const hit = (score: number, data: string, metadata: Record<string, unknown> = {}) => ({ score, data, metadata });
const passage = (text: string, ref = "ostep"): Passage => ({ title: "T", text, ref });

describe("usablePassages", () => {
  it("drops hits below the relevance floor", () => {
    const out = usablePassages([hit(0.9, "strong"), hit(0.1, "weak"), hit(0.45, "ok")]);
    expect(out.map((p) => p.text)).toEqual(["strong", "ok"]);
  });

  it("drops hits with no text, however relevant", () => {
    expect(usablePassages([hit(0.99, "   "), { score: 0.99 }, hit(0.99, "real")]).map((p) => p.text)).toEqual(["real"]);
  });

  it("survives junk in the result array", () => {
    expect(usablePassages([null, undefined, 7, "string", hit(0.8, "real")])).toHaveLength(1);
  });

  it("keeps a hit with no score, since a missing score is not a low one", () => {
    expect(usablePassages([{ data: "text", metadata: {} }])).toHaveLength(1);
  });

  it("prefers source_id as the ref and falls back to url, then to library", () => {
    const out = usablePassages([
      hit(0.9, "a", { source_id: "ostep", url: "https://x" }),
      hit(0.9, "b", { url: "https://y" }),
      hit(0.9, "c", {}),
    ]);
    expect(out.map((p) => p.ref)).toEqual(["ostep", "https://y", "library"]);
  });

  it("caps how many passages one write reads", () => {
    expect(usablePassages(Array.from({ length: 30 }, (_, i) => hit(0.9, `p${i}`)))).toHaveLength(8);
  });
});

describe("enoughToWriteFrom", () => {
  it("refuses fewer than three passages, however long", () => {
    expect(enoughToWriteFrom([passage("x".repeat(5000)), passage("y".repeat(5000))])).toBe(false);
  });

  it("refuses three short ones: under 400 characters is not a lesson's worth", () => {
    expect(enoughToWriteFrom([passage("short"), passage("also short"), passage("tiny")])).toBe(false);
  });

  it("accepts three substantial passages", () => {
    expect(enoughToWriteFrom([passage("a".repeat(200)), passage("b".repeat(200)), passage("c".repeat(200))])).toBe(true);
  });

  it("refuses nothing at all, which is the case that matters most", () => {
    expect(enoughToWriteFrom([])).toBe(false);
  });
});

describe("renderLesson", () => {
  const lesson = {
    title: "Bloom filters",
    summary: "A probabilistic set membership test with no false negatives.",
    whatItIs: "A bit array and k hash functions. ".repeat(12),
    whyAsked: "Because it shows whether a candidate can reason about probability under a memory budget. ".repeat(8),
    coreIdea: "Hash the key k times, set those bits, and accept that collisions make a maybe. ".repeat(10),
    keyPoints: ["No false negatives, only false positives", "Sized by expected count and target rate", "Deletion needs a counting variant"],
    sixtySecondAnswer: "A Bloom filter answers is this key present with either no or maybe. ".repeat(9),
    followUps: [
      {
        question: "Your filter reports 30% false positives. How would you bring that down?",
        answer: "More bits or more hashes. ".repeat(4),
      },
      { question: "Can you delete from a Bloom filter?", answer: "Not from a plain one. ".repeat(4) },
      { question: "Compare it with a hash set.", answer: "Constant memory versus exact answers. ".repeat(4) },
    ],
    workedExample: "Sizing for a million keys at a one percent rate needs about 9.6 bits each. ".repeat(6),
    traps: ["Treating a maybe as a yes", "Sizing from current load rather than expected growth"],
  };

  it("builds Markdown that passes the contract the pipeline uses", () => {
    const body = renderLesson(lesson);
    expect(
      checkLesson(
        body,
        lesson.followUps.map((f) => f.question),
      ),
    ).toEqual([]);
  });

  it("renders the same sections, in the same order, as the pipeline's own render", () => {
    // Taken from pipeline/src/pipeline/lessons/write.py. The first section has
    // no heading on purpose: the body opens with it. If this list drifts, a
    // Coach-written lesson reads as a different app from the other 273.
    const body = renderLesson(lesson);
    const order = [
      "## Why interviewers ask this",
      "## The core idea",
      "## Key points",
      "## Your 60-second answer",
      "## If they dig deeper",
      "## Worked example",
      "## Common traps",
    ];
    let at = -1;
    for (const heading of order) {
      const next = body.indexOf(heading);
      expect(next, heading).toBeGreaterThan(at);
      at = next;
    }
    expect(body.startsWith("## ")).toBe(false);
    expect(body.startsWith(lesson.whatItIs.trim().slice(0, 40))).toBe(true);
  });

  it("includes the follow-up ladder with its answers, not just the questions", () => {
    const body = renderLesson(lesson);
    for (const f of lesson.followUps) {
      expect(body).toContain(`**${f.question}**`);
      expect(body).toContain(f.answer.trim());
    }
  });

  it("renders key points and traps as bullets", () => {
    const body = renderLesson(lesson);
    for (const point of lesson.keyPoints) expect(body).toContain(`- ${point}`);
    for (const trap of lesson.traps) expect(body).toContain(`- ${trap}`);
  });
});
