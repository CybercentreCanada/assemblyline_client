

def test_alert(datastore, client):
    res = client.search.fields.alert()
    assert isinstance(res, dict)
    for v in res.values():
        assert 'default' in v
        assert 'indexed' in v
        assert 'list' in v
        assert 'stored' in v
        assert 'type' in v


def test_file(datastore, client):
    res = client.search.fields.file()
    assert isinstance(res, dict)
    for v in res.values():
        assert 'default' in v
        assert 'indexed' in v
        assert 'list' in v
        assert 'stored' in v
        assert 'type' in v


def test_heuristic(datastore, client):
    res = client.search.fields.heuristic()
    assert isinstance(res, dict)
    for v in res.values():
        assert 'default' in v
        assert 'indexed' in v
        assert 'list' in v
        assert 'stored' in v
        assert 'type' in v


def test_result(datastore, client):
    res = client.search.fields.result()
    assert isinstance(res, dict)
    for v in res.values():
        assert 'default' in v
        assert 'indexed' in v
        assert 'list' in v
        assert 'stored' in v
        assert 'type' in v


def test_safelist(datastore, client):
    res = client.search.fields.safelist()
    assert isinstance(res, dict)
    for v in res.values():
        assert 'default' in v
        assert 'indexed' in v
        assert 'list' in v
        assert 'stored' in v
        assert 'type' in v


def test_signature(datastore, client):
    res = client.search.fields.signature()
    assert isinstance(res, dict)
    for v in res.values():
        assert 'default' in v
        assert 'indexed' in v
        assert 'list' in v
        assert 'stored' in v
        assert 'type' in v


def test_submission(datastore, client):
    res = client.search.fields.submission()
    assert isinstance(res, dict)
    for v in res.values():
        assert 'default' in v
        assert 'indexed' in v
        assert 'list' in v
        assert 'stored' in v
        assert 'type' in v


def test_workflow(datastore, client):
    res = client.search.fields.workflow()
    assert isinstance(res, dict)
    for v in res.values():
        assert 'default' in v
        assert 'indexed' in v
        assert 'list' in v
        assert 'stored' in v
        assert 'type' in v
