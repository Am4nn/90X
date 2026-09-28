// How much JavaScript a phone downloads before the app runs.
//
//   bun run build && bun run check:bundle
//
// Nothing was watching this. 90x installs to a Home Screen and gets opened on a
// train, and a dependency that quietly adds 200 KB costs a reader seconds on
// every cold start — but it never fails a test, so it lands, and the next one
// lands on top of it. `next build` prints numbers and the log scrolls past.
//
// Two figures, both gzipped because that is what crosses the network:
//
//   the shared bootstrap  every route pays it before rendering anything
//   all client chunks     the ceiling on what any navigation can pull
//
// Deliberately not per route: this version of Next writes no App Router build
// manifest, so per-route client JS cannot be read back without parsing build
// log text, and a number derived from scraped output is worse than no number.
//
// Both ratchet. A run that comes in under fails and asks for the ceiling to be
// lowered, because a ratchet only works if somebody turns it.

import { readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { gzipSync } from "node:zlib";

const WEB = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const NEXT = path.join(WEB, ".next");

// Kilobytes, gzipped. Only ever lowered.
const SHARED_CEILING = 292;
const TOTAL_CEILING = 743;

const gz = (file: string) => {
  try {
    return statSync(file).isFile() ? gzipSync(readFileSync(file)).byteLength : 0;
  } catch {
    return 0;
  }
};
const kb = (bytes: number) => Math.round(bytes / 1024);

let manifest: { rootMainFiles?: string[]; polyfillFiles?: string[] };
try {
  manifest = JSON.parse(readFileSync(path.join(NEXT, "build-manifest.json"), "utf8"));
} catch {
  console.error("\n  No build to measure. Run `bun run build` first.\n");
  process.exit(1);
}

const shared = [...new Set([...(manifest.rootMainFiles ?? []), ...(manifest.polyfillFiles ?? [])])].filter((f) => f.endsWith(".js"));
if (!shared.length) {
  console.error("\n  The build manifest lists no bootstrap files, so this measured nothing.");
  console.error("  Next's manifest shape has changed; fix this check rather than deleting it.\n");
  process.exit(1);
}
const sharedKb = kb(shared.reduce((n, f) => n + gz(path.join(NEXT, f)), 0));

function* jsUnder(dir: string): Generator<string> {
  let entries: string[];
  try {
    entries = readdirSync(dir);
  } catch {
    return;
  }
  for (const entry of entries) {
    const full = path.join(dir, entry);
    if (statSync(full).isDirectory()) yield* jsUnder(full);
    else if (entry.endsWith(".js")) yield full;
  }
}
const chunks = [...jsUnder(path.join(NEXT, "static", "chunks"))];
const totalKb = kb(chunks.reduce((n, f) => n + gz(f), 0));

console.log("\n  JavaScript a cold start downloads, gzipped\n");
console.log(`    shared bootstrap   ${String(sharedKb).padStart(5)} KB   ceiling ${SHARED_CEILING}`);
console.log(`    all client chunks  ${String(totalKb).padStart(5)} KB   ceiling ${TOTAL_CEILING}   (${chunks.length} files)`);

const over = [
  sharedKb > SHARED_CEILING ? `the shared bootstrap is ${sharedKb} KB, over ${SHARED_CEILING}` : null,
  totalKb > TOTAL_CEILING ? `all chunks together are ${totalKb} KB, over ${TOTAL_CEILING}` : null,
].filter(Boolean);
if (over.length) {
  console.log("\n    FAIL");
  for (const f of over) console.log(`          ${f}`);
  console.log("\n    Find what grew before raising a ceiling. A ceiling raised without");
  console.log("    looking is the same as not having one.\n");
  process.exit(1);
}

// Slack is reported, not failed on. The design-token check fails when it finds
// fewer than its ceiling, and that is right for counting discrete things: the
// number is the same on every machine. Bytes are not - gzip and the minifier
// differ enough between a laptop and a CI runner that this measured 292 KB
// locally and 291 in CI, which turned a green build red for nothing. So it asks
// for the ratchet to be turned only when there is real headroom, and never
// fails for being small.
const SLACK = 0.05;
const roomy = [
  sharedKb < Math.floor(SHARED_CEILING * (1 - SLACK)) ? `SHARED_CEILING to ${sharedKb}` : null,
  totalKb < Math.floor(TOTAL_CEILING * (1 - SLACK)) ? `TOTAL_CEILING to ${totalKb}` : null,
].filter(Boolean);
if (roomy.length) {
  console.log(`\n    Well under budget. Lower ${roomy.join(" and ")} so it cannot creep back.`);
}
console.log("\n    ok: the app still fits on a phone.\n");
