
## Fixed: swap activates only the newest publish

Option 1 above, as recommended. `cards.published_at` (migration
`20261003000025_cards_published_at.sql`, additive and nullable). Every publish stamps each
card it sends with the transaction's `now()`, so one publish is one value, and the swap
activates only cards carrying the newest stamp. A card the newest publish left out keeps an
older stamp and stays retired, however it got that way.

Also: swap now **refuses** to apply when no card carries a stamp (there is no "current
corpus" to activate), and its dry run reports how many retired archetyped cards the stamp is
keeping out, so a surprise shows up there and not in production.

Tested against a real Postgres (`tests/test_swap.py`, local database only, always rolled
back), including the scenario that found this. Against the previous swap it fails by
re-activating three cards it must not: one retired earlier, one never stamped, and a live card
that is no longer sent.

### Rollout order matters

1. Apply the migration to production.
2. `pipeline rebatch && pipeline publish`: stamps every kept card. Until this runs, every
   production row reads `published_at = NULL` and `swap --apply` will refuse.
3. `pipeline swap` (dry run), read `left_retired_not_in_newest_publish`, then `--apply`.

Running `publish` before step 1 fails with `column "published_at" does not exist`, and so do
the `test_publish.py` integration tests that run against `DATABASE_URL`.
