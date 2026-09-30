"""Gate 2: run the blind gate over 50 cards, report the rejection rate, stop.

The plan forbids spending the rest of the corpus budget on a blind gate nobody
has seen the cost of. This takes 50 freshly generated draft cards through the
blind gate, reports how many a reader could guess, and stops. It writes
nothing: a rejection rate that comes back implausible means the gate is wrong,
not the corpus, and the number goes to the orchestrator rather than into more
generation or a blanket rewrite.
"""

import json

from ..llm import LLM, spend_usd
from . import blind_gate

TRIAL_CARDS = 50


class Draft:
    """A stored card in the shape the blind gate reads."""

    def __init__(self, row) -> None:
        (self.id, self.format, self.prompt, options, self.answer,
         picked, constraints, pairs, value, tolerance) = row
        self.options = json.loads(options) if options else []
        self.picked = json.loads(picked) if picked else None
        constraints = json.loads(constraints) if constraints else None
        # Part B's grader stores constraints as {"before": [[a, b], ...]}; the
        # flat list the blind gate checks is the value under that key.
        self.constraints = constraints.get("before") if isinstance(constraints, dict) else constraints
        self.pairs = json.loads(pairs) if pairs else None
        self.value = value
        self.tolerance = tolerance


def pick_cards(con, n: int = TRIAL_CARDS) -> list[Draft]:
    """The first n draft lesson cards, in a stable order."""
    rows = con.execute(
        """select id, format, prompt_md, options, answer_md, picked, constraints, pairs, value, tolerance
           from cards where source = 'lesson' and status = 'draft'
           order by topic_slug, id limit ?""",
        [n],
    ).fetchall()
    return [Draft(r) for r in rows]


def run(con, llm: LLM | None = None, n: int = TRIAL_CARDS, tier: str = "smart") -> dict:
    """Report the blind-gate rejection rate over n cards. Writes nothing."""
    llm = llm or LLM(con)
    cards = pick_cards(con, n)
    before = spend_usd(con)
    verdicts = blind_gate.review(llm, cards, tier=tier)
    rejected = blind_gate.judge(cards, verdicts)
    spent = spend_usd(con) - before
    rate = len(rejected) / len(cards) if cards else 0.0
    print(f"Gate 2: {len(cards)} cards, {len(rejected)} rejected ({rate:.0%}), ${spent:.4f}", flush=True)
    for card, reason in rejected:
        print(f"  {card.id}: {reason}", flush=True)
    return {"cards": len(cards), "rejected": len(rejected), "rate": rate, "spend": spent}
