import yaml
import pytest

from pipeline import staging
from pipeline.enrich import topic_lists


class FakeLLM:
    def __init__(self, reply):
        self.reply, self.calls = reply, []

    def complete_json(self, system, user, schema, tier="fast", purpose=""):
        self.calls.append({"user": user, "tier": tier, "purpose": purpose})
        return schema(**self.reply(user) if callable(self.reply) else self.reply)


DRAFT = {"topics": [
    {"name": "Caching", "parent": None, "importance": 0.9, "description": "Cache layers and eviction"},
    {"name": "Cache eviction policies", "parent": "Caching", "importance": 0.7, "description": "LRU, LFU"},
    {"name": "Load balancing", "parent": None, "importance": 0.8, "description": "Spreading traffic"},
]}


def seed(con):
    con.execute("""insert into documents (id, domain, title, body_md, sort) values
        ('d1', 'system_design', 'Caching', 'body about caching', 0),
        ('d2', 'system_design', 'Caching › LRU', 'least recently used', 1),
        ('d3', 'system_design', 'Load balancer', 'round robin', 2),
        ('d4', 'system_design', 'Preface', 'about the book', 3)""")


def test_draft_writes_editable_yaml(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    seed(con)
    llm = FakeLLM(DRAFT)
    path = topic_lists.draft(con, llm, "system_design", out_dir=tmp_path)
    data = yaml.safe_load(open(path, encoding="utf-8"))
    assert [t["slug"] for t in data["topics"]] == ["sd-caching", "sd-cache-eviction-policies", "sd-load-balancing"]
    assert data["topics"][1]["parent"] == "sd-caching"
    assert "Load balancer" in llm.calls[0]["user"] and llm.calls[0]["tier"] == "smart"


def test_apply_validates_and_classifies(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    seed(con)
    path = topic_lists.draft(con, FakeLLM(DRAFT), "system_design", out_dir=tmp_path)

    def classify(user):
        return {"assignments": [{"doc": 1, "topic": "sd-caching"}, {"doc": 2, "topic": "sd-cache-eviction-policies"},
                                {"doc": 3, "topic": "sd-load-balancing"}, {"doc": 4, "topic": "none"}]}

    n = topic_lists.apply(con, FakeLLM(classify), "system_design", out_dir=tmp_path)
    assert n == 3
    assert con.execute("select count(*) from topics where domain = 'system_design'").fetchone()[0] == 3
    got = dict(con.execute("select id, topic_slug from documents order by id").fetchall())
    assert got == {"d1": "sd-caching", "d2": "sd-cache-eviction-policies", "d3": "sd-load-balancing", "d4": None}


def test_apply_rejects_unknown_parent(tmp_path):
    con = staging.connect(tmp_path / "s.duckdb")
    (tmp_path / "system_design.yaml").write_text(yaml.safe_dump({"domain": "system_design", "topics": [
        {"name": "A", "slug": "sd-a", "parent": "sd-missing", "importance": 0.5}]}), encoding="utf-8")
    with pytest.raises(ValueError, match="sd-missing"):
        topic_lists.apply(con, FakeLLM({"assignments": []}), "system_design", out_dir=tmp_path)
