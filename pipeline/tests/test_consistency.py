"""Reading an area's lessons together.

The fact checker reads one lesson at a time, so it cannot see that two
lessons describe the same mechanism differently. Both look fine alone.
"""

from pipeline.lessons.consistency import claims_of

LESSON = """A tree bin reverts to a list when chains shrink.

## Why interviewers ask this

They want to know if you have read the source.

## Key points

- Treeification needs 8 nodes in a bin and a table of at least 64.
- Removal untreeifies on structure, not on size.

## Worked example

Inserting a ninth key treeifies the bin.

## Common traps

- Believing the threshold is always 6.
"""


def test_claims_are_the_definition_and_the_key_points():
    """Contradictions live in what a lesson asserts, not in its examples."""
    claims = claims_of(LESSON)
    assert claims.startswith("A tree bin reverts to a list when chains shrink.")
    assert "Removal untreeifies on structure, not on size." in claims
    assert "Inserting a ninth key" not in claims, "the worked example is not a claim"
    assert "Believing the threshold" not in claims, "traps are not claims"


def test_a_lesson_without_key_points_still_yields_its_definition():
    assert claims_of("Just an opening line.\n\n## Worked example\n\nStuff.") == "Just an opening line."


def test_findings_survive_an_interrupted_run(tmp_path):
    """A run killed 61 windows of 69 in lost every finding, because they were
    collected in memory and returned at the end - about $2 of model calls for
    nothing, and the same mistake the lesson run was built to avoid."""
    from pipeline import staging
    from pipeline.lessons import consistency

    con = staging.connect(tmp_path / "s.duckdb")
    consistency.save(con, [{
        "domain": "java",
        "topics": ["java-hashmap-internals", "java-concurrenthashmap"],
        "disagreement": "One says a treeified bin never reverts, the other says it untreeifies at six.",
        "correct": "A treeified bin reverts to a list when it shrinks to six entries.",
        "fix": "java-hashmap-internals",
    }])
    back = consistency.stored(con)
    assert len(back) == 1
    assert back[0]["fix"] == "java-hashmap-internals"
    assert back[0]["topics"] == ["java-hashmap-internals", "java-concurrenthashmap"]
    # The same window landing twice must not double the list Aman reads.
    consistency.save(con, back)
    assert len(consistency.stored(con)) == 1
