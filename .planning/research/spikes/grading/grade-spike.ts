// THROWAWAY spike for .planning/research/2026-09-28-models-leetcode-memory.md. Same 12 cases and prompt as
// web/scripts/check-grading.ts + web/src/lib/feed/grader.ts, but the backend is
// picked by env and every call records latency and billed tokens, including
// DeepSeek's hidden thinking tokens (raw total_tokens - prompt - completion).
//
//   SPIKE_BACKEND=deepseek  DEEPSEEK_API_KEY=...  [SPIKE_MODEL=deepseek-flash] [SPIKE_THINKING=off|on]
//   SPIKE_BACKEND=gateway   AI_GATEWAY_API_KEY=... [SPIKE_MODEL=deepseek/deepseek-v4-flash]
//   SPIKE_BACKEND=jev-gateway AI_GATEWAY_API_KEY=... [SPIKE_MODEL=typesafe-ai/jev] [SPIKE_JEV_THRESHOLD=0.5]
//   SPIKE_BACKEND=jev-direct  TYPESAFE_AI_API_KEY=... [SPIKE_MODEL=jev-latest]
//   SPIKE_REPEATS=3   (runs each case N times to measure consistency)
import { createDeepSeek } from "@ai-sdk/deepseek";
import { createGateway } from "@ai-sdk/gateway";
import { createTypeSafeAi } from "@ai-sdk/typesafe-ai";
import { experimental_evaluate as evaluate, generateText, Output } from "ai";
import { z } from "zod";

const SYSTEM = `You grade short answers in a software-engineering interview practice app.
For each numbered key point, decide whether the candidate's answer clearly covers it.
Be fair: accept paraphrases, synonyms and correct extra detail; don't require exact wording.
Don't give credit for a key point that is only hinted at, contradicted, or wrong.
Return one boolean per key point, in order.`;

const CASES = [
  { prompt: "Why does a HashMap have O(1) average lookup?",
    reference: "Keys are hashed to a bucket index, so a lookup jumps straight to one bucket; with a good hash and resizing, buckets stay short.",
    keyPoints: ["hash function maps the key to a bucket index", "direct access to the bucket, not a scan", "resizing keeps buckets short"],
    answers: [
      { text: "The key's hash picks the bucket directly, and the table grows when it gets full so each bucket holds few entries.", expect: 3 },
      { text: "Because it hashes the key to find the bucket.", expect: 2 },
      { text: "It keeps the keys sorted and does binary search.", expect: 0 },
    ] },
  { prompt: "What does a load balancer's health check do?",
    reference: "It probes each backend periodically and stops routing traffic to ones that fail, adding them back when they recover.",
    keyPoints: ["periodic probe of each backend", "unhealthy backends get no traffic", "recovered backends are added back"],
    answers: [
      { text: "It pings servers every few seconds and takes dead ones out of rotation until they respond again.", expect: 3 },
      { text: "It checks servers.", expect: 1 },
    ] },
  { prompt: "Difference between a process and a thread?",
    reference: "A process has its own address space; threads live inside a process and share its memory, so switching and communicating is cheaper.",
    keyPoints: ["process has its own memory/address space", "threads share the process's memory", "threads are cheaper to create/switch"],
    answers: [
      { text: "Threads share memory within one process; each process is isolated with its own address space. Thread switches are lighter.", expect: 3 },
      { text: "A thread is a small process.", expect: 0 },
    ] },
];

// USD per 1M tokens [in, out]; matches web/src/lib/ai/cost.ts + Jev list price.
const PRICES: Record<string, [number, number]> = {
  "deepseek-flash": [0.3, 1.2], "deepseek/deepseek-v4-flash": [0.3, 1.2],
  "deepseek-v4-pro": [1.32, 3.96], "typesafe-ai/jev": [0.042, 0], "jev-latest": [0.042, 0],
};

const backend = process.env.SPIKE_BACKEND ?? "deepseek";
const repeats = Number(process.env.SPIKE_REPEATS ?? 1);
const threshold = Number(process.env.SPIKE_JEV_THRESHOLD ?? 0.5);
const defaults: Record<string, string> = {
  deepseek: "deepseek-flash", gateway: "deepseek/deepseek-v4-flash", "jev-gateway": "typesafe-ai/jev", "jev-direct": "jev-latest",
};
const modelId = process.env.SPIKE_MODEL ?? defaults[backend];

type Call = { hits: boolean[] | null; ms: number; tokIn: number; tokOut: number; tokHidden: number; probs?: number[]; err?: string };

async function gradeLlm(c: (typeof CASES)[number], answer: string): Promise<Call> {
  const n = c.keyPoints.length;
  const model =
    backend === "deepseek"
      ? createDeepSeek({ apiKey: process.env.DEEPSEEK_API_KEY })(modelId)
      : createGateway({ apiKey: process.env.AI_GATEWAY_API_KEY })(modelId);
  const prompt = [
    `Question:\n${c.prompt}`, `Reference answer:\n${c.reference}`,
    `Key points:\n${c.keyPoints.map((k, i) => `${i + 1}. ${k}`).join("\n")}`, `Candidate's answer:\n${answer}`,
  ].join("\n\n");
  const t0 = performance.now();
  const r = await generateText({
    model, system: SYSTEM, prompt, temperature: 0,
    output: Output.object({ schema: z.object({ hits: z.array(z.boolean()).length(n) }) }),
    providerOptions: process.env.SPIKE_THINKING === "on" ? {} : { deepseek: { thinking: { type: "disabled" } } },
  });
  const ms = performance.now() - t0;
  const raw = (r.usage as { raw?: Record<string, number> }).raw ?? {};
  const tokIn = r.usage.inputTokens ?? 0, tokOut = r.usage.outputTokens ?? 0;
  const total = Number(raw.total_tokens ?? raw.totalTokens ?? r.usage.totalTokens ?? tokIn + tokOut);
  return { hits: r.output.hits, ms, tokIn, tokOut, tokHidden: Math.max(0, total - tokIn - tokOut) };
}

async function gradeJev(c: (typeof CASES)[number], answer: string): Promise<Call> {
  const model =
    backend === "jev-gateway"
      ? createGateway({ apiKey: process.env.AI_GATEWAY_API_KEY }).evaluationModel(modelId)
      : createTypeSafeAi({ apiKey: process.env.TYPESAFE_AI_API_KEY }).evaluationModel(modelId);
  // One Boolean question per key point, all against the same state, one request.
  const questions = Object.fromEntries(
    c.keyPoints.map((k, i) => [`kp${i + 1}`, {
      type: "boolean" as const,
      instructions: `Does the candidate's answer clearly cover this key point: "${k}"? Accept paraphrases and synonyms; not if only hinted at, contradicted or wrong.`,
    }]),
  );
  const t0 = performance.now();
  const r = await evaluate({
    model,
    state: { task: "Grade a short interview-practice answer against key points.", question: c.prompt, referenceAnswer: c.reference, candidateAnswer: answer },
    questions,
  });
  const ms = performance.now() - t0;
  const probs = c.keyPoints.map((_, i) => (r.answers as Record<string, { probability: number }>)[`kp${i + 1}`].probability);
  return { hits: probs.map((p) => p >= threshold), probs, ms, tokIn: r.usage?.inputTokens ?? 0, tokOut: r.usage?.outputTokens ?? 0, tokHidden: 0 };
}

const grade = backend.startsWith("jev") ? gradeJev : gradeLlm;
const [pin, pout] = PRICES[modelId] ?? [1, 5];
let off = 0, total = 0, unstable = 0;
const all: Call[] = [];
console.log(`backend=${backend} model=${modelId} repeats=${repeats}`);
for (const c of CASES) for (const a of c.answers) {
  const runs: Call[] = [];
  for (let k = 0; k < repeats; k++) {
    try { runs.push(await grade(c, a.text)); }
    catch (e) { runs.push({ hits: null, ms: 0, tokIn: 0, tokOut: 0, tokHidden: 0, err: String((e as Error).message ?? e).slice(0, 200) }); }
  }
  all.push(...runs);
  const counts = runs.map((r) => (r.hits ? r.hits.filter(Boolean).length : "err"));
  if (new Set(counts.map(String)).size > 1) unstable++;
  const got = counts[0];
  total++;
  const ok = typeof got === "number" && Math.abs(got - a.expect) <= 1;
  const exact = typeof got === "number" && got === a.expect;
  if (!ok) off++;
  const r0 = runs[0];
  console.log(`${ok ? (exact ? "ok= " : "ok~ ") : "FAIL"} ${counts.join(",")}/${c.keyPoints.length} exp ${a.expect}  ${r0.ms.toFixed(0)}ms in=${r0.tokIn} out=${r0.tokOut} hidden=${r0.tokHidden}${r0.probs ? " p=" + r0.probs.map((p) => p.toFixed(2)).join("/") : ""}${r0.err ? " ERR " + r0.err : ""}  ${a.text.slice(0, 40)}`);
}
const good = all.filter((r) => !r.err);
const sum = (f: (r: Call) => number) => good.reduce((s, r) => s + f(r), 0);
const ms = good.map((r) => r.ms).sort((x, y) => x - y);
const cost = (sum((r) => r.tokIn) * pin + sum((r) => r.tokOut + r.tokHidden) * pout) / 1e6;
console.log(`\n${total - off}/${total} within one key point; ${unstable} cases changed across ${repeats} repeats; errors ${all.length - good.length}/${all.length}`);
if (good.length) console.log(`p50 ${ms[Math.floor(ms.length / 2)].toFixed(0)}ms p90 ${ms[Math.floor(ms.length * 0.9)].toFixed(0)}ms | avg in ${(sum((r) => r.tokIn) / good.length).toFixed(0)} out ${(sum((r) => r.tokOut) / good.length).toFixed(0)} hidden ${(sum((r) => r.tokHidden) / good.length).toFixed(0)} | $${(cost / good.length).toFixed(7)}/grade, x7500/mo = $${((cost / good.length) * 7500).toFixed(3)}`);
