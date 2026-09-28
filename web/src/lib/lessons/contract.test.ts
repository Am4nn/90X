import { describe, expect, it } from "vitest";
import { checkLesson, isInterviewerPrompt, wordCount } from "./contract";

// Ported from `pipeline/tests/test_lessons.py` alongside the contract itself.
// Two copies of a rule need two copies of the cases, or the second copy drifts
// and nobody finds out until a lesson ships.

const GOOD_BODY = `## What it is

A lock keeps two threads from touching one piece of state at the same time. ${"Only one holder at a time, and every other caller waits its turn. ".repeat(20)}

## Why interviewers ask this

Because concurrency is where confident answers go wrong. ${"The candidate who can name the failure mode is the one who has debugged it. ".repeat(12)}

## The core idea

${"Acquire, mutate, release, and never hold two locks in a different order than anybody else does. ".repeat(14)}`;

const OK_FOLLOW_UPS = ["What breaks under load?", "Why does that matter here?", "Compare it with the alternative."];

describe("wordCount", () => {
  it("counts words, not whitespace runs", () => {
    expect(wordCount("  one   two\n\nthree  ")).toBe(3);
    expect(wordCount("")).toBe(0);
  });
});

describe("checkLesson", () => {
  it("passes a lesson that reads like a lesson", () => {
    expect(checkLesson(GOOD_BODY, OK_FOLLOW_UPS)).toEqual([]);
  });

  it("rejects one that is too short", () => {
    expect(checkLesson("Three words only", OK_FOLLOW_UPS).some((p) => p.includes("too short"))).toBe(true);
  });

  it("rejects one that is too long", () => {
    expect(checkLesson("word ".repeat(1500), OK_FOLLOW_UPS).some((p) => p.includes("too long"))).toBe(true);
  });

  it("rejects a reference to source the reader cannot see", () => {
    const problems = checkLesson(`${GOOD_BODY}\n\nAs the passage states, writes are cheap.`, OK_FOLLOW_UPS);
    expect(problems.some((p) => p.includes("cannot see"))).toBe(true);
  });

  it("rejects the lesson talking about itself", () => {
    const problems = checkLesson(`${GOOD_BODY}\n\nAccording to this lesson, locks are cheap.`, OK_FOLLOW_UPS);
    expect(problems.some((p) => p.includes("cannot see"))).toBe(true);
  });

  it("treats a document store as subject matter, not a citation", () => {
    // sd-nosql-types wrote "The document store adds richer queries" and was
    // rejected. Document stores are one of the NoSQL types it is about.
    const body = `${GOOD_BODY}\n\n${"The document store adds richer queries but needs indexes. A document database nests fields inside one record. ".repeat(12)}`;
    expect(checkLesson(body, OK_FOLLOW_UPS)).toEqual([]);
  });

  it("still catches a document being cited", () => {
    expect(
      checkLesson(`${GOOD_BODY}\n\nAccording to the document, writes are cheap.`, OK_FOLLOW_UPS).some((p) => p.includes("cannot see")),
    ).toBe(true);
    expect(
      checkLesson(`${GOOD_BODY}\n\nThe document describes three tradeoffs.`, OK_FOLLOW_UPS).some((p) => p.includes("cannot see")),
    ).toBe(true);
  });

  it("does not read Java generics as HTML", () => {
    // Matching any <word> failed a lesson for writing List<Integer>, which is
    // how Java is written.
    expect(
      checkLesson(`${GOOD_BODY}\n\nA List<Integer> holds boxed values, and Map<String, List<Integer>> nests them.`, OK_FOLLOW_UPS),
    ).toEqual([]);
  });

  it("rejects raw HTML", () => {
    expect(checkLesson(`${GOOD_BODY}\n\n<div class="note">Careful.</div>`, OK_FOLLOW_UPS).some((p) => p.includes("raw HTML"))).toBe(true);
  });

  it("allows angle brackets and URLs inside code", () => {
    expect(checkLesson(`${GOOD_BODY}\n\n\`\`\`\n<div>curl https://example.com</div>\n\`\`\``, OK_FOLLOW_UPS)).toEqual([]);
  });

  it("rejects PDF ligatures", () => {
    expect(checkLesson(`${GOOD_BODY}\n\nThe buﬀer is ﬂushed.`, OK_FOLLOW_UPS).some((p) => p.includes("ligature"))).toBe(true);
  });

  it("rejects a link", () => {
    expect(checkLesson(`${GOOD_BODY}\n\nSee [the docs](https://example.com).`, OK_FOLLOW_UPS).some((p) => p.includes("link"))).toBe(true);
  });

  it("rejects a bare URL on its own line but allows one in prose", () => {
    expect(checkLesson(`${GOOD_BODY}\n\n- https://example.com/a\n`, OK_FOLLOW_UPS).some((p) => p.includes("references"))).toBe(true);
    // The URL shortener lesson was failed three times for writing URLs, which
    // is its entire subject.
    expect(checkLesson(`${GOOD_BODY}\n\nA short key maps to https://example.com/very/long inside the row.`, OK_FOLLOW_UPS)).toEqual([]);
  });

  it("rejects a table", () => {
    expect(checkLesson(`${GOOD_BODY}\n\n| a | b |\n| - | - |\n`, OK_FOLLOW_UPS).some((p) => p.includes("table"))).toBe(true);
  });

  it("rejects a word broken by PDF extraction but allows a hanging hyphen", () => {
    expect(checkLesson(`${GOOD_BODY}\n\nThe cache behaves infor- mally here.`, OK_FOLLOW_UPS).some((p) => p.includes("broken"))).toBe(true);
    // "pre- and post-conditions" is ordinary English.
    expect(checkLesson(`${GOOD_BODY}\n\nIt checks pre- and post-conditions on entry.`, OK_FOLLOW_UPS)).toEqual([]);
  });

  it("reports a broken word on a later call too", () => {
    // BROKEN_WORD is a global regex at module scope; a shared lastIndex would
    // make the second call miss what the first one found.
    const body = `${GOOD_BODY}\n\nThe cache behaves infor- mally here.`;
    expect(checkLesson(body, OK_FOLLOW_UPS).some((p) => p.includes("broken"))).toBe(true);
    expect(checkLesson(body, OK_FOLLOW_UPS).some((p) => p.includes("broken"))).toBe(true);
  });
});

describe("isInterviewerPrompt", () => {
  it("accepts an imperative, because that is what interviewers say", () => {
    expect(isInterviewerPrompt("Walk me through the TLS handshake.")).toBe(true);
  });

  it("accepts a question followed by an instruction", () => {
    expect(isInterviewerPrompt("Can a table violate both 2NF and 3NF at the same time? Give an example.")).toBe(true);
  });

  it("accepts setup before the ask", () => {
    expect(isInterviewerPrompt("Your team has a method with a long chain of instanceof checks. How would you refactor it?")).toBe(true);
    expect(isInterviewerPrompt("Can a NoSQL system with quorum reads be considered CP under CAP? Use Cassandra as an example.")).toBe(true);
    expect(isInterviewerPrompt("Traffic tripled overnight. The cache is cold. What do you look at first?")).toBe(true);
  });

  it("rejects an answer hiding behind a question", () => {
    expect(isInterviewerPrompt("What breaks under load? The lock serializes every request.")).toBe(false);
  });

  it("rejects a statement with no ask at all", () => {
    expect(isInterviewerPrompt("Processes are useful.")).toBe(false);
    expect(isInterviewerPrompt("")).toBe(false);
  });

  it("surfaces the first bad follow-up through checkLesson", () => {
    const problems = checkLesson(GOOD_BODY, ["What is a process?", "Processes are useful.", "Why?"]);
    expect(problems.some((p) => p.includes("interviewer would say"))).toBe(true);
  });
});
