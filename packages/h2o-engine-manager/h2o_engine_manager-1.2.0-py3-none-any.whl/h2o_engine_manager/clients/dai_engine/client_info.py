from typing import Callable
from typing import Optional

from h2o_engine_manager.gen.api.dai_engine_service_api import DAIEngineServiceApi


class ClientInfo:
    """ClientInfo is a utility class grouping client-related data."""

    def __init__(
        self,
        url: str,
        token_provider: Callable[[], str],
        api_instance: DAIEngineServiceApi,
        ssl_ca_cert: Optional[str] = None
    ):
        """Initialize ClientInfo.

        Args:
            url (str): URL of the AIEM server.
            token_provider (Callable[[], str]): Token provider.
            api_instance (DAIEngineServiceApi): Instance of the generated DAIEngine service API client.
            ssl_ca_cert (str, optional): Path to a CA cert bundle with certificates of trusted CAs.
        """
        self.url = url
        self.token_provider = token_provider
        self.api_instance = api_instance
        self.ssl_ca_cert = ssl_ca_cert
