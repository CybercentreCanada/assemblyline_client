import os
import pytest


UI_HOST = os.getenv('UI_HOST', "https://localhost:443")

original_skip = pytest.skip

# Check if we are in an unattended build environment where skips won't be noticed
IN_CI_ENVIRONMENT = any(indicator in os.environ for indicator in
                        ['CI', 'BITBUCKET_BUILD_NUMBER', 'AGENT_JOBSTATUS'])


def skip_or_fail(message):
    """Skip or fail the current test, based on the environment"""
    if IN_CI_ENVIRONMENT:
        pytest.fail(message)
    else:
        original_skip(message)


# Replace the built in skip function with our own
pytest.skip = skip_or_fail


try:
    from assemblyline.common.security import get_random_password
    from assemblyline.datastore.store import ESStore
    from assemblyline.datastore.helper import AssemblylineDatastore
    from assemblyline.common.uid import get_random_id
    from passlib.hash import bcrypt

    from assemblyline_client import get_client
    from assemblyline.common import forge
    from assemblyline.odm import random_data

    config = forge.get_config()

    @pytest.fixture(scope='session')
    def filestore():
        try:
            return forge.get_filestore(config, connection_attempts=1)
        except ConnectionError as err:
            pytest.skip(str(err))

    @pytest.fixture(scope='session')
    def datastore_connection():
        store = ESStore(config.datastore.hosts)
        ret_val = store.ping()
        if not ret_val:
            pytest.skip("Could not connect to datastore")

        return AssemblylineDatastore(store)

    @pytest.fixture(scope="session")
    def datastore(datastore_connection, filestore):
        ds = datastore_connection
        try:
            random_data.create_heuristics(ds, heuristics_count=10)
            random_data.create_services(ds)
            random_data.create_signatures(ds)
            random_data.create_users(ds)
            random_data.create_workflows(ds)
            random_data.create_safelists(ds)
            submissions = []
            for _ in range(2):
                submissions.append(random_data.create_submission(ds, filestore))
            random_data.create_alerts(ds, alert_count=10, submission_list=submissions)
            yield ds
        finally:
            # Cleanup test data
            random_data.wipe_alerts(ds)
            random_data.wipe_heuristics(ds)
            random_data.wipe_safelist(ds)
            random_data.wipe_services(ds)
            random_data.wipe_signatures(ds)
            random_data.wipe_submissions(ds, filestore)
            random_data.wipe_users(ds)
            random_data.wipe_workflows(ds)

    @pytest.fixture(scope="module")
    def client(datastore):
        user = datastore.user.get('admin')
        random_pass = get_random_password(length=48)
        key_name = "key_%s" % get_random_id().lower()
        user.apikeys[key_name] = {"password": bcrypt.hash(random_pass), "acl": ["R", "W", "E"]}
        datastore.user.save('admin', user)
        api_key = "%s:%s" % (key_name, random_pass)

        c = get_client(UI_HOST, apikey=('admin', api_key), verify=False, retries=1)
        return c

except (ImportError, ModuleNotFoundError):
    import sys

    if sys.version_info < (3, 0):
        @pytest.fixture()
        def client():
            pytest.skip("This feature cannot be tested under python 2.x.")

        @pytest.fixture()
        def datastore():
            pytest.skip("This feature cannot be tested under python 2.x.")
    else:
        raise
