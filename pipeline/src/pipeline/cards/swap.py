"""The Feed v2 swap: one statement flips new draft cards live and old live cards retired.

Prepared and verified locally, then stopped — the production flip is a human's
(DECISIONS round 5; H-publish-swap.md). The order matters: the flip runs only
after the app is deployed, never before, and it *retires* rather than deletes
so nobody's readiness dial drops — `card_state` rows are left in place.
"""

import psycopg

from . import archetypes

# Retiring every live card would take the areas Feed v2 never reached with it.
# `ai`, `lld` and `behavioral` have no eligible archetype in the catalogue, so
# nothing could regenerate their 980 cards; retiring them would remove 96 topics
# at 0.77-0.81 importance from the Feed to fix a format problem they do not have,
# and DECISIONS round 2 settled that behavioural cards are never retired. They
# stay live in their old format until the catalogue covers them.


def covered_areas() -> list[str]:
    """The areas at least one archetype can write. Derived from the registry, so
    adding `ai` to an archetype's `areas` is all it takes for the next swap to
    retire ai's old cards."""
    return sorted({area for a in archetypes.registry().archetypes for area in a.areas})


def flip(pg: psycopg.Connection, dry_run: bool = True) -> dict:
    """Report (dry-run) or apply the two-step status flip.

    Retiring first and activating second, so a card can never be both live and
    retired mid-transaction; activating only `archetype is not null` so a legacy
    card that never went live stays invisible rather than being revived; and
    retiring only within the areas the catalogue covers, so an area Feed v2 could
    not regenerate keeps the cards it has.
    """
    areas = covered_areas()
    where_retire = """status = 'live' and topic_slug in (
                        select slug from public.topics where domain = any(%s))"""
    cur = pg.cursor()
    cur.execute(f"select count(*) from public.cards where {where_retire}", (areas,))
    retiring = cur.fetchone()[0]
    cur.execute(
        """select count(*) from public.cards
           where archetype is not null and status in ('draft', 'live', 'retired')"""
    )
    activating = cur.fetchone()[0]
    cur.execute(
        """select count(*) from public.cards where status = 'live' and topic_slug in (
             select slug from public.topics where not (domain = any(%s)))""",
        (areas,),
    )
    exempt = cur.fetchone()[0]
    counts = {"retire_live": retiring, "activate_draft_archetyped": activating,
              "kept_live_uncovered_area": exempt, "covered_areas": areas}
    if dry_run:
        return counts
    with pg.transaction():
        cur.execute(f"update public.cards set status = 'retired' where {where_retire}", (areas,))
        # `retired` and `live` as well as `draft`: a regenerated card whose question
        # did not change keeps its id, and publish leaves `status` alone, so it
        # arrives already live. The retire above stands it down, and an activation
        # that looked only at `draft` would leave it retired - the new corpus one
        # card short with no error anywhere. Measured on the real publish: one card
        # in 4,666, which the dry run reported as 4,665 to activate.
        cur.execute(
            """update public.cards set status = 'live'
               where archetype is not null and status in ('draft', 'live', 'retired')"""
        )
    return {"retired": retiring, "activated": activating, "kept_live_uncovered_area": exempt}


def run(url: str, dry_run: bool = True) -> dict:
    with psycopg.connect(url, prepare_threshold=None) as pg:
        return flip(pg, dry_run=dry_run)
