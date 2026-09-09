import random
from utils import random_id_from_collection

def test_get_submissions(datastore, client):
    subm = client.search.submission("*")

    sid = subm['items'][0]['sid']
    sha256 = subm['items'][0].full()['files'][0]['sha256']
    
    file = client.search.file("sha256:{}".format(sha256))['items'][0]

    assert file.get_submissions()[0]['sid'] == sid

def test_get_results(datastore, client):
    query = client.search.result("*")['items']
    result = query[random.randint(0, len(query)-1)]
    result_id = result['id']
    sha256 = result()['sha256']

    file = client.search.file("sha256:{}".format(sha256))['items'][0]
    results_wrapper = file.get_results()

    result_ids = [result['id'] for result in results_wrapper]

    assert result_id in result_ids

def test_get_extracted_files(datastore, client):
    query = client.search.result("*")['items']
    result = query[random.randint(0, len(query)-1)]()

    test_file = client.search.file(result['sha256'])['items'][0]
    datastore_extracted_files = result['response']['extracted']

    files_sha256 = [file['sha256'] for file in datastore_extracted_files]
    extracted_sha256 = [file['sha256'] for file in test_file.get_extracted_files()]

    for sha256 in files_sha256:
        assert sha256 in extracted_sha256

def test_get_submitted_files(datastore, client):
    query = client.search.submission("*")['items']
    subm = query[random.randint(0, len(query)-1)]
    assert len(subm.full()['files']) == len(subm.get_submitted_files())
