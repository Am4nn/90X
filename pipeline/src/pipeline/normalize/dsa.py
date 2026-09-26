"""Join the LeetCode-style sources into one `problems` table, keyed by slug.

Base list: kaysss/leetcode-problem-detailed (every free and premium problem).
Statement: greengerong markdown > newfacade text > kaysss HTML converted.
Solutions: newfacade Python + greengerong Java/C++/JS.
Enrichment: NeetCode pattern/flags/video, company frequency (liquidslr)."""

import ast
import csv
import glob
import json
import re
from pathlib import Path

from markdownify import markdownify

from ..config import DATA_DIR

DSA = DATA_DIR / "dsa"

# Categories kept, and the topic they belong to beyond DSA patterns.
KEEP_CATEGORIES = {"Algorithms": [], "Concurrency": ["concurrency"], "Database": ["sql"]}

# greengerong column → our language key.
LANG_KEYS = {"java": "java", "c++": "cpp", "javascript": "javascript", "python": "python"}


def pattern_slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def strip_fence(text: str) -> str:
    text = text.strip()
    m = re.match(r"^```[\w+#-]*\n(.*?)\n?```$", text, re.S)
    return m.group(1).strip() if m else text


def _list(value) -> list:
    if isinstance(value, list):
        return value
    if not value:
        return []
    try:
        parsed = ast.literal_eval(value)
        return list(parsed) if isinstance(parsed, (list, tuple)) else []
    except (ValueError, SyntaxError):
        return []


def _num(value, cast=float):
    try:
        return cast(float(value))
    except (TypeError, ValueError):
        return None


def build_problems(kaysss: dict, newfacade: dict, multilang: dict, neetcode: dict, companies: dict) -> list[dict]:
    rows = []
    for slug, k in kaysss.items():
        category = k.get("category", "")
        if category not in KEEP_CATEGORIES:
            continue
        nf, gg, nc = newfacade.get(slug, {}), multilang.get(slug, {}), neetcode.get(slug)

        statement = (gg.get("content") or "").strip() or (nf.get("problem_description") or "").strip()
        if not statement and (k.get("content") or "").strip():
            statement = markdownify(k["content"], heading_style="ATX").strip()

        solutions = {}
        if nf.get("completion"):
            solutions["python"] = nf["completion"].strip()
        for column, key in LANG_KEYS.items():
            if gg.get(column) and key not in solutions:
                solutions[key] = strip_fence(gg[column])

        rows.append({
            "slug": slug,
            "kind": "leetcode",
            "lc_number": _num(k.get("questionFrontendId"), int),
            "title": k["questionTitle"],
            "difficulty": k["difficulty"],
            "pattern_slug": pattern_slug(nc["pattern"]) if nc else None,
            "pattern_source": "neetcode" if nc else None,
            "topic_slugs": KEEP_CATEGORIES[category],
            "tags": _list(k.get("topicTags")) or _list(nf.get("tags")),
            "nc150": bool(nc and nc.get("neetcode150")),
            "blind75": bool(nc and nc.get("blind75")),
            "companies": companies.get(slug, {}),
            "statement_md": statement or None,
            "solutions": solutions,
            "video_id": nc.get("video") if nc else None,
            "url": f"https://leetcode.com/problems/{slug}/",
            "source_id": "leetcode-detailed",
            "ac_rate": _num(k.get("acRate")),
            "total_accepted": _num(k.get("totalAcceptedRaw"), int),
            "similar_slugs": _list(k.get("similarQuestions")),
        })
    return rows


# ---- loading the real files ------------------------------------------------

def load_kaysss(path: Path = DSA / "leetcode-detailed" / "questions_detailed.csv") -> dict:
    csv.field_size_limit(10**9)
    with open(path, encoding="utf-8") as f:
        return {r["TitleSlug"]: r for r in csv.DictReader(f)}


def load_newfacade(folder: Path = DSA / "leetcode-dataset") -> dict:
    out = {}
    for file in sorted(folder.glob("*.jsonl")):
        with open(file, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                out[r["task_id"]] = r
    return out


def load_multilang(path: Path = DSA / "leetcode-multilang" / "leetcode-train.jsonl") -> dict:
    with open(path, encoding="utf-8") as f:
        return {r["slug"]: r for r in map(json.loads, f)}


def load_neetcode(path: Path = DSA / "neetcode" / ".problemSiteData.json") -> dict:
    with open(path, encoding="utf-8") as f:
        return {p["link"].strip("/"): p for p in json.load(f)}


def load_companies(folder: Path = DSA / "company-wise-liquidslr") -> dict:
    out: dict[str, dict] = {}
    for file in glob.glob(str(folder / "*" / "5. All.csv")):
        company = Path(file).parent.name
        with open(file, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                slug = r["Link"].rstrip("/").split("/")[-1]
                freq = _num(r.get("Frequency"))
                if freq is not None:
                    out.setdefault(slug, {})[company] = freq
    return out


def run(con) -> int:
    rows = build_problems(load_kaysss(), load_newfacade(), load_multilang(), load_neetcode(), load_companies())
    con.execute("delete from problems where kind = 'leetcode'")
    con.executemany(
        """insert into problems (slug, kind, lc_number, title, difficulty, pattern_slug, pattern_source,
               topic_slugs, tags, nc150, blind75, companies, statement_md, solutions, video_id, url,
               source_id, ac_rate, total_accepted, similar_slugs)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [[r["slug"], r["kind"], r["lc_number"], r["title"], r["difficulty"], r["pattern_slug"], r["pattern_source"],
          r["topic_slugs"], r["tags"], r["nc150"], r["blind75"], json.dumps(r["companies"]), r["statement_md"],
          json.dumps(r["solutions"]), r["video_id"], r["url"], r["source_id"], r["ac_rate"], r["total_accepted"],
          r["similar_slugs"]] for r in rows],
    )
    return len(rows)
