import http

import pytest

from h2o_secure_store.exception import CustomApiException


def test_delete_oauth_client(
    delete_all_oauth_clients_before_after,
    super_admin_oauth_client_client,
):
    super_admin_oauth_client_client.create_oauth_client(
        issuer="issuer1",
        client_id="client1",
        oauth_client_id="oauth-client1",
        authorization_endpoint="authz-endpoint",
        token_endpoint="token-endpoint",
    )

    super_admin_oauth_client_client.delete_oauth_client(
        oauth_client_id="oauth-client1",
    )

    with pytest.raises(CustomApiException) as exc:
        super_admin_oauth_client_client.get_oauth_client(
            oauth_client_id="oauth-client1",
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_delete_oauth_client_not_found(
    delete_all_oauth_clients_before_after,
    super_admin_oauth_client_client,
):
    with pytest.raises(CustomApiException) as exc:
        super_admin_oauth_client_client.delete_oauth_client(
            oauth_client_id="non-existing",
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
