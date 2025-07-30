import time

from h2o_secure_store.clients.secret_version.client import SecretVersionClient
from h2o_secure_store.clients.secret_version.secret_version import SecretVersion


def test_reveal_secret_version_rotated_key(
        delete_secret_rows_before,
        secret_user,
        user_secret_version_client: SecretVersionClient,
):
    v = user_secret_version_client.create_secret_version(
        parent=secret_user.name,
        secret_version=SecretVersion(
            value=b"secret_value"
        ),
    )

    user_secret_version_client.reveal_secret_version_value(
        name=v.name
    )

    # Wait for the key to be rotated
    time.sleep(5)

    user_secret_version_client.reveal_secret_version_value(
        name=v.name
    )