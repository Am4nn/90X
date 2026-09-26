from pipeline.normalize import docs

MD = """# Guide

Intro paragraph that is long enough to stand on its own as a section body here.

## Caching

Caching keeps hot data close. """ + "Details. " * 60 + """

```python
## not a heading, inside code
x = 1
```

### Cache eviction

LRU evicts the least recently used entry. """ + "More. " * 60 + """

### Tiny

Too short.

## Load balancing

![diagram](images/lb.png) and see [consistency](consistency.md). """ + "Text. " * 60 + """
"""


def test_split_respects_code_fences_and_merges_tiny_sections():
    sections = docs.split_markdown(MD, min_chars=200)
    titles = [s.title for s in sections]
    assert titles == ["Guide", "Caching", "Caching › Cache eviction", "Load balancing"]
    caching = sections[1].body
    assert "## not a heading" in caching  # stayed inside the Caching body
    eviction = sections[2].body
    assert "Too short." in eviction  # tiny section merged into the previous one


def test_rewrites_relative_links_to_github():
    body = "![d](images/lb.png) [c](consistency.md) [abs](https://x.io) [anchor](#top)"
    out = docs.rewrite_links(body, repo="donnemartin/system-design-primer", file_dir="solutions/web")
    assert "https://raw.githubusercontent.com/donnemartin/system-design-primer/HEAD/solutions/web/images/lb.png" in out
    assert "https://github.com/donnemartin/system-design-primer/blob/HEAD/solutions/web/consistency.md" in out
    assert "(https://x.io)" in out and "(#top)" in out


def test_doc_ids_are_stable():
    a = docs.doc_id("primer", "README.md", "Caching", 1)
    assert a == docs.doc_id("primer", "README.md", "Caching", 1)
    assert a != docs.doc_id("primer", "README.md", "Caching", 2)
    assert a.startswith("primer:")


def test_split_long_text_keeps_paragraphs_together():
    text = "\n\n".join(f"para {i} " + "x" * 90 for i in range(10))
    parts = docs.split_long_text(text, limit=300)
    assert len(parts) > 1 and all(len(p) <= 400 for p in parts)
    assert "\n\n".join(parts).count("para ") == 10


def test_split_long_text_falls_back_to_single_newlines():
    text = "\n".join(f"line {i} " + "y" * 90 for i in range(20))  # no blank lines, like PDF text
    parts = docs.split_long_text(text, limit=500)
    assert len(parts) >= 4 and all(len(p) <= 600 for p in parts)
    assert sum(p.count("line ") for p in parts) == 20
