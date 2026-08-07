import os

import requests
from assemblyline.odm.models.user import USER_ROLES_BASIC
from assemblyline.odm.models.apikey import get_apikey_id
from assemblyline.odm.random_data import DEV_APIKEY_NAME

from assemblyline_client import get_client
from conftest import UI_HOST


def _get_keycloak_access_token(
    client_id="assemblyline", client_secret="assemblyline", scope=None
):
    token_req = {
        "grant_type": "password",
        "username": "admin",
        "password": "admin",
        "client_secret": client_secret,
        "client_id": client_id,
    }
    if scope:
        token_req["scope"] = scope

    token_resp = requests.post(
        "http://localhost:8080/realms/master/protocol/openid-connect/token",
        data=token_req,
        timeout=30,
    )
    token_resp.raise_for_status()
    return token_resp.json()["access_token"]


def test_internal_auth():
    # Use the internal auth method to authenticate with the Assemblyline client
    client = get_client(UI_HOST, auth=("admin", "admin"), verify=False, retries=1)
    whoami = client.user.whoami()
    assert whoami["username"] == "admin"


def test_apikey_auth(datastore):
    # Use an API key to authenticate with the Assemblyline client
    apikey = datastore.apikey.get(get_apikey_id(DEV_APIKEY_NAME, "admin"))
    password = os.getenv("DEV_ADMIN_PASS", "admin") or "admin"
    apikey_auth = f"{apikey.key_name}:{password}"

    client = get_client(UI_HOST, apikey=("admin", apikey_auth), verify=False, retries=1)
    whoami = client.user.whoami()
    assert whoami["username"] == "admin"


def test_oauth_auth(datastore_connection):
    # Create the keycloak user for OAuth-related sign-ins
    datastore_connection.user.save(
        "admin-keycloak",
        {
            "uname": "admin-keycloak",
            "name": "Admin",
            "password": "__NO_PASSWORD__",
            "email": "admin@keycloak.com",
            "roles": USER_ROLES_BASIC,
        },
    )
    datastore_connection.user.commit()

    # Get the OAuth token from Keycloak and use it to authenticate with the Assemblyline client
    oauth_token = _get_keycloak_access_token(scope="openid email profile")

    client = get_client(UI_HOST, oauth=oauth_token, verify=False, retries=1)
    whoami = client.user.whoami()
    assert whoami["username"] == "admin-keycloak"
