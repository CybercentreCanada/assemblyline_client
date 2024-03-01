
def _compare_values(a, b):
    assert len(a) == len(b)
    for idx, item_a in enumerate(a):
        item_b = b[idx]
        for key, val in item_a.items():
            assert val == item_b.get(key, val)


def test_alert(datastore, client):
    res = sorted([x for x in client.search.stream.alert("id:*")], key=lambda k: k['id'])
    assert len(res) > 0
    _compare_values(res, sorted(list(datastore.alert.stream_search("id:*", as_obj=False)), key=lambda k: k['id']))


def test_file(datastore, client):
    res = sorted([x for x in client.search.stream.file("id:*")], key=lambda k: k['id'])
    assert len(res) > 0
    _compare_values(res, sorted(list(datastore.file.stream_search("id:*", as_obj=False)), key=lambda k: k['id']))


def test_heuristic(datastore, client):
    res = sorted([x for x in client.search.stream.heuristic("id:*")], key=lambda k: k['id'])
    assert len(res) > 0
    _compare_values(res, sorted(list(datastore.heuristic.stream_search("id:*", as_obj=False)), key=lambda k: k['id']))


def test_result(datastore, client):
    res = sorted([x for x in client.search.stream.result("id:*")], key=lambda k: k['id'])
    assert len(res) > 0
    _compare_values(res, sorted(list(datastore.result.stream_search("id:*", as_obj=False)), key=lambda k: k['id']))


def test_safelist(datastore, client):
    res = sorted([x for x in client.search.stream.safelist("id:*")], key=lambda k: k['id'])
    assert len(res) > 0
    _compare_values(res, sorted(list(datastore.safelist.stream_search("id:*", as_obj=False)), key=lambda k: k['id']))


def test_signature(datastore, client):
    res = sorted([x for x in client.search.stream.signature("id:*")], key=lambda k: k['id'])
    assert len(res) > 0
    _compare_values(res, sorted(list(datastore.signature.stream_search("id:*", as_obj=False)), key=lambda k: k['id']))


def test_submission(datastore, client):
    res = sorted([x for x in client.search.stream.submission("id:*")], key=lambda k: k['id'])
    assert len(res) > 0
    _compare_values(res, sorted(list(datastore.submission.stream_search("id:*", as_obj=False)), key=lambda k: k['id']))


def test_workflow(datastore, client):
    res = sorted([x for x in client.search.stream.workflow("id:*")], key=lambda k: k['id'])
    assert len(res) > 0
    _compare_values(res, sorted(list(datastore.workflow.stream_search("id:*", as_obj=False)), key=lambda k: k['id']))
