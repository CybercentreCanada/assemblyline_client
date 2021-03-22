
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

        with pytest.raises(ClientError):
            client.bundle.import_bundle(tested_bundle, min_classification="RESTRICTED")

        datastore.delete_submission_tree(submission_id)
        datastore.submission.commit()

        client.bundle.import_bundle(tested_bundle)

        assert datastore.submission.get(submission_id) is not None
    finally:
        os.unlink(tested_bundle)
