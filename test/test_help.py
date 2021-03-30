
def test_classification_definition(client):
    res = client.help.classification_definition()
    assert "RESTRICTED" in res
    assert "UNRESTRICTED" in res


def test_configuration(client):
    res = client.help.configuration()
    assert "services.categories" in res
    assert "services.stages" in res
    assert "ui.download_encoding" in res


def test_constants(client):
    res = client.help.constants()
    assert "file_types" in res
    assert "priorities" in res
    assert "tag_types" in res


def test_tos(client):
    res = client.help.tos()
    assert res is None
