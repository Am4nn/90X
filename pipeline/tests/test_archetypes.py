"""The archetype registry and the budget that assigns format to the writer."""

import pytest

from pipeline.cards import archetypes


def test_47_archetypes_parse():
    reg = archetypes.registry()
    assert len(reg.archetypes) == 47
    ids = [a.id for a in reg.archetypes]
    assert len(ids) == len(set(ids)), "archetype ids must be unique"


def test_eligible_returns_the_documented_sets():
    sql = {a.id for a in archetypes.eligible("sql")}
    assert {"read-query-plan", "isolation-behaviour", "fill-clause", "term-meaning"} <= sql
    # What-breaks-first and estimate are system-design-only; impossible-bound is
    # dsa-only. None of them belongs in SQL.
    assert not {"what-breaks-first", "estimate", "impossible-bound", "api-guarantee"} & sql

    sd = {a.id for a in archetypes.eligible("system_design")}
    assert {"what-breaks-first", "estimate", "api-guarantee", "method-semantics"} <= sd
    assert "read-query-plan" not in sd

    dsa = {a.id for a in archetypes.eligible("dsa")}
    assert {"which-invariant", "impossible-bound", "pattern-signal", "complexity-table"} <= dsa
    assert "what-breaks-first" not in dsa


def test_areas_the_catalogue_does_not_cover_have_no_cards():
    assert archetypes.eligible("behavioral") == []
    assert archetypes.eligible("lld") == []
    assert archetypes.eligible("ai") == []


def test_budget_length_tracks_importance():
    low = archetypes.budget({"domain": "dsa", "importance": 0.5})
    high = archetypes.budget({"domain": "dsa", "importance": 1.0})
    assert len(high) > len(low)
    assert len(low) == archetypes.count_for(0.5)
    assert len(high) == archetypes.count_for(1.0)


def test_budget_never_names_an_ineligible_archetype():
    for area in ("dsa", "system_design", "cs", "java", "sql"):
        allowed = {a.id for a in archetypes.eligible(area)}
        slots = archetypes.budget({"domain": area, "importance": 1.0})
        assert slots, f"{area} should produce a budget"
        assert all(s.archetype in allowed for s in slots), area
        # Every slot's primitive belongs to its archetype.
        by_id = {a.id: a for a in archetypes.eligible(area)}
        assert all(s.primitive in by_id[s.archetype].primitives for s in slots), area


def test_budget_spreads_across_primitives_not_just_pick_one():
    # A short budget used to be almost all pick_one, because the registry lists
    # those archetypes first and the round-robin never reached the rest. The
    # interleaving must keep a 10-card topic spread across primitives.
    from collections import Counter

    for area in ("dsa", "cs", "java", "sql", "system_design"):
        slots = archetypes.budget({"domain": area, "importance": 0.5})
        prims = Counter(s.primitive for s in slots)
        assert len(prims) >= 4, f"{area}: {dict(prims)}"
        top = prims.most_common(1)[0][1]
        assert top <= len(slots) // 2, f"{area}: {dict(prims)}"


def test_the_four_dual_primitive_archetypes_offer_both():
    for aid in ("complexity", "trace-the-value", "estimate", "impossible-bound"):
        assert set(archetypes.by_id(aid).primitives) == {"pick_one", "numeric"}, aid


def test_flash_is_self_rate_and_easy_only():
    flash = archetypes.by_id("flash")
    assert flash.primitives == ("self_rate",)
    assert flash.difficulties == ("Easy",)
    assert not flash.why_step


def test_flash_slots_are_always_easy():
    # A topic with only flash eligible (impossible in practice, but the rule is
    # that a slot landing on flash is Easy whatever the cycle said).
    slots = archetypes.budget({"domain": "dsa", "importance": 0.5})
    for s in slots:
        if s.archetype == "flash":
            assert s.difficulty == "Easy"


def test_shape_of_maps_primitives_and_nothing_else():
    assert archetypes.shape_of("pick_one") == "chosen"
    assert archetypes.shape_of("order") == "ordered"
    assert archetypes.shape_of("match") == "mapping"
    assert archetypes.shape_of("numeric") == "number"
    assert archetypes.shape_of("self_rate") is None
    assert archetypes.shape_of("typed") is None  # a legacy format, not a primitive


def test_options_shape_of_maps_primitives():
    assert archetypes.options_shape_of("pick_one") == "list"
    assert archetypes.options_shape_of("order") == "list"
    assert archetypes.options_shape_of("tap_in_place") == "list"
    assert archetypes.options_shape_of("claim_grid") == "list"
    assert archetypes.options_shape_of("match") == "match"
    assert archetypes.options_shape_of("bucket") == "bucket"
    assert archetypes.options_shape_of("assemble") == "assemble"
    assert archetypes.options_shape_of("grid_toggle") == "grid"
    assert archetypes.options_shape_of("numeric") == "none"
    assert archetypes.options_shape_of("self_rate") == "none"
    assert archetypes.options_shape_of("typed") is None  # legacy, no optionsShape


def test_difficulty_is_not_a_flat_third():
    # The cycle's target mix is Medium-heavy, not Easy/Medium/Hard thirds.
    slots = archetypes.budget({"domain": "system_design", "importance": 1.0})
    from collections import Counter

    counts = Counter(s.difficulty for s in slots)
    assert counts["Medium"] > counts["Easy"], counts
    assert counts["Medium"] > counts["Hard"], counts
    assert counts["Hard"] > 0, "a budget with no Hard target reproduces the too-easy corpus"
