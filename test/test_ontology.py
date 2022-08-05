
import pytest

from io import BytesIO

try:
    from utils import random_id_from_collection
except ImportError:
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get_ontology_for_alert(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')
    alert_data = datastore.alert.get(alert_id, as_obj=False)
    res = client.ontology.alert(alert_id)
    assert len(res) != 0
    assert any([record['file']['sha256'] == alert_data['file']['sha256'] for record in res])


def test_get_ontology_for_alert_raw(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')

    bio = BytesIO()
    res = client.ontology.alert(alert_id, output=bio)
    assert res
    assert bio.getbuffer().nbytes > 0


def test_get_ontology_for_file(datastore, client):
    sid = random_id_from_collection(datastore, 'submission')
    submission_data = datastore.submission.get(sid, as_obj=False)
    sha256 = submission_data['files'][0]['sha256']
    res = client.ontology.file(sha256)
    assert len(res) != 0
    assert all([record['file']['sha256'] == sha256 for record in res])


def test_get_ontology_for_file_raw(datastore, client):
    sid = random_id_from_collection(datastore, 'submission')
    submission_data = datastore.submission.get(sid, as_obj=False)
    sha256 = submission_data['files'][0]['sha256']

    bio = BytesIO()
    res = client.ontology.file(sha256, output=bio)
    assert res
    assert bio.getbuffer().nbytes > 0


def test_get_ontology_for_submission(datastore, client):
    sid = random_id_from_collection(datastore, 'submission')
    submission_data = datastore.submission.get(sid, as_obj=False)
    res = client.ontology.submission(sid)
    assert len(res) != 0
    assert any([record['file']['sha256'] == submission_data['files'][0]['sha256'] for record in res])


def test_get_ontology_for_submission_raw(datastore, client):
    sid = random_id_from_collection(datastore, 'submission')

    bio = BytesIO()
    res = client.ontology.submission(sid, output=bio)
    assert res
    assert bio.getbuffer().nbytes > 0
