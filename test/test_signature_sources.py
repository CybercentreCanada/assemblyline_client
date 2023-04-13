try:
    from assemblyline.odm.random_data import random_model_obj
    from assemblyline.odm.models.service import UpdateSource

    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_add(datastore, client):
    # Select a random service
    service = random_id_from_collection(datastore, 'service_delta')

    # Make sure the service can generate signatures
    service_data = datastore.get_service_with_delta(service, as_obj=False)
    service_data['update_config'] = {'generates_signatures': True, 'sources': []}
    res = client.service.set(service, service_data)
    assert res['success']

    # Add a new source
    added_source_name = "NEW_TEST_SOURCE"
    new_source = random_model_obj(UpdateSource, as_json=True)
    new_source['name'] = added_source_name

    res = client.signature.sources.add(service, new_source)
    assert res['success']

    # Test if new source is there
    service_data = datastore.get_service_with_delta(service, as_obj=False)
    assert service_data['update_config']['sources'][0]['name'] == added_source_name


def test_delete(datastore, client):
    # Get the first service with a source
    sources = client.signature.sources()
    service = list(sources.keys())[0]

    # Delete all sources for the service
    for source in sources[service]["sources"]:
        res = client.signature.sources.delete(service, source['name'])
        assert res['success']

    datastore.service_delta.commit()

    # Test if the source was deleted
    service_data = datastore.get_service_with_delta(service, as_obj=False)
    assert service_data['update_config']['sources'] == []


def test_list(datastore, client):
    sources = client.signature.sources()
    assert isinstance(sources, dict)

    for name, srcs in sources.items():
        assert isinstance(name, str)
        assert isinstance(srcs["sources"], list)

        for src in srcs["sources"]:
            assert 'name' in src
            assert 'uri' in src


def test_update(datastore, client):
    new_uri = "HTTP://LOCALHOST/TEST_UPDATE"

    # Get the first service with a source
    sources = client.signature.sources()
    service = list(sources.keys())[0]

    # Update uri of all sources for the service
    for source in sources[service]["sources"]:
        source['uri'] = new_uri
        res = client.signature.sources.update(service, source['name'], source)
        assert res['success']

    # Test if the source was updated
    service_data = datastore.get_service_with_delta(service, as_obj=False)
    for source in service_data['update_config']['sources']:
        assert source['uri'] == new_uri
