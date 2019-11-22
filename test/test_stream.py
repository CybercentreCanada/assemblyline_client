

def test_alert(datastore, client):
    res = [x for x in client.search.stream.alert("id:*")]
    assert len(res) > 0
    assert res == list(datastore.alert.stream_search("id:*", as_obj=False))


def test_file(datastore, client):
    res = [x for x in client.search.stream.file("id:*")]
    assert len(res) > 0
    assert res == list(datastore.file.stream_search("id:*", as_obj=False))


def test_heuristic(datastore, client):
    res = [x for x in client.search.stream.heuristic("id:*")]
    assert len(res) > 0
    assert res == list(datastore.heuristic.stream_search("id:*", as_obj=False))


def test_result(datastore, client):
    res = [x for x in client.search.stream.result("id:*")]
    assert len(res) > 0
    assert res == list(datastore.result.stream_search("id:*", as_obj=False))


def test_signature(datastore, client):
    res = [x for x in client.search.stream.signature("id:*")]
    assert len(res) > 0
    assert res == list(datastore.signature.stream_search("id:*", as_obj=False))


def test_submission(datastore, client):
    res = [x for x in client.search.stream.submission("id:*")]
    assert len(res) > 0
    assert res == list(datastore.submission.stream_search("id:*", as_obj=False))


def test_workflow(datastore, client):
    res = [x for x in client.search.stream.workflow("id:*")]
    assert len(res) > 0
    assert res == list(datastore.workflow.stream_search("id:*", as_obj=False))
