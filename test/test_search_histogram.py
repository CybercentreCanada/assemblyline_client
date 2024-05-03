

def test_alert(datastore, client):
    res = client.search.histogram.alert('al.score', "id:*", mincount=1, start=0, end=4000, gap=500)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_badlist(datastore, client):
    res = client.search.histogram.badlist('added', "id:*", mincount=1, start="now-6h", end="now+6h")
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_file(datastore, client):
    res = client.search.histogram.file('seen.last', "id:*", mincount=1, start="now-6h", end="now+6h")
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_result(datastore, client):
    res = client.search.histogram.result('result.score', "id:*", mincount=1, start=0, end=4000, gap=500)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_safelist(datastore, client):
    res = client.search.histogram.safelist('added', "id:*", mincount=1, start="now-15d",
                                           end="now+15d", gap="+1d")
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_signature(datastore, client):
    res = client.search.histogram.signature('last_modified', "id:*", mincount=1, start="now-6h",
                                            end="now+6h", gap="+1h")
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_submission(datastore, client):
    res = client.search.histogram.submission('max_score', "id:*", mincount=1, end=4000, gap=400)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1


def test_workflow(datastore, client):
    res = client.search.histogram.workflow('hit_count', "id:*", mincount=1, end=4000, gap=400)
    assert isinstance(res, dict)
    for v in res.values():
        assert v >= 1
