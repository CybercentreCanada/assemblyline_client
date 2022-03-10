
import os
import pytest

try:
    from assemblyline_client.v4_client.common.utils import ClientError
    from utils import random_id_from_collection
except ImportError:
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


# noinspection PyUnusedLocal
def test_create_to_file(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    tested_bundle = "/tmp/bundle_{}".format(submission_id)
    try:
        client.bundle.create(submission_id, tested_bundle)

        assert open(tested_bundle, 'rb').read(4) == b'CART'
    finally:
        os.unlink(tested_bundle)


# noinspection PyUnusedLocal
def test_create_alert_to_file(datastore, client):
    alert_id = random_id_from_collection(datastore, 'alert')
    tested_bundle = "/tmp/bundle_alert_{}".format(alert_id)
    try:
        client.bundle.create(alert_id, tested_bundle, use_alert=True)

        assert open(tested_bundle, 'rb').read(4) == b'CART'
    finally:
        os.unlink(tested_bundle)


# noinspection PyUnusedLocal
def test_create_to_file_using_object(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    tested_bundle = "/tmp/bundle_{}_fobj".format(submission_id)
    try:
        client.bundle.create(submission_id, open(tested_bundle, "wb"))

        assert open(tested_bundle, 'rb').read(4) == b'CART'
    finally:
        os.unlink(tested_bundle)


# noinspection PyUnusedLocal
def test_create_raw(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    data = client.bundle.create(submission_id)

    assert data[:4] == b'CART'


def test_import(datastore, client):
    submission_id = random_id_from_collection(datastore, 'submission')
    tested_bundle = "/tmp/bundle_{}".format(submission_id)

    try:
        client.bundle.create(submission_id, tested_bundle)

        # Test failure to import because already exists
        with pytest.raises(ClientError):
            client.bundle.import_bundle(tested_bundle, min_classification="RESTRICTED")

        # Test import with exist_ok
        client.bundle.import_bundle(tested_bundle, exist_ok=True)

        # Delete submission
        datastore.delete_submission_tree(submission_id)
        datastore.submission.commit()

        # Test normal import
        client.bundle.import_bundle(tested_bundle)

        assert datastore.submission.get(submission_id) is not None
    finally:
        os.unlink(tested_bundle)
