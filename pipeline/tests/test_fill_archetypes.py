"""scripts/fill_archetypes.py: nothing is released that was not actually judged.

The script promises a new card is released only after the answerability gate and the key audit
have both ruled on it. Two ways it broke that promise, found in review: a topic whose gate call
failed left its cards as plain drafts that were then counted as survivors, and a key-audit chunk
that raised was skipped, its cards kept and released unchecked.
"""

import importlib.util
import os
from pathlib import Path

import pytest

from pipeline import staging
from pipeline.cards import key_audit

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "fill_archetypes.py"
os.chdir(Path(__file__).resolve().parents[1])
_spec = importlib.util.spec_from_file_location("fill_archetypes_script", SCRIPT)
fa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fa)


def make(tmp_path, rows):
    con = staging.connect(tmp_path / "s.duckdb")
    con.execute("insert into topics (slug, domain, name, sort) values ('t', 'cs', 'T', 0)")
    for cid, quality in rows:
        con.execute(
            """insert into cards (id, topic_slug, format, archetype, difficulty, prompt_md, options, answer_md,
                                  key_points, picked, status, kept, quality, source)
               values (?, 't', 'pick_one', 'concept', 'Easy', 'Which one?', '["a","b","c","d"]', 'a is right',
                       '["x","y"]', '[0]', 'draft', false, ?, 'lesson')""",
            [cid, quality],
        )
    return con


def test_a_card_the_gate_never_ruled_on_is_not_a_survivor(tmp_path):
    con = make(tmp_path, [("judged", '{"regated": true}'), ("unjudged", "{}")])
    assert fa.judged_survivors(con, ["judged", "unjudged"]) == ["judged"]
    con.execute("update cards set status = 'rejected' where id = 'judged'")
    assert fa.judged_survivors(con, ["judged", "unjudged"]) == [], "a rejected card is not a survivor"
    assert fa.judged_survivors(con, []) == []


class Verdicts:
    """Stands in for key_audit.audit: one scripted reply per tier."""

    def __init__(self, by_tier):
        self.by_tier = by_tier
        self.tiers_seen = []

    def __call__(self, llm, topic, cards, tier="fast"):
        self.tiers_seen.append(tier)
        outcome = self.by_tier[tier]
        if isinstance(outcome, Exception):
            raise outcome
        return key_audit.KeyAudit(verdicts=[key_audit.KeyVerdict(index=i, verdict=outcome.get(i, "agrees"),
                                                                 reason="the key disagrees")
                                            for i in range(len(cards))])


def test_a_chunk_where_a_tier_fails_is_unaudited_never_released(tmp_path, monkeypatch):
    con = make(tmp_path, [("a", '{"regated": true}'), ("b", '{"regated": true}')])
    monkeypatch.setattr(fa.key_audit, "audit", Verdicts({"fast": {}, "smart": RuntimeError("provider down")}))
    rejected, unaudited = fa.audit_new(None, con, {"t": {"name": "T"}}, ["a", "b"])
    assert rejected == set()
    assert unaudited == {"a", "b"}, "a failed tier must leave the whole chunk unaudited, not skipped"


def test_a_contradiction_from_either_tier_rejects_a_new_card(tmp_path, monkeypatch):
    con = make(tmp_path, [("a", '{"regated": true}'), ("b", '{"regated": true}')])
    # Only the second tier objects, to card index 1.
    monkeypatch.setattr(fa.key_audit, "audit", Verdicts({"fast": {}, "smart": {1: "contradicts"}}))
    rejected, unaudited = fa.audit_new(None, con, {"t": {"name": "T"}}, ["a", "b"])
    assert unaudited == set()
    assert len(rejected) == 1
    gone = next(iter(rejected))
    status, kept, why = con.execute("select status, kept, reject_reason from cards where id = ?", [gone]).fetchone()
    assert (status, kept) == ("rejected", False) and why.startswith("answer key contradicts")


def test_a_clean_chunk_is_audited_on_both_tiers_and_released(tmp_path, monkeypatch):
    con = make(tmp_path, [("a", '{"regated": true}')])
    audit = Verdicts({"fast": {}, "smart": {}})
    monkeypatch.setattr(fa.key_audit, "audit", audit)
    assert fa.audit_new(None, con, {"t": {"name": "T"}}, ["a"]) == (set(), set())
    assert audit.tiers_seen == ["fast", "smart"], "both tiers must run on every chunk"


def test_an_budget_stop_is_not_swallowed_as_a_failed_chunk(tmp_path, monkeypatch):
    from pipeline.llm import BudgetExceeded

    con = make(tmp_path, [("a", '{"regated": true}')])
    monkeypatch.setattr(fa.key_audit, "audit", Verdicts({"fast": BudgetExceeded("cap"), "smart": {}}))
    with pytest.raises(BudgetExceeded):
        fa.audit_new(None, con, {"t": {"name": "T"}}, ["a"])
