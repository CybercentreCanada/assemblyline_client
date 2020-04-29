import os
import pytest

UI_HOST = os.getenv('UI_HOST', "https://localhost:443")

try:
    from assemblyline.common.security import get_random_password
    from assemblyline.common.uid import get_random_id
    from passlib.hash import bcrypt

    from assemblyline_client import get_client
    from assemblyline.common import forge
    from assemblyline.odm import random_data

    config = forge.get_config()
    ds = forge.get_datastore(config)
    fs = forge.get_filestore(config)


    def purge_client():
        # Cleanup test data
        random_data.wipe_alerts(ds)
        random_data.wipe_heuristics(ds)
        random_data.wipe_services(ds)
        random_data.wipe_signatures(ds)
        random_data.wipe_submissions(ds, fs)
        random_data.wipe_users(ds)
        random_data.wipe_workflows(ds)


    @pytest.fixture(scope="session")
    def datastore(request):
        random_data.create_heuristics(ds, heuristics_count=10)
        random_data.create_services(ds)
        random_data.create_signatures(ds)
        random_data.create_users(ds)
        random_data.create_workflows(ds)
        submissions = []
        for _ in range(2):
            submissions.append(random_data.create_submission(ds, fs))
        random_data.create_alerts(ds, alert_count=10, submission_list=submissions)
        request.addfinalizer(purge_client)
        return ds


    @pytest.fixture(scope="module")
    def client():
        user = ds.user.get('admin')
        random_pass = get_random_password(length=48)
        key_name = "key_%s" % get_random_id().lower()
        user.apikeys[key_name] = {"password": bcrypt.hash(random_pass), "acl": ["R", "W"]}
        ds.user.save('admin', user)
        api_key = "%s:%s" % (key_name, random_pass)

        c = get_client(UI_HOST, apikey=('admin', api_key), verify=False)
        return c
except ImportError:
    import sys

    if sys.version_info < (3, 0):
        @pytest.fixture()
        def client():
            pytest.skip()

        @pytest.fixture()
        def datastore():
            pytest.skip()
    else:
        raise
