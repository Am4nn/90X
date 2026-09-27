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
