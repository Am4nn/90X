"""Run the Feed v2 full generation, resumable and logged.

Usage (from the pipeline directory):

    uv run python run_feed_v2.py                # full run
    uv run python run_feed_v2.py --only a,b,c   # a subset of topic slugs
    uv run python run_feed_v2.py --reconcile    # trim surplus + write the shortfall

What it does, in order:

1. Write every topic's card budget (run_lessons.run) — drafts saved per topic.
   With --reconcile, trim each topic's surplus archetypes and write only its
   shortfall instead (reconcile.run). That is the right step once a corpus
   already exists: run_lessons skips any topic that already has archetyped
   cards, so it would write the 96 newly-covered topics and leave the uneven
   distribution on the other 177 untouched.
2. Gate + repair the drafts (regate.run) — answerability AND guessability
   (blind gate) verdicts, one rewrite each for rejected cards.

Properties you can rely on:

- Resumable. Each step saves per topic and skips topics that already have
  cards, so interrupting and re-running continues instead of restarting.
- Budget-capped. Every call is scoped to run_id "feed-v2-full", so the cap
  (PIPELINE_MAX_USD, default 35) counts only this run's spend, not the
  lifetime llm_calls table.
- Monitored. All progress goes to stdout AND .data/review/feed-v2-run.log
  (appended), so you can `tail -f` it while it runs.
- Off-peak only. DeepSeek halves its prices outside peak hours and the whole
  budget assumes that, so the run waits for the window rather than starting at
  double price. Checked once at the start: the weekend window is long enough
  that a 40-minute run cannot cross out of it.
"""

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from pipeline import staging
from pipeline.llm import LLM, is_off_peak, wait_for_off_peak
from pipeline.cards import reconcile, regate, run_lessons, validate

RUN_ID = "feed-v2-full"
LOG = Path(__file__).resolve().parents[1] / ".data" / "review" / "feed-v2-run.log"


class _Tee:
    """Mirror stdout to the console and an append-only log file."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
            s.flush()

    def flush(self):
        for s in self.streams:
            s.flush()


def _parse_args(argv):
    only = None
    for arg in argv:
        if arg.startswith("--only"):
            if "=" in arg:
                only = arg.split("=", 1)[1].split(",")
            elif argv.index(arg) + 1 < len(argv):
                only = argv[argv.index(arg) + 1].split(",")
    return [t.strip() for t in only if t.strip()] if only else None


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    only = _parse_args(argv)
    mode = "reconcile" if "--reconcile" in argv else "write"
    run_id = "feed-v2-rebalance" if mode == "reconcile" else RUN_ID

    LOG.parent.mkdir(parents=True, exist_ok=True)
    log = open(LOG, "a", encoding="utf-8")
    sys.stdout = _Tee(sys.__stdout__, log)

    print(f"=== Feed v2 run start  {datetime.now(timezone.utc).isoformat()}  run_id={run_id}  "
          f"only={only or 'all'} mode={mode} ===", flush=True)

    if not is_off_peak():
        print("peak hours: waiting for the off-peak window before spending", flush=True)
        wait_for_off_peak()
        print(f"off-peak window open  {datetime.now(timezone.utc).isoformat()}", flush=True)

    con = staging.connect()
    llm = LLM(con, run_id=run_id)

    started = time.time()

    if mode == "reconcile":
        print("--- step 1: trim surplus + write the shortfall ---", flush=True)
        written, dropped, refused = reconcile.run(con, only=only, tier="smart", llm=llm, dry_run=False)
        print(f"reconcile done: {written} cards written, {dropped} trimmed, {refused} slots refused, "
              f"{int(time.time() - started)}s elapsed", flush=True)
    else:
        print("--- step 1: write ---", flush=True)
        written, refused = run_lessons.run(con, only=only, tier="smart", llm=llm)
        print(f"write done: {written} cards, {refused} slots refused, "
              f"{int(time.time() - started)}s elapsed", flush=True)

    print("--- step 2: gate + repair ---", flush=True)
    result = regate.run(con, only=only, tier="smart", llm=llm)
    print(f"regate done: {result}, {int(time.time() - started)}s total", flush=True)

    print("--- step 3: cross-topic dedupe + answer-definition consistency ---", flush=True)
    print(validate.report(con), flush=True)

    print(f"=== Feed v2 run end  {datetime.now(timezone.utc).isoformat()}  "
          f"{int(time.time() - started)}s ===", flush=True)
    # Restore the real stdout before closing the log: leaving the _Tee in place
    # over a closed file made the first run exit 1 on anything printed after
    # this point, which looked like a failed run and was not one.
    sys.stdout = sys.__stdout__
    log.close()


if __name__ == "__main__":
    main()
