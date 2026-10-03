// Reading an ordering card's rules. A card stores the constraints it claims
// ("a has to come before b"), not one blessed sequence, so every genuinely correct
// order passes. These helpers say what the rules pin down.

type Graph = { incoming: number[]; outgoing: number[][] };

/** The rules as a graph, or null when a rule points at the same item or outside the list. */
function graph(count: number, constraints: [number, number][]): Graph | null {
  const incoming = Array.from({ length: count }, () => 0);
  const outgoing: number[][] = Array.from({ length: count }, () => []);
  for (const [before, after] of constraints) {
    if (before === after || before < 0 || after < 0 || before >= count || after >= count) return null;
    incoming[after] = (incoming[after] ?? 0) + 1;
    outgoing[before]?.push(after);
  }
  return { incoming, outgoing };
}

/** Takes items whose rules are all met, smallest first. `unique` stops when more than one is ready. */
function walk(count: number, constraints: [number, number][], unique: boolean): number[] | null {
  const g = graph(count, constraints);
  if (!g) return null;
  const ready = g.incoming.flatMap((n, i) => (n === 0 ? [i] : []));
  const placed: number[] = [];
  const most = unique ? 1 : Number.POSITIVE_INFINITY;
  while (ready.length > 0 && ready.length <= most) {
    ready.sort((a, b) => a - b);
    const next = ready.shift();
    if (next === undefined) break;
    placed.push(next);
    for (const to of g.outgoing[next] ?? []) {
      g.incoming[to] = (g.incoming[to] ?? 0) - 1;
      if (g.incoming[to] === 0) ready.push(to);
    }
  }
  return placed.length === count ? placed : null;
}

/** The one sequence the rules allow, or null when several orders satisfy them (or none does). */
export const onlyOrder = (count: number, constraints: [number, number][]): number[] | null => walk(count, constraints, true);

/** Any one sequence that keeps every rule (the smallest index first), or null when the rules contradict. */
export const sampleOrder = (count: number, constraints: [number, number][]): number[] | null => walk(count, constraints, false);

/** The rules an order broke: each [before, after] pair placed the wrong way round. */
export function brokenRules(order: number[], constraints: [number, number][]): [number, number][] {
  const at = new Map(order.map((item, position) => [item, position]));
  return constraints.filter(([before, after]) => (at.get(before) ?? -1) > (at.get(after) ?? -1));
}
