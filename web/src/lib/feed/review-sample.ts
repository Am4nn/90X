// Which cards the admin reviews from a draft batch, and what the verdicts mean.
// Stand-in until the feed-logic branch lands; same exports.

export const SAMPLE_SIZE = 20;
export const PASS_AT = 18;

// Tiny seeded PRNG so the same batch always shows the same cards.
function mulberry32(seed: number) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Half the sample (rounded up) is the riskiest cards (lowest `risk`, null
 *  counts as safest), the rest is seeded-random from what's left. */
export function pickReviewSample(cards: { id: string; risk: number | null }[], seed: number, size = SAMPLE_SIZE): string[] {
  const unique = [...new Map(cards.map((c) => [c.id, c])).values()];
  // Sorting by id too makes the result independent of input order.
  const ordered = unique.toSorted((a, b) => (a.risk ?? 1) - (b.risk ?? 1) || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  if (ordered.length <= size) return ordered.map((c) => c.id);

  const riskiest = Math.ceil(size / 2);
  const rest = ordered.slice(riskiest);
  const random = mulberry32(seed);
  for (let i = 0; i < size - riskiest; i++) {
    const j = i + Math.floor(random() * (rest.length - i));
    const picked = rest[j];
    const here = rest[i];
    if (picked && here) [rest[i], rest[j]] = [picked, here];
  }
  return [...ordered.slice(0, riskiest), ...rest.slice(0, size - riskiest)].map((c) => c.id);
}

/** Pending until `size` verdicts are in; pass `size` = the batch's sample
 *  length when the batch is smaller than SAMPLE_SIZE. The pass mark scales
 *  with it: 18 of 20, 9 of 10. */
export function batchVerdict(verdicts: ("good" | "bad")[], size = SAMPLE_SIZE, passAt = PASS_AT): "pending" | "published" | "rejected" {
  if (verdicts.length < size) return "pending";
  const good = verdicts.filter((v) => v === "good").length;
  return good >= Math.ceil((passAt * size) / SAMPLE_SIZE) ? "published" : "rejected";
}
