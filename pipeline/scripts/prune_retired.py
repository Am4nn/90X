"""Delete retired cards from production that nothing points at, after backing them up.

Retired cards accumulate: the old corpus, each refile that did not fit, each legacy
card. They are not served, but they sit in `public.cards`, keep their batches
visible in the admin as "Draft", and are the rows the swap's `status in (draft, live,
retired)` can resurrect.

What is deleted: a retired card with **no history anywhere** - no review, no
scheduling state, no flag, no admin verdict. The four tables that reference a card
all `ON DELETE CASCADE`, so deleting a card that has history deletes the history
too. Those cards are left alone; this script never cascades.

Then any batch left with no cards at all.

Why the backup comes first and is verified: 103 of the cards this removes exist
nowhere else - they predate the staging database. "Kept locally" is only true if
this writes them out. The full row of every card is written as JSON, and the file is
read back and checked card by card before a single delete is issued.

The delete runs in one transaction and commits only if every count is exactly what
was planned and nothing else moved: the live cards, the reviews, the scheduling
state. Any mismatch rolls the whole thing back.

Run from `pipeline/`. Dry run unless called with --apply.
"""

import json
import os
import sys

import psycopg
from dotenv import load_dotenv

APPLY = "--apply" in sys.argv
BACKUP = os.path.abspath("../.data/review/prod-retired-cards.jsonl")

load_dotenv(".env")

# No history anywhere. Each of these four references public.cards ON DELETE CASCADE.
NO_HISTORY = """
    c.status = 'retired'
    and not exists (select 1 from public.card_reviews r where r.card_id = c.id)
    and not exists (select 1 from public.card_state s where s.card_id = c.id)
    and not exists (select 1 from public.card_flags f where f.card_id = c.id)
    and not exists (select 1 from public.batch_review_items i where i.card_id = c.id)
"""

WATCHED = {
    "live cards": "select count(*) from public.cards where status = 'live'",
    "draft cards": "select count(*) from public.cards where status = 'draft'",
    "reviews": "select count(*) from public.card_reviews",
    "card state": "select count(*) from public.card_state",
    "flags": "select count(*) from public.card_flags",
    "admin verdicts": "select count(*) from public.batch_review_items",
}


def snapshot(cur) -> dict[str, int]:
    out = {}
    for name, sql in WATCHED.items():
        cur.execute(sql)
        out[name] = cur.fetchone()[0]
    return out


def main() -> None:
    with psycopg.connect(os.environ["DATABASE_URL"], prepare_threshold=None) as pg:
        cur = pg.cursor()
        cur.execute(f"select c.id::text from public.cards c where {NO_HISTORY} order by c.id")
        ids = [r[0] for r in cur.fetchall()]
        cur.execute("select count(*) from public.cards where status = 'retired'")
        retired_total = cur.fetchone()[0]
        before = snapshot(cur)

        print(f"retired cards: {retired_total}; with no history, to delete: {len(ids)}; "
              f"kept because they carry history: {retired_total - len(ids)}")
        print("before:", before)

        if not APPLY:
            print("\ndry run; pass --apply to back up, then delete")
            return

        # 1. Back up the full rows, then read the file back and check it.
        cur.execute(f"select c.id::text, to_jsonb(c) from public.cards c where {NO_HISTORY} order by c.id")
        rows = cur.fetchall()
        assert [r[0] for r in rows] == ids, "the set changed between reading ids and reading rows"
        os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
        with open(BACKUP, "w", encoding="utf-8") as fh:
            for _, row in rows:
                fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
        with open(BACKUP, encoding="utf-8") as fh:
            back = [json.loads(line) for line in fh]
        assert len(back) == len(ids), f"backup has {len(back)} rows, expected {len(ids)}"
        assert {b["id"] for b in back} == set(ids), "backup is missing cards"
        assert all(b.get("prompt_md") is not None for b in back), "a backed-up card has no prompt"
        print(f"backed up and re-read {len(back)} cards -> {BACKUP}")

        # 2. Delete, in one transaction, re-checking the history predicate at delete time.
        try:
            cur.execute(
                f"delete from public.cards c where c.id = any(%s::uuid[]) and {NO_HISTORY}",
                (ids,),
            )
            assert cur.rowcount == len(ids), f"deleted {cur.rowcount}, planned {len(ids)}"

            cur.execute(
                "delete from public.card_batches b where not exists "
                "(select 1 from public.cards c where c.batch_id = b.id)"
            )
            batches_removed = cur.rowcount

            after = snapshot(cur)
            for name in WATCHED:
                assert after[name] == before[name], f"{name} moved: {before[name]} -> {after[name]}"
            cur.execute("select count(*) from public.cards where status = 'retired'")
            assert cur.fetchone()[0] == retired_total - len(ids), "retired count is not what was planned"
            # Every remaining card still has a batch to sit in.
            cur.execute("select count(*) from public.cards c where c.batch_id is not null and not exists "
                        "(select 1 from public.card_batches b where b.id = c.batch_id)")
            assert cur.fetchone()[0] == 0, "a card lost its batch"
        except Exception:
            pg.rollback()
            print("ROLLED BACK; nothing was deleted")
            raise
        pg.commit()

        cur.execute("select status, count(*) from public.card_batches group by 1 order by 2 desc")
        batches = cur.fetchall()
        cur.execute("select status, count(*) from public.cards group by 1 order by 2 desc")
        print(f"\ndeleted {len(ids)} cards and {batches_removed} empty batches")
        print("watched counts unchanged:", after)
        print("cards now:", cur.fetchall())
        print("batches now:", batches)


if __name__ == "__main__":
    main()
