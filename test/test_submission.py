
try:
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_delete(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    pre_del_data = datastore.submission.get(submission_id)

    res = client.submission.delete(submission_id)
    assert res['success']

    datastore.submission.commit()
    post_del_data = datastore.submission.get(submission_id)
    assert pre_del_data != post_del_data
    assert post_del_data is None


def test_file_of_submission_details(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    submissison_data = datastore.submission.get(submission_id)

    res = client.submission.file(submission_id, submissison_data.files[0].sha256)
    assert res['file_info']['sha256']
    assert submissison_data.params.submitter in res['metadata']['submitter']


def test_full_submission(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission', q="file_count:[2 TO *]")
    submissison_data = datastore.submission.get(submission_id, as_obj=False)

    res = client.submission.full(submission_id)
    assert res['params'] == submissison_data['params']
    assert res['sid'] == submission_id
    assert 'file_tree' in res
    assert 'results' in res
    assert 'file_infos' in res
    assert 'errors' in res


def test_is_completed(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    submissison_data = datastore.submission.get(submission_id)

    res = client.submission.is_completed(submission_id)
    assert res == (submissison_data.state == 'completed')


def test_list(datastore, client):
    res = client.submission.list()
    assert res['total'] == datastore.submission.search('id:*', rows=0)['total']

    res = client.submission.list(user='admin')
    assert res['total'] == datastore.submission.search('params.submitter:admin', rows=0)['total']

    res = client.submission.list(group='USERS')
    assert res['total'] == datastore.submission.search('params.groups:USERS', rows=0)['total']


def test_report(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')

    res = client.submission.report(submission_id)
    assert res['sid'] == submission_id
    assert 'report_filtered' in res
    assert 'attack_matrix' in res
    assert 'important_files' in res


def test_set_verdict(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')

    for verdict in ['malicious', 'non_malicious']:
        res = client.submission.set_verdict(submission_id, verdict)
        assert res['success']

        submission_data = datastore.submission.get(submission_id, as_obj=False)
        assert 'admin' in submission_data['verdict'][verdict]


def test_submission(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    res = client.submission(submission_id)
    assert res == datastore.submission.get(submission_id, as_obj=False)
    assert res['sid'] == submission_id


def test_summary(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')

    res = client.submission.summary(submission_id)
    assert 'tags' in res
    assert 'map' in res


def test_tree(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission', q="file_count:[2 TO *]")
    submission_data = datastore.submission.get(submission_id)

    res = client.submission.tree(submission_id)
    assert len(res) >= 1
    for k in ['classification', 'filtered', 'tree']:
        assert k in res
    assert submission_data.files[0].sha256 in res['tree']
