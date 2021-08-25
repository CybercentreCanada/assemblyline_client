

def test_alert(datastore, client):
    res = client.search.stats.alert('al.score', query="id:*")
    assert list(res.keys()) == ['avg', 'count', 'max', 'min', 'sum']
    for v in res.values():
        assert isinstance(v, int) or isinstance(v, float)


def test_file(datastore, client):
    res = client.search.stats.file('seen.count', query="id:*")
    assert list(res.keys()) == ['avg', 'count', 'max', 'min', 'sum']
    for v in res.values():
        assert isinstance(v, int) or isinstance(v, float)


def test_result(datastore, client):
    res = client.search.stats.result('result.score', query="id:*")
    assert list(res.keys()) == ['avg', 'count', 'max', 'min', 'sum']
    for v in res.values():
        assert isinstance(v, int) or isinstance(v, float)


def test_safelist(datastore, client):
    res = client.search.stats.safelist('file.size', query="id:*")
    assert list(res.keys()) == ['avg', 'count', 'max', 'min', 'sum']
    for v in res.values():
        assert isinstance(v, int) or isinstance(v, float)


def test_signature(datastore, client):
    res = client.search.stats.signature('order', query="id:*")
    assert list(res.keys()) == ['avg', 'count', 'max', 'min', 'sum']
    for v in res.values():
        assert isinstance(v, int) or isinstance(v, float)


def test_submission(datastore, client):
    res = client.search.stats.submission('file_count', query="id:*")
    assert list(res.keys()) == ['avg', 'count', 'max', 'min', 'sum']
    for v in res.values():
        assert isinstance(v, int) or isinstance(v, float)


def test_workflow(datastore, client):
    res = client.search.stats.workflow('hit_count', query="id:*")
    assert list(res.keys()) == ['avg', 'count', 'max', 'min', 'sum']
    for v in res.values():
        assert isinstance(v, int) or isinstance(v, float)
