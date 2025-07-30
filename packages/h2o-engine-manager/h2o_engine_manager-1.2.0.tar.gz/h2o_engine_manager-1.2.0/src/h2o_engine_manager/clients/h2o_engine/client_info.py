from typing import Optional

import h2o_authn

from h2o_engine_manager.gen.api.h2_o_engine_service_api import H2OEngineServiceApi


class ClientInfo:
    """ClientInfo is a utility class grouping client-related data."""

    def __init__(
        self,
        url: str,
        token_provider: h2o_authn.TokenProvider,
        api_instance: H2OEngineServiceApi,
        ssl_ca_cert: Optional[str] = None
    ):
        """Initialize ClientInfo.

        Args:
            url (str): URL of the AIEM server.
            token_provider (h2o_authn.TokenProvider): Token provider.
            api_instance (H2OEngineServiceApi): Instance of the generated H2OEngine service API client.
            ssl_ca_cert (str, optional): Path to a CA cert bundle with certificates of trusted CAs.
        """
        self.url = url
        self.token_provider = token_provider
        self.api_instance = api_instance
        self.ssl_ca_cert = ssl_ca_cert
