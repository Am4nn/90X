"""Gate 1: generate one topic's full budget and measure the cost per card.

The plan forbids running 274 topics on an estimate. The original pass averaged
~$0.0017 a card; structured cards carry more fields and may cost more. This
writes exactly one topic — the highest-importance one with an `ok` lesson — and
reports cards written, tokens in and out, spend, and the measured cost per
card. It stops there; nothing else is generated until a human approves the
number.
"""

import time

from ..llm import LLM, spend_usd
from . import archetypes, run_lessons


def pick_topic(con) -> dict | None:
    """The highest-importance topic with an ok lesson, by the same order the
    lesson run uses: importance desc, then slug."""
    row = con.execute(
        """select t.slug, t.name, t.domain, t.importance, l.body_md
           from lessons l join topics t on t.slug = l.topic_slug
           where l.status = 'ok'
           order by t.importance desc, t.slug limit 1"""
    ).fetchone()
    if row is None:
        return None
    return dict(zip(["slug", "name", "domain", "importance", "lesson"], row))


def tokens(con) -> tuple[int, int, int]:
    return con.execute(
        "select coalesce(sum(tokens_in),0), coalesce(sum(tokens_out),0), coalesce(sum(tokens_reasoning),0) "
        "from llm_calls"
    ).fetchone()


def run(con, tier: str = "smart") -> None:
    llm = LLM(con)
    topic = pick_topic(con)
    if topic is None:
        print("no topic with an ok lesson", flush=True)
        return
    slots = archetypes.budget(topic)
    before_spend = spend_usd(con)
    before_tokens = tokens(con)
    started = time.time()

    with run_lessons.lock_for(con):
        hard = run_lessons.hard_sources(con, topic["slug"], topic["domain"])
    print(f"writing {len(slots)} slots...", flush=True)
    cards, refused = run_lessons.write_topic(llm, topic, topic["lesson"], slots, run_lessons.hard_text(hard), tier,
                                             progress=True)
    with run_lessons.lock_for(con):
        run_lessons.save(con, topic, cards, hard)
        spent = spend_usd(con) - before_spend
        after_tokens = tokens(con)

    t_in, t_out, t_reasoning = [b - a for a, b in zip(before_tokens, after_tokens)]
    cost_per_card = spent / len(cards) if cards else 0.0

    print("", flush=True)
    print(f"topic:        {topic['slug']} ({topic['name']}, {topic['domain']}, importance {topic['importance']})")
    print(f"budget:       {len(slots)} slots, {len({s.archetype for s in slots})} archetypes")
    print(f"cards:        {len(cards)} written, {len(refused)} refused")
    print(f"tokens:       {t_in} in, {t_out} out" + (f" (+{t_reasoning} reasoning)" if t_reasoning else ""))
    print(f"spend:        ${spent:.4f}")
    print(f"cost/card:    ${cost_per_card:.5f}")
    print(f"cumulative:   ${spend_usd(con):.4f}")
    print(f"elapsed:      {int(time.time() - started)}s", flush=True)
