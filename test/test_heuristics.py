
try:
    from assemblyline.common import forge
    from utils import random_id_from_collection
except ImportError:
    import pytest
    import sys
    if sys.version_info < (3, 0):
        pytestmark = pytest.mark.skip
    else:
        raise


def test_get(datastore, client):
    heuristics_id = random_id_from_collection(datastore, 'heuristic')
    res = client.heuristics(heuristics_id)

    heuristic_data = datastore.heuristic.get(heuristics_id, as_obj=False)
    assert res['classification'] == heuristic_data['classification']
    assert res['description'] == heuristic_data['description']
    assert res['filetype'] == heuristic_data['filetype']
    assert res['heur_id'] == heuristic_data['heur_id']
    assert res['name'] == heuristic_data['name']


def test_stats(datastore, client):
    cache = forge.get_statistics_cache()
    cache.delete()

    res = client.heuristics.stats()
    assert len(res) == 0

    stats = datastore.calculate_heuristic_stats()
    cache.set('heuristics', stats)

    res = client.heuristics.stats()
    assert len(res) == datastore.heuristic.search('id:*')['total']
