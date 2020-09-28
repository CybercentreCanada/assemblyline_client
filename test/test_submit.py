import os

try:
    from assemblyline.common import forge
    from assemblyline.common.uid import get_random_id
    from assemblyline.odm.randomizer import get_random_phrase

    from utils import random_id_from_collection

    config = forge.get_config()

except (ImportError, SyntaxError):
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_submit_content(datastore, client):
    content = get_random_phrase(wmin=15, wmax=50).encode()
    fname = "{}.txt".format(get_random_id())
    res = client.submit(content=content, fname=fname)
    assert res['sid'] is not None
    assert res['files'][0]['name'] == fname
    assert res == datastore.submission.get(res['sid'], as_obj=False)


def test_submit_path(datastore, client):
    content = get_random_phrase(wmin=15, wmax=50).encode()
    test_path = "/tmp/test_submit_{}.txt".format(get_random_id())
    with open(test_path, 'wb') as test_file:
        test_file.write(content + b"PATH")

    params = {'service_spec': {"extract": {"password": "test"}}}
    res = client.submit(path=test_path, params=params)
    assert res.get('sid', None) is not None
    assert res['files'][0]['name'] == os.path.basename(test_path)
    assert res['params']['service_spec'] == params['service_spec']
    assert res == datastore.submission.get(res['sid'], as_obj=False)


def test_submit_sha(datastore, client):
    file_id = random_id_from_collection(datastore, 'file')
    metadata = {"file_id": get_random_id(), "comment": "test"}
    res = client.submit(sha256=file_id, metadata=metadata)
    assert res['sid'] is not None
    assert res['files'][0]['sha256'] == file_id
    assert res['metadata'] == metadata
    assert res == datastore.submission.get(res['sid'], as_obj=False)


def test_submit_url(datastore, client):
    url='https://www.cyber.gc.ca/en/theme-gcwu-fegc/assets/wmms.svg'
    params = {"deep_scan": True, "ignore_cache": True, "priority": 100}
    res = client.submit(url=url, params=params)
    assert res['sid'] is not None
    assert res['files'][0]['name'] == os.path.basename(url)
    for k in params:
        assert res['params'][k] == params[k]
    assert res == datastore.submission.get(res['sid'], as_obj=False)


def test_submit_dynamic(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    submission_data = datastore.submission.get(submission_id, as_obj=False)

    res = client.submit.dynamic(submission_data['files'][0]['sha256'], copy_sid=submission_id,
                                name=submission_data['files'][0]['name'])
    assert res['sid'] is not None
    assert res == datastore.submission.get(res['sid'], as_obj=False)
    assert 'Dynamic Analysis' in res['params']['services']['selected']
    for k in res['params']:
        if k not in ['submitter', 'services', 'description']:
            assert res['params'][k] == submission_data['params'][k]


def test_resubmit(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    submission_data = datastore.submission.get(submission_id, as_obj=False)
    submission_data['params']['services']['runtime_excluded'] = []

    res = client.submit.resubmit(submission_id)
    assert res['sid'] is not None
    assert res == datastore.submission.get(res['sid'], as_obj=False)
    for k in res['params']:
        if k not in ['submitter', 'description']:
            assert res['params'][k] == submission_data['params'][k]
