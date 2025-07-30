import ssl

import pytest as pytest
import trustme as trustme
import urllib3
from pytest_httpserver import HTTPServer
from trustme import CA

from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.dai_engine.dai_engine_client import DAIEngineClient

LIST_DAI_ENGINES_RESPONSE_JSON = {
    "daiEngines": [],
    "nextPageToken": "",
    "totalSize": 0,
}


# Using guide from pytest-httpserver for running HTTPS server:
# https://pytest-httpserver.readthedocs.io/en/latest/howto.html#running-an-https-server


@pytest.fixture(scope="session")
def ca():
    return trustme.CA()


@pytest.fixture(scope="session")
def httpserver_ssl_context(ca):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_cert = ca.issue_cert("localhost")
    localhost_cert.configure_cert(context)
    return context


class MockTokenProvider:
    def __call__(self) -> str:
        return "access-token"


def test_local_certs_verify(httpserver: HTTPServer, ca: CA):
    # Given: server returns some valid response when listing DAIEngines
    httpserver.expect_request(uri="/v1/workspaces/default/daiEngines").respond_with_json(
        response_json=LIST_DAI_ENGINES_RESPONSE_JSON,
    )

    # When DAIEngineClient verifies CA certs from local PEM file
    with ca.cert_pem.tempfile() as ca_temp_path:
        client = DAIEngineClient(
            connection_config=(ConnectionConfig(
                aiem_url=httpserver.url_for(suffix=""),
                token_provider=MockTokenProvider(),
            )),
            default_workspace_id="default",
            verify_ssl=True,
            ssl_ca_cert=ca_temp_path,
        )

        # Then DAIEngineClient communicates with AIEM server without errors.
        response = client.list_engines(workspace_id="default")
        assert response.engines == []
        assert response.next_page_token == ""
        assert response.total_size == 0


def test_missing_certs_verify(httpserver: HTTPServer):
    # Given: server returns some valid response when listing DAIEngines
    httpserver.expect_request(uri="/v1/workspaces/default/daiEngines").respond_with_json(
        response_json=LIST_DAI_ENGINES_RESPONSE_JSON,
    )

    # When DAIEngineClient verifies CA certs but is missing the cert file
    client = DAIEngineClient(
        connection_config=(ConnectionConfig(
            aiem_url=httpserver.url_for(suffix=""),
            token_provider=MockTokenProvider(),
        )),
        default_workspace_id="default",
        verify_ssl=True,
        ssl_ca_cert=None,
    )

    # Then DAIEngineClient raises SSL error
    with pytest.raises(urllib3.exceptions.MaxRetryError) as err:
        client.list_engines(workspace_id="default")
    assert "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate" in str(
        err.value)


def test_missing_certs_no_verify(httpserver: HTTPServer):
    # Given: server returns some valid response when listing DAIEngines
    httpserver.expect_request(uri="/v1/workspaces/default/daiEngines").respond_with_json(
        response_json=LIST_DAI_ENGINES_RESPONSE_JSON,
    )

    # When DAIEngineClient does not have the cert file but does not verify certs
    client = DAIEngineClient(
        connection_config=(ConnectionConfig(
            aiem_url=httpserver.url_for(suffix=""),
            token_provider=MockTokenProvider(),
        )),
        default_workspace_id="default",
        verify_ssl=False,
        ssl_ca_cert=None,
    )

    # Then DAIEngineClient communicates with AIEM server without errors.
    response = client.list_engines(workspace_id="default")
    assert response.engines == []
    assert response.next_page_token == ""
    assert response.total_size == 0


def test_local_certs_no_verify(httpserver: HTTPServer, ca: CA):
    # Given: server returns some valid response when listing DAIEngines
    httpserver.expect_request(uri="/v1/workspaces/default/daiEngines").respond_with_json(
        response_json=LIST_DAI_ENGINES_RESPONSE_JSON,
    )

    # When DAIEngineClient does not verify CA certs but still provides certs file
    with ca.cert_pem.tempfile() as ca_temp_path:
        client = DAIEngineClient(
            connection_config=(ConnectionConfig(
                aiem_url=httpserver.url_for(suffix=""),
                token_provider=MockTokenProvider(),
            )),
            default_workspace_id="default",
            verify_ssl=False,
            ssl_ca_cert=ca_temp_path,
        )

        # Then DAIEngineClient communicates with AIEM server without errors.
        response = client.list_engines(workspace_id="default")
        assert response.engines == []
        assert response.next_page_token == ""
        assert response.total_size == 0
