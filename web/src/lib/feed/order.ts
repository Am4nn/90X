// Reading an ordering card's rules. A card stores the constraints it claims
// ("a has to come before b"), not one blessed sequence, so every genuinely correct
// order passes. These helpers say what the rules pin down.

/** The one sequence the rules allow, or null when several orders satisfy them (or none does). */
export function onlyOrder(count: number, constraints: [number, number][]): number[] | null {
  const incoming = Array.from({ length: count }, () => 0);
  const outgoing: number[][] = Array.from({ length: count }, () => []);
  for (const [before, after] of constraints) {
    if (before === after || before < 0 || after < 0 || before >= count || after >= count) return null;
    incoming[after] = (incoming[after] ?? 0) + 1;
    outgoing[before]?.push(after);
  }
  const placed: number[] = [];
  let ready = incoming.flatMap((n, i) => (n === 0 ? [i] : []));
  while (ready.length === 1) {
    const [next] = ready;
    if (next === undefined) break;
    placed.push(next);
    ready = [];
    for (const to of outgoing[next] ?? []) {
      incoming[to] = (incoming[to] ?? 0) - 1;
      if (incoming[to] === 0) ready.push(to);
    }
  }
  return placed.length === count ? placed : null;
}

/** The rules an order broke: each [before, after] pair placed the wrong way round. */
export function brokenRules(order: number[], constraints: [number, number][]): [number, number][] {
  const at = new Map(order.map((item, position) => [item, position]));
  return constraints.filter(([before, after]) => (at.get(before) ?? -1) > (at.get(after) ?? -1));
}

/** Any one sequence that keeps every rule (the smallest index first), or null when the rules contradict. */
export function sampleOrder(count: number, constraints: [number, number][]): number[] | null {
  const incoming = Array.from({ length: count }, () => 0);
  const outgoing: number[][] = Array.from({ length: count }, () => []);
  for (const [before, after] of constraints) {
    if (before === after || before < 0 || after < 0 || before >= count || after >= count) return null;
    incoming[after] = (incoming[after] ?? 0) + 1;
    outgoing[before]?.push(after);
  }
  const ready = incoming.flatMap((n, i) => (n === 0 ? [i] : []));
  const placed: number[] = [];
  while (ready.length > 0) {
    ready.sort((a, b) => a - b);
    const next = ready.shift();
    if (next === undefined) break;
    placed.push(next);
    for (const to of outgoing[next] ?? []) {
      incoming[to] = (incoming[to] ?? 0) - 1;
      if (incoming[to] === 0) ready.push(to);
    }
  }
  return placed.length === count ? placed : null;
}
