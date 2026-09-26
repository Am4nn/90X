import pytest
from pydantic import ValidationError

from pipeline import staging
from pipeline.enrich import patterns, topics
from pipeline.normalize import dsa


def test_taxonomy_has_24_patterns_and_connected_map():
    rows, links = topics.dsa_topics()
    slugs = {r["slug"] for r in rows}
    assert len(slugs) == 24
    assert {"prefix-sum", "matrix-grid", "string", "simulation", "segment-tree-fenwick", "design"} <= slugs
    assert all(a in slugs and b in slugs for a, b in links)
    reach, frontier = {"arrays-hashing"}, ["arrays-hashing"]
    while frontier:
        n = frontier.pop()
        for a, b in links:
            if a == n and b not in reach:
                reach.add(b)
                frontier.append(b)
    assert reach == slugs


def test_tags_need_one_to_four_known_techniques():
    patterns.PatternTags(pattern="Prefix Sum", techniques=["prefix-sum", "greedy", "matrix"])
    with pytest.raises(ValidationError):
        patterns.PatternTags(pattern="Prefix Sum", techniques=[])
    with pytest.raises(ValidationError):
        patterns.PatternTags(pattern="Prefix Sum", techniques=["telepathy"])
    with pytest.raises(ValidationError):
        patterns.PatternTags(pattern="Prefix Sum", techniques=["a", "b", "c", "d", "e"])


def test_premium_flag_from_missing_leetcode_content():
    rows = {r["slug"]: r for r in dsa.build_problems(
        {"p": {"questionFrontendId": "1", "questionTitle": "P", "TitleSlug": "p", "content": "", "difficulty": "Easy",
               "category": "Algorithms", "topicTags": "[]", "similarQuestions": "[]", "acRate": "1", "totalAcceptedRaw": "1"},
         "f": {"questionFrontendId": "2", "questionTitle": "F", "TitleSlug": "f", "content": "<p>x</p>", "difficulty": "Easy",
               "category": "Algorithms", "topicTags": "[]", "similarQuestions": "[]", "acRate": "1", "totalAcceptedRaw": "1"}},
        {"p": {"problem_description": "text from another dataset"}}, {}, {}, {})}
    assert rows["p"]["premium"] is True and rows["p"]["statement_md"] == "text from another dataset"
    assert rows["f"]["premium"] is False


def test_only_algorithm_problems_are_tagged(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("""insert into problems (slug, kind, title, difficulty, topic_slugs, statement_md, solutions) values
        ('algo', 'leetcode', 'A', 'Easy', [], 's', '{}'),
        ('swap-salary', 'leetcode', 'Swap Salary', 'Easy', ['sql'], 's', '{}'),
        ('fizz', 'leetcode', 'Fizz Buzz Multithreaded', 'Medium', ['concurrency'], 's', '{}')""")
    assert [r[0] for r in patterns.untagged(con)] == ["algo"]
