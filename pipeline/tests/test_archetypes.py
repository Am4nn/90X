"""The archetype registry and the budget that assigns format to the writer."""

import pytest

from pipeline.cards import archetypes


def test_the_catalogue_parses():
    reg = archetypes.registry()
    # 47 at first release, plus the nine that ai, lld and behavioral needed.
    assert len(reg.archetypes) == 56
    ids = [a.id for a in reg.archetypes]
    assert len(ids) == len(set(ids)), "archetype ids must be unique"
    assert all(set(a.primitives) <= set(reg.shapes) for a in reg.archetypes), \
        "every archetype's primitives must be primitives in the registry"


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


def test_every_area_with_topics_is_covered():
    # These three had no eligible archetype in the first release, which is why
    # 980 of their cards could not be regenerated and 96 topics at 0.77-0.81
    # importance produced nothing. An empty set here means that silently again.
    for area in ("behavioral", "lld", "ai", "dsa", "system_design", "cs", "java", "sql"):
        assert archetypes.eligible(area), f"{area} has no eligible archetype"


def test_the_new_areas_got_the_archetypes_meant_for_them():
    lld = {a.id for a in archetypes.eligible("lld")}
    assert {"which-principle-violated", "responsibility-owner", "class-relationship"} <= lld
    assert not {"read-query-plan", "isolation-behaviour", "estimate"} & lld

    ai = {a.id for a in archetypes.eligible("ai")}
    assert {"which-metric-fits", "data-leak-spotter", "estimate", "impossible-bound"} <= ai
    # ML lessons are conceptual, so nothing that needs a code snippet or a trace.
    assert not {"tap-the-bug", "fill-code-blank", "trace-the-value", "read-query-plan"} & ai

    behavioral = {a.id for a in archetypes.eligible("behavioral")}
    assert {"your-story", "strongest-answer", "star-parts", "answer-critique"} <= behavioral
    # Behavioural questions are about the shape of an answer, never about code.
    assert not {"complexity", "tap-the-bug", "estimate", "fill-code-blank"} & behavioral


def test_compose_is_a_primitive_with_no_answer_shape():
    # A written answer is marked against the card's key points by the existing
    # `gradeWithAi`, so no answer-shape column stores it.
    assert archetypes.shape_of("compose") is None
    assert archetypes.options_shape_of("compose") == "none"
    assert {a.id for a in archetypes.registry().archetypes if "compose" in a.primitives} == {"your-story"}


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


def test_the_round_robin_rotates_so_every_archetype_is_reached():
    """The defect behind the first corpus: 173 cards for `flash`, 1 for
    `pattern-signal`, six archetypes never written.

    A topic gets ~18 slots while an area has 20-41 eligible archetypes, so a
    round-robin that starts at 0 every time hands every topic the same opening
    stretch and never reaches the tail. `start` is what fixes it, and the
    property is that over enough topics each archetype is drawn equally often.
    """
    from collections import Counter

    area = "system_design"
    eligible = archetypes.eligible(area)
    assert len(eligible) > 10, "the test needs more archetypes than a topic has slots"
    topic = {"domain": area, "importance": 0.9}
    per_topic = archetypes.count_for(0.9)
    assert per_topic < len(eligible), "the starvation only happens on a short budget"

    # Without rotation: the tail is never reached, however many topics there are.
    stuck = Counter()
    for _ in range(40):
        stuck.update(slot.archetype for slot in archetypes.budget(topic, 0))
    assert len(stuck) < len(eligible), "expected the unrotated round-robin to starve the tail"

    # With it: every archetype is drawn, and no two differ by more than one pass.
    rotated = Counter()
    start = 0
    for _ in range(40):
        rotated.update(slot.archetype for slot in archetypes.budget(topic, start))
        start += per_topic
    assert len(rotated) == len(eligible), "every eligible archetype must be reached"
    assert max(rotated.values()) - min(rotated.values()) <= 1, dict(rotated)


def test_slot_starts_are_independent_of_which_topics_a_run_writes():
    """A resumed run must assign a topic the same archetypes as a full one.

    The running total is computed over every topic with a lesson, in one
    canonical order, so filtering the run cannot shift the rotation. Two partial
    runs that disagreed would produce a corpus neither would produce alone.
    """
    topic = {"domain": "sql", "importance": 0.8}
    assert archetypes.budget(topic, 7) == archetypes.budget(topic, 7), "the budget must be deterministic"

    # The archetype sequence wraps with the eligible count, so a whole extra lap
    # asks for the same archetypes. The difficulty targets do *not* repeat with
    # it: DIFFICULTY_CYCLE advances once per slot and its period is 5, so the
    # same archetype is deliberately asked at a different difficulty next lap,
    # which is how one archetype ends up spanning Easy, Medium and Hard.
    n = len(archetypes.eligible("sql"))
    ids = lambda start: [slot.archetype for slot in archetypes.budget(topic, start)]
    assert ids(3) == ids(3 + n)
    difficulties = lambda start: [slot.difficulty for slot in archetypes.budget(topic, start)]
    assert difficulties(3) != difficulties(3 + n), \
        "a second lap must vary difficulty, or every card of an archetype has the same one"
