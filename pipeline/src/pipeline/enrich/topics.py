"""Topic trees. DSA is fixed: NeetCode's 18 patterns and its roadmap edges,
which draw the Pattern Map. Other areas are drafted by AI into
pipeline/topics/<domain>.yaml and approved by hand (see draft/apply)."""

from ..normalize.dsa import pattern_slug

# (name, importance) in roadmap order.
DSA_PATTERNS = [
    ("Arrays & Hashing", 1.0), ("Two Pointers", 0.9), ("Stack", 0.8), ("Binary Search", 0.9),
    ("Sliding Window", 0.9), ("Linked List", 0.8), ("Trees", 1.0), ("Tries", 0.6),
    ("Heap / Priority Queue", 0.8), ("Backtracking", 0.7), ("Graphs", 0.9), ("Advanced Graphs", 0.6),
    ("1-D Dynamic Programming", 0.9), ("2-D Dynamic Programming", 0.8), ("Greedy", 0.7),
    ("Intervals", 0.7), ("Math & Geometry", 0.5), ("Bit Manipulation", 0.5),
]

# NeetCode roadmap: prerequisite → next.
DSA_EDGES = [
    ("Arrays & Hashing", "Two Pointers"), ("Arrays & Hashing", "Stack"),
    ("Two Pointers", "Binary Search"), ("Two Pointers", "Sliding Window"), ("Two Pointers", "Linked List"),
    ("Binary Search", "Trees"), ("Linked List", "Trees"),
    ("Trees", "Tries"), ("Trees", "Heap / Priority Queue"), ("Trees", "Backtracking"),
    ("Heap / Priority Queue", "Intervals"), ("Heap / Priority Queue", "Greedy"), ("Heap / Priority Queue", "Advanced Graphs"),
    ("Backtracking", "Graphs"), ("Backtracking", "1-D Dynamic Programming"),
    ("Graphs", "Advanced Graphs"), ("Graphs", "2-D Dynamic Programming"), ("Graphs", "Math & Geometry"),
    ("1-D Dynamic Programming", "2-D Dynamic Programming"), ("1-D Dynamic Programming", "Bit Manipulation"),
    ("Bit Manipulation", "Math & Geometry"),
]


def dsa_topics() -> tuple[list[dict], list[tuple[str, str]]]:
    rows = [
        {"slug": pattern_slug(name), "parent_slug": None, "domain": "dsa", "name": name,
         "description": None, "importance": imp, "sort": i}
        for i, (name, imp) in enumerate(DSA_PATTERNS)
    ]
    links = [(pattern_slug(a), pattern_slug(b)) for a, b in DSA_EDGES]
    return rows, links


def apply_dsa(con) -> int:
    rows, links = dsa_topics()
    con.execute("delete from topic_links where from_slug in (select slug from topics where domain = 'dsa')")
    con.execute("delete from topics where domain = 'dsa'")
    con.executemany(
        "insert into topics (slug, parent_slug, domain, name, description, importance, sort) values (?, ?, ?, ?, ?, ?, ?)",
        [[r["slug"], r["parent_slug"], r["domain"], r["name"], r["description"], r["importance"], r["sort"]] for r in rows],
    )
    con.executemany("insert into topic_links (from_slug, to_slug) values (?, ?)", links)
    return len(rows)
