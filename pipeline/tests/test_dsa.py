from pipeline.normalize import dsa


def test_pattern_slug():
    assert dsa.pattern_slug("Arrays & Hashing") == "arrays-hashing"
    assert dsa.pattern_slug("Heap / Priority Queue") == "heap-priority-queue"
    assert dsa.pattern_slug("1-D Dynamic Programming") == "1-d-dynamic-programming"


def test_strip_fence():
    assert dsa.strip_fence("\n    ```java\nint x = 1;\n```\n") == "int x = 1;"
    assert dsa.strip_fence("plain") == "plain"


def base_rows():
    kaysss = {
        "two-sum": {"questionFrontendId": "1", "questionTitle": "Two Sum", "TitleSlug": "two-sum",
                    "content": "<p>Given <code>nums</code></p>", "difficulty": "Easy", "acRate": "55.1",
                    "totalAcceptedRaw": "1000", "similarQuestions": "['3sum']", "category": "Algorithms",
                    "topicTags": "['Array', 'Hash Table']"},
        "premium-one": {"questionFrontendId": "2", "questionTitle": "Premium One", "TitleSlug": "premium-one",
                        "content": "", "difficulty": "Medium", "acRate": "40", "totalAcceptedRaw": "5",
                        "similarQuestions": "[]", "category": "Algorithms", "topicTags": "['Graph']"},
        "combine-tables": {"questionFrontendId": "175", "questionTitle": "Combine Two Tables", "TitleSlug": "combine-tables",
                           "content": "<p>SQL</p>", "difficulty": "Easy", "acRate": "70", "totalAcceptedRaw": "9",
                           "similarQuestions": "[]", "category": "Database", "topicTags": "['Database']"},
        "pandas-one": {"questionFrontendId": "9000", "questionTitle": "Pandas", "TitleSlug": "pandas-one",
                       "content": "<p>x</p>", "difficulty": "Easy", "acRate": "1", "totalAcceptedRaw": "1",
                       "similarQuestions": "[]", "category": "pandas", "topicTags": "[]"},
    }
    newfacade = {"two-sum": {"task_id": "two-sum", "problem_description": "Given nums (nf).",
                             "completion": "class Solution: pass", "tags": ["Array", "Hash Table"]}}
    multilang = {"two-sum": {"slug": "two-sum", "content": "Given `nums` (gg).",
                             "java": "```java\nclass S {}\n```", "c++": "```cpp\nint a;\n```",
                             "python": "```python\ndef f(): pass\n```", "javascript": "```javascript\nlet a;\n```"}}
    neetcode = {"two-sum": {"pattern": "Arrays & Hashing", "neetcode150": True, "blind75": True, "video": "KLlXCFG5TnA"}}
    companies = {"two-sum": {"Amazon": 100.0, "Google": 80.5}}
    return kaysss, newfacade, multilang, neetcode, companies


def test_build_problems_joins_sources():
    rows = {r["slug"]: r for r in dsa.build_problems(*base_rows())}
    assert set(rows) == {"two-sum", "premium-one", "combine-tables"}  # pandas dropped

    ts = rows["two-sum"]
    assert ts["lc_number"] == 1 and ts["difficulty"] == "Easy" and ts["kind"] == "leetcode"
    assert ts["statement_md"] == "Given `nums` (gg)."  # greengerong markdown wins
    assert ts["solutions"] == {"java": "class S {}", "cpp": "int a;", "python": "class Solution: pass", "javascript": "let a;"}
    assert ts["pattern_slug"] == "arrays-hashing" and ts["pattern_source"] == "neetcode"
    assert ts["nc150"] and ts["blind75"] and ts["video_id"] == "KLlXCFG5TnA"
    assert ts["companies"] == {"Amazon": 100.0, "Google": 80.5}
    assert ts["tags"] == ["Array", "Hash Table"] and ts["similar_slugs"] == ["3sum"]
    assert ts["ac_rate"] == 55.1 and ts["total_accepted"] == 1000
    assert ts["url"] == "https://leetcode.com/problems/two-sum/"

    assert rows["premium-one"]["statement_md"] is None  # premium: no statement anywhere
    assert rows["premium-one"]["pattern_slug"] is None

    sql = rows["combine-tables"]
    assert sql["topic_slugs"] == ["sql"] and "SQL" in sql["statement_md"]  # HTML converted


def test_rerun_keeps_ai_tags(tmp_path, monkeypatch):
    from pipeline import staging

    con = staging.connect(tmp_path / "s.duckdb")
    monkeypatch.setattr(dsa, "load_kaysss", lambda: base_rows()[0])
    monkeypatch.setattr(dsa, "load_newfacade", lambda: base_rows()[1])
    monkeypatch.setattr(dsa, "load_multilang", lambda: base_rows()[2])
    monkeypatch.setattr(dsa, "load_neetcode", lambda: base_rows()[3])
    monkeypatch.setattr(dsa, "load_companies", lambda: base_rows()[4])
    dsa.run(con)
    con.execute("update problems set pattern_slug = 'graphs', pattern_source = 'ai', techniques = ['bfs'] where slug = 'premium-one'")
    dsa.run(con)
    assert con.execute("select pattern_slug, pattern_source, techniques from problems where slug = 'premium-one'").fetchone() == ("graphs", "ai", ["bfs"])
