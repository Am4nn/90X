// The structural contract a lesson must pass before it is stored.
//
// A port of `pipeline/src/pipeline/lessons/check.py`. Two copies of a rule is
// normally a smell, and jscpd would flag it if the languages matched — but the
// pipeline is Python and the app is TypeScript, and the alternative was a
// pipeline HTTP endpoint: a new surface and a new deploy target so that a chat
// message could reach a regex. The rules here are pure string work with no
// dependencies, and they are the one gate that must never be skipped, so the
// app owns its own copy.
//
// Every rule exists because the first content pass shipped the opposite: raw
// HTML, PDF ligatures, link tables, book chapters, and cards that referred to
// text the reader never saw. A prompt asking nicely was not enough — the card
// generator already said "no questions about the text itself" and the drafts
// leaked anyway. So the rules are enforced, not requested.
//
// Keep this in step with check.py. The tests are ported alongside it, and a
// change to either side without the other is a bug in whichever moved second.

// "the passage", "the reference solution": the reader cannot see any of it.
// `section`, `text` and `document` need a following verb, because "the section
// of memory" and "the document store" are ordinary subject matter — the bare
// noun rejected a NoSQL lesson for naming the thing it was about, the same
// mistake as reading List<Integer> as markup.
const REFERS_TO_SOURCE =
  /\b(?:the|this|that|above|below)\s+(?:passage|excerpt|snippet|chapter|article|extract|reference\s+solution|given\s+solution|source\s+material)\b|\b(?:this|the)\s+(?:section|text|document)\s+(?:covers|describes|explains|shows|above|below)\b|\b(?:as|which)\s+(?:the\s+)?(?:author|text|passage|article|document)\s+(?:states|says|notes|mentions|explains|writes)\b|\baccording\s+to\s+the\s+(?:passage|text|author|article|section|chapter|document)\b|\b(?:this|the)\s+(?:lesson|write-?up|explainer)\b|\baccording\s+to\s+this\b/i;

// Only real HTML tag names. Matching any <word> read Java generics as markup and
// failed a lesson for writing List<Integer>, which is how you write Java.
const HTML_TAG =
  /<\/?(?:div|span|p|a|img|br|hr|table|thead|tbody|tr|td|th|ul|ol|li|h[1-6]|b|i|u|strong|em|code|pre|blockquote|section|article|nav|header|footer|main|aside|form|input|label|button|select|option|script|style|link|meta|iframe|svg|path|figure|figcaption|details|summary|font|center|small|sup|sub)\b[^<>]*>/i;

const CODE = /```[\s\S]*?```|`[^`]+`/g;
const MARKDOWN_LINK = /\]\(/;
// A reference list is URLs standing alone on their own lines. Counting URLs
// instead failed the URL shortener lesson three times for writing URLs, which is
// the entire subject. Inline examples are prose; a bare line is a citation.
const REFERENCE_LINE = /^[ \t]*[-*]?[ \t]*<?https?:\/\/\S+>?[ \t]*$/m;
const LIGATURE = /[ﬀ-ﬆ]/; // ﬀ ﬁ ﬂ ﬃ ﬄ ﬅ from bad PDF extraction
const PIPE_TABLE = /^[ \t]*\|.*\|[ \t]*$/m;
// "cat  ching" and "infor- mally": PDF text extraction splitting words.
const BROKEN_WORD = /\b[a-z]{2,}-\s+([a-z]{3,})\b/g;
// "pre- and post-conditions" is ordinary English; "infor- mally" is a PDF break.
const CONNECTIVES = new Set(["and", "but", "for", "nor", "the", "then", "with", "not", "yet", "plus", "versus", "post", "pre"]);

export const MIN_WORDS = 250;
export const MAX_WORDS = 1400;

// An interviewer's follow-up is often an instruction, not a question: "Walk me
// through the TLS handshake." is exactly what gets asked. Only verbs that ask
// for output — "suppose" and "consider" would let a bare scene-setter count as
// the whole prompt.
const IMPERATIVE =
  /^(?:walk|explain|describe|compare|contrast|design|sketch|derive|show|tell|give|name|estimate|trace|implement|justify|defend|use|outline|list|propose|argue|critique|identify|rank|prove|quantify|evaluate|state|write)\b/i;

/** Code is where angle brackets and URLs legitimately live. */
function withoutCode(text: string): string {
  return text.replace(CODE, " ");
}

export function wordCount(text: string): number {
  return text.split(/\s+/).filter(Boolean).length;
}

/**
 * True if the follow-up sets up and then asks, and never answers itself.
 *
 * The shape is setup, then asking: statements may lead, and once a sentence
 * prompts, every sentence after it must prompt too. The whole field is rendered
 * as what the interviewer says, and what must never happen is answering it in
 * place — "What breaks under load? The lock serializes every request." hands the
 * reader the answer beside the question. A statement before any prompt cannot do
 * that: there is nothing yet to answer.
 *
 * Testing the whole string rejected "Can a table violate both 2NF and 3NF at the
 * same time? Give an example."; requiring every sentence to be a prompt then
 * rejected "Your team has a method with a long chain of instanceof checks. How
 * would you refactor it?" Both are what interviewers say.
 */
export function isInterviewerPrompt(text: string): boolean {
  const parts = text
    .trim()
    .split(/(?<=[.?!])\s+/)
    .map((p) => p.trim())
    .filter(Boolean);
  const prompts = parts.map((p) => p.endsWith("?") || IMPERATIVE.test(p));
  const first = prompts.indexOf(true);
  if (first === -1) return false;
  return prompts.slice(first).every(Boolean);
}

/** The reasons this lesson is not publishable. Empty means it is. */
export function checkLesson(bodyMd: string, followUps: string[]): string[] {
  const problems: string[] = [];
  const words = wordCount(bodyMd);
  if (words < MIN_WORDS) problems.push(`too short (${words} words, minimum ${MIN_WORDS})`);
  if (words > MAX_WORDS) problems.push(`too long (${words} words, maximum ${MAX_WORDS})`);

  const refers = REFERS_TO_SOURCE.exec(bodyMd);
  if (refers) problems.push(`refers to source the reader cannot see: "${refers[0]}"`);

  const prose = withoutCode(bodyMd);
  const html = HTML_TAG.exec(prose);
  if (html) problems.push(`raw HTML: "${html[0]}"`);
  if (LIGATURE.test(bodyMd)) problems.push("PDF ligature characters");

  const link = MARKDOWN_LINK.exec(prose);
  if (link) problems.push(`contains a link: "${link[0]}"`);
  if (REFERENCE_LINE.test(prose)) problems.push("reads like a list of references, not a lesson");
  if (PIPE_TABLE.test(bodyMd)) problems.push("contains a table");

  // `matchAll` rather than a shared lastIndex: BROKEN_WORD is global and a
  // module-level global regex remembers where it stopped between calls.
  const broken = [...bodyMd.matchAll(BROKEN_WORD)].find((m) => m[1] && !CONNECTIVES.has(m[1]));
  if (broken) problems.push(`word broken by PDF extraction: "${broken[0]}"`);

  const bad = followUps.find((q) => !isInterviewerPrompt(q));
  if (bad !== undefined) problems.push(`follow-up is not something an interviewer would say: "${bad}"`);

  return problems;
}
