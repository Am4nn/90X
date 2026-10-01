"""The Feed v2 swap: one statement flips new draft cards live and old live cards retired.

Prepared and verified locally, then stopped — the production flip is a human's
(DECISIONS round 5; H-publish-swap.md). The order matters: the flip runs only
after the app is deployed, never before, and it *retires* rather than deletes
so nobody's readiness dial drops — `card_state` rows are left in place.
"""

import psycopg


def flip(pg: psycopg.Connection, dry_run: bool = True) -> dict:
    """Report (dry-run) or apply the two-step status flip.

    Retiring first and activating second, so a card can never be both live and
    retired mid-transaction; activating only `archetype is not null` so a legacy
    card that never went live stays invisible rather than being revived.
    """
    cur = pg.cursor()
    cur.execute("select count(*) from public.cards where status = 'live'")
    retiring = cur.fetchone()[0]
    cur.execute("select count(*) from public.cards where status = 'draft' and archetype is not null")
    activating = cur.fetchone()[0]
    if dry_run:
        return {"retire_live": retiring, "activate_draft_archetyped": activating}
    with pg.transaction():
        cur.execute("update public.cards set status = 'retired' where status = 'live'")
        cur.execute("update public.cards set status = 'live'    where status = 'draft' and archetype is not null")
    return {"retired": retiring, "activated": activating}


def run(url: str, dry_run: bool = True) -> dict:
    with psycopg.connect(url, prepare_threshold=None) as pg:
        return flip(pg, dry_run=dry_run)
