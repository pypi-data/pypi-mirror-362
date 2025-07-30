import http

import pytest

from h2o_secure_store.clients.base.workspace import DEFAULT_WORKSPACE
from h2o_secure_store.clients.secret.client import SecretClient
from h2o_secure_store.clients.secret_version.client import SecretVersionClient
from h2o_secure_store.clients.secret_version.secret_version import SecretVersion
from h2o_secure_store.exception import CustomApiException


def test_get_secret_version(
        delete_secret_rows_before,
        secret_user,
        user_secret_version_client: SecretVersionClient,
):
    secret_version = user_secret_version_client.create_secret_version(
        parent=secret_user.name,
        secret_version=SecretVersion(
            value=b"secret_value"
        ),
    )

    secret_version_get = user_secret_version_client.get_secret_version(
        name=f"{DEFAULT_WORKSPACE}/secrets/{secret_user.get_secret_id()}/versions/{secret_version.get_secret_version_id()}"
    )

    assert secret_version_get.name == f"workspaces/{secret_user.get_workspace_id()}/secrets/{secret_user.get_secret_id()}/versions/{secret_version.get_secret_version_id()}"
    assert secret_version_get.value == b""  # Value is not returned in the response.
    assert secret_version_get.creator == secret_version.creator
    assert secret_version_get.create_time == secret_version.create_time
    assert secret_version_get.uid == secret_version.uid


def test_get_latest_secret_version(
        delete_secret_rows_before,
        secret_user,
        user_secret_version_client: SecretVersionClient,
):
    user_secret_version_client.create_secret_version(
        parent=secret_user.name,
        secret_version=SecretVersion(
            value=b"secret_value"
        ),
    )

    latest_secret_version = user_secret_version_client.create_secret_version(
        parent=secret_user.name,
        secret_version=SecretVersion(
            value=b"secret_value"
        ),
    )

    secret_version_get = user_secret_version_client.get_secret_version(
        name=f"{DEFAULT_WORKSPACE}/secrets/{secret_user.get_secret_id()}/versions/latest"
    )

    assert secret_version_get.name == f"workspaces/{secret_user.get_workspace_id()}/secrets/{secret_user.get_secret_id()}/versions/{latest_secret_version.get_secret_version_id()}"


def test_get_secret_version_not_found(
        delete_secret_rows_before,
        secret_user,
        user_secret_version_client: SecretVersionClient,
):
    with pytest.raises(CustomApiException) as exc:
        user_secret_version_client.get_secret_version(
            name=f"{DEFAULT_WORKSPACE}/secrets/{secret_user.get_secret_id()}/versions/non-existent"
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_get_latest_secret_version_not_found(
        delete_secret_rows_before,
        secret_user,
        user_secret_version_client: SecretVersionClient,
):
    with pytest.raises(CustomApiException) as exc:
        user_secret_version_client.get_secret_version(
            name=f"{DEFAULT_WORKSPACE}/secrets/{secret_user.get_secret_id()}/versions/latest"
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_get_secret_version_not_found_parent(
        delete_secret_rows_before,
        user_secret_version_client: SecretVersionClient,
):
    with pytest.raises(CustomApiException) as exc:
        user_secret_version_client.get_secret_version(
            name=f"{DEFAULT_WORKSPACE}/secrets/non-existent/versions/non-existent"
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_get_secret_version_deleted_parent(
        delete_secret_rows_before,
        secret_user,
        user_secret_client: SecretClient,
        user_secret_version_client: SecretVersionClient,
):
    secret_version = user_secret_version_client.create_secret_version(
        parent=secret_user.name,
        secret_version=SecretVersion(
            value=b"secret_value"
        ),
    )
    user_secret_client.delete_secret(name=secret_user.name)

    with pytest.raises(CustomApiException) as exc:
        user_secret_version_client.get_secret_version(
            name=f"{DEFAULT_WORKSPACE}/secrets/{secret_user.get_secret_id()}/versions/{secret_version.get_secret_version_id()}"
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
