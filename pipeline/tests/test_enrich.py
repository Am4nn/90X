from pipeline.enrich import importance, topics


def test_importance_orders_sensibly():
    stats = importance.Stats(max_accepted=10_000_000, max_companies=50)
    nc150_hot = importance.score(nc150=True, blind75=True, companies={"Amazon": 100, "Google": 90}, total_accepted=9_000_000, stats=stats)
    company_only = importance.score(nc150=False, blind75=False, companies={"Amazon": 80}, total_accepted=500_000, stats=stats)
    obscure = importance.score(nc150=False, blind75=False, companies={}, total_accepted=2_000, stats=stats)
    assert 0 <= obscure < company_only < nc150_hot <= 1


def test_importance_handles_missing_numbers():
    stats = importance.Stats(max_accepted=100, max_companies=1)
    assert importance.score(False, False, {}, None, stats) == 0


def test_dsa_topics_cover_all_patterns_and_links_are_valid():
    rows, links = topics.dsa_topics()
    slugs = {r["slug"] for r in rows}
    assert len(slugs) == 24
    assert "sliding-window" in slugs and "heap-priority-queue" in slugs
    assert all(a in slugs and b in slugs for a, b in links)
    # every pattern except the root is reachable from arrays-hashing
    reach, frontier = {"arrays-hashing"}, ["arrays-hashing"]
    while frontier:
        node = frontier.pop()
        for a, b in links:
            if a == node and b not in reach:
                reach.add(b)
                frontier.append(b)
    assert reach == slugs
