// Identical constants copied between files. Run with `bun run check:dupes`.
//
// knip does not find these, and it is worth being clear why: knip reports code
// nothing imports. BAND_TEXT was declared four times and used four times, so
// every copy was live and knip was right to say nothing. What went wrong is
// duplication, which is a different question, and nothing was asking it - so a
// palette change meant finding four copies and a fifth would have been free to
// appear.
//
// Deliberately narrow: top-level `const NAME = <one line>;` declarations whose
// value is identical in more than one file. That is the shape every real case
// took, and a narrow check that stays green is worth more than a clever one
// nobody keeps passing.

import { readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "src");
// Only a ratchet can hold: a run that finds fewer should lower this.
const CEILING = 0;

// `const NAME = ...;` at the top level, all on one line. A name has to look like
// a constant - MixedCase or SCREAMING - because `const x = 1` inside a file is
// not the thing being hunted.
const DECL = /^const ([A-Z][A-Za-z0-9_]*) = (.+);$/;
const SKIP = new Set(["pulled"]);

function* files(dir: string): Generator<string> {
  for (const entry of readdirSync(dir)) {
    const full = path.join(dir, entry);
    if (statSync(full).isDirectory()) {
      if (!SKIP.has(entry)) yield* files(full);
    } else if (/\.tsx?$/.test(entry) && !/\.test\.tsx?$/.test(entry)) {
      yield full;
    }
  }
}

const seen = new Map<string, { name: string; where: string[] }>();
for (const file of files(ROOT)) {
  const rel = path.relative(path.join(ROOT, ".."), file).replaceAll("\\", "/");
  for (const line of readFileSync(file, "utf8").split("\n")) {
    const m = DECL.exec(line.trim());
    if (!m) continue;
    const [, name, value] = m;
    // Keyed on the value, not the name: the same list under two names is still
    // one list, and that is how DAY_NAMES and DAY_NAMES_LONG began.
    const key = `${name}=${value!.replace(/\s+/g, " ")}`;
    const hit = seen.get(key) ?? { name: name!, where: [] };
    hit.where.push(rel);
    seen.set(key, hit);
  }
}

const dupes = [...seen.values()].filter((d) => d.where.length > 1);
console.log("\n  duplicated constants\n");
for (const d of dupes) {
  console.log(`    ${d.name}  ×${d.where.length}`);
  for (const w of d.where) console.log(`        ${w}`);
}
if (!dupes.length) console.log("    none");
console.log(`\n    ${String(dupes.length).padStart(4)}  total, ceiling ${CEILING}\n`);

if (dupes.length > CEILING) {
  console.log("    FAIL  Move it somewhere both files can import.\n");
  process.exit(1);
}
if (dupes.length < CEILING) {
  console.log(`    Lower CEILING to ${dupes.length} so it cannot creep back.\n`);
  process.exit(1);
}
console.log("    ok: nothing is written out twice.\n");
