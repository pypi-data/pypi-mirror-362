import os
import ssl

import h2o_authn
import pytest
from requests.exceptions import ConnectionError

import h2o_engine_manager


@pytest.mark.skip(reason="discovery service is not in skaffold")
def test_login_args_provided():
    h2o_engine_manager.login(
        environment=os.getenv("AIEM_DISCOVERY_URL"),
        platform_token=os.getenv("PLATFORM_TOKEN_USER"),
    )


@pytest.mark.skip(reason="discovery service is not in skaffold")
def test_login_h2o_cli_config():
    h2o_engine_manager.login()


@pytest.mark.skip(reason="discovery service is not in skaffold")
def test_login_ssl_verify_false():
    h2o_engine_manager.login(verify_ssl=False)


@pytest.mark.skip(reason="discovery service is not in skaffold")
def test_login_ssl_verify_valid_cert(valid_ca_bundle):
    h2o_engine_manager.login(verify_ssl=True, ssl_ca_cert=valid_ca_bundle)


@pytest.mark.skip(reason="discovery service is not in skaffold")
def test_login_ssl_verify_invalid_cert(invalid_ca_bundle):
    with pytest.raises(ssl.SSLError):
        h2o_engine_manager.login(verify_ssl=True, ssl_ca_cert=invalid_ca_bundle)


@pytest.mark.skip(reason="discovery service is not in skaffold")
def test_login_token_provider():
    os.environ["H2O_CLOUD_ENVIRONMENT"] = os.getenv("AIEM_DISCOVERY_URL")

    tp = h2o_authn.TokenProvider(
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
        refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
    )
    h2o_engine_manager.login(token_provider=tp)


@pytest.mark.skip(reason="discovery service is not in skaffold")
def test_incorrect_url():
    with pytest.raises(ConnectionError):
        h2o_engine_manager.login_custom(
            endpoint="https://incorrect-url.com",
            refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
            issuer_url=os.getenv("PLATFORM_OIDC_URL"),
            client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
        )
