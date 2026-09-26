from pipeline import chunk, vector


def words(n, prefix="w"):
    return " ".join(f"{prefix}{i}" for i in range(n))


def test_chunks_respect_word_limits_and_keep_all_text():
    text = "\n\n".join(words(120, f"p{j}_") for j in range(10))  # 1,200 words in 10 paragraphs
    parts = chunk.split_text(text, max_words=450)
    assert len(parts) == 4  # 3 paragraphs (360 words) fit per chunk; paragraphs are never cut
    assert all(len(p.split()) <= 450 for p in parts)
    assert sum(len(p.split()) for p in parts) == 1200


def test_giant_paragraph_is_split_by_words():
    parts = chunk.split_text(words(1000), max_words=450)
    assert [len(p.split()) for p in parts] == [450, 450, 100]


def test_tiny_tail_merges_into_previous_chunk():
    text = words(440) + "\n\n" + words(20, "t")
    parts = chunk.split_text(text, max_words=450, min_words=60)
    assert len(parts) == 1  # a 20-word tail isn't worth its own vector


def test_build_chunks_ids_and_hashes_are_stable():
    rows = chunk.build_chunks("doc", "primer:abc", "Caching", words(900), meta={"domain": "system_design"})
    assert [r["id"] for r in rows] == ["doc:primer:abc:0", "doc:primer:abc:1"]
    again = chunk.build_chunks("doc", "primer:abc", "Caching", words(900), meta={"domain": "system_design"})
    assert [r["hash"] for r in rows] == [r["hash"] for r in again]
    assert rows[0]["text"].startswith("Caching\n\n")  # title gives the embedding context


def test_plan_upserts_only_changed_and_deletes_stale():
    chunks = [{"id": "a", "hash": "1"}, {"id": "b", "hash": "2"}, {"id": "c", "hash": "3"}]
    embedded = {"a": "1", "b": "old", "z": "9"}
    upsert, delete = vector.plan(chunks, embedded)
    assert [c["id"] for c in upsert] == ["b", "c"]
    assert delete == ["z"]
