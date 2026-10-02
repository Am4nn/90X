"""Retire the pre-Feed-v2 cards from production, keeping every one of them locally.

2,137 published cards have no archetype. They are the corpus from before Feed v2
and `swap` never activates them, so they have been sitting in production as drafts:
inert, not served, but 36% of the rows and a standing invitation to confusion.

Retired in production, kept in staging. In staging they are marked `kept = false`
with a reason rather than deleted, which does two things: a future `rebatch` leaves
them out, so a later publish cannot quietly reinstate them, and every column
survives, so flipping `kept` back is all it takes to bring them home.

Run from `pipeline/`. Dry run unless called with --apply.
"""

import os
import sys

import duckdb
import psycopg
from dotenv import load_dotenv

APPLY = "--apply" in sys.argv
load_dotenv(".env")

LEGACY = "source = 'lesson' and kept = true and status = 'draft' and archetype is null"
REASON = "legacy: no archetype, retired from production 2026-10-03 (kept here for reuse)"

con = duckdb.connect(os.path.abspath("../.data/staging.duckdb"), read_only=not APPLY)
staged = con.execute(f"select count(*) from cards where {LEGACY}").fetchone()[0]
ids = [r[0] for r in con.execute(f"select id from cards where {LEGACY}").fetchall()]

with psycopg.connect(os.environ["DATABASE_URL"], prepare_threshold=None) as pg:
    cur = pg.cursor()
    cur.execute("""select count(*) from public.cards
                   where archetype is null and status = 'draft'""")
    in_prod = cur.fetchone()[0]
    # Nothing live may be touched: the flip put 3,772 archetyped cards in front of
    # readers and this is a cleanup, not a change to what anyone is studying.
    cur.execute("""select count(*) from public.cards
                   where archetype is null and status = 'live'""")
    live_legacy = cur.fetchone()[0]

    print(f"staging: {staged} legacy kept-drafts")
    print(f"production: {in_prod} archetype-null drafts to retire, {live_legacy} live (must be 0)")
    assert live_legacy == 0, "a legacy card is live; stopping rather than changing what readers see"

    if not APPLY:
        print("\ndry run; pass --apply to write")
        raise SystemExit

    cur.execute("""update public.cards set status = 'retired'
                   where archetype is null and status = 'draft'""")
    retired = cur.rowcount
    pg.commit()

    cur.execute("select status, count(*) from public.cards group by 1 order by 2 desc")
    after = cur.fetchall()

con.execute(
    f"update cards set kept = false, reject_reason = ? where {LEGACY}", [REASON]
)
con.commit()
left = con.execute(f"select count(*) from cards where {LEGACY}").fetchone()[0]

print(f"\nretired {retired} in production; staging kept-drafts without an archetype left: {left}")
print("production now:")
for status, n in after:
    print(f"   {n:>6}  {status}")
assert left == 0
# The rows are still here in full - this is the proof.
back = con.execute(
    "select count(*) from cards where reject_reason = ?", [REASON]
).fetchone()[0]
print(f"recoverable locally: {back} rows intact, flip `kept` to bring them back")
