import random


def random_id_from_collection(ds, col_name, q=None):
    collection = ds.get_collection(col_name)
    if q is None:
        q = "id:*"
    return random.choice(collection.search(q, fl="id", rows=100, as_obj=False)['items'])['id']
