from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import get_connection
from h2o_engine_manager.clients.engine.engine import Engine
from h2o_engine_manager.clients.engine.page import EnginesPage
from h2o_engine_manager.gen.api.engine_service_api import EngineServiceApi
from h2o_engine_manager.gen.configuration import Configuration


class EngineClient:
    """EngineClient manages Engines."""

    def __init__(
        self,
        url: str,
        platform_token: str,
        platform_oidc_url: str,
        platform_oidc_client_id: str,
        platform_oidc_client_secret: Optional[str] = None,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes EngineClient.

        Args:
            url (str): URL of AI Engine Manager Gateway.
            platform_token (str): H2O.ai platform token.
            platform_oidc_url (str): Base URL of the platform_token OIDC issuer.
            platform_oidc_client_id (str): OIDC Client ID associated with the platform_token.
            platform_oidc_client_secret (str, optional): Optional OIDC Client Secret that issued the 'platform_token'.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """

        cfg = get_connection(
            aiem_url=url,
            refresh_token=platform_token,
            issuer_url=platform_oidc_url,
            client_id=platform_oidc_client_id,
            client_secret=platform_oidc_client_secret,
            verify_ssl=verify_ssl,
            ssl_ca_cert=ssl_ca_cert,
        )

        engine_cfg = Configuration(host=url)
        engine_cfg.verify_ssl = verify_ssl
        engine_cfg.ssl_ca_cert = ssl_ca_cert

        with TokenApiClient(
            engine_cfg, cfg.token_provider
        ) as engine_service_api_client:
            self.engine_service_api = EngineServiceApi(engine_service_api_client)

    def list_engines(
        self,
        workspace_id: str,
        page_size: int = 0,
        page_token: str = "",
        order_by: str = "",
        filter_expr: str = "",
    ) -> EnginesPage:
        list_response = self.engine_service_api.engine_service_list_engines(
            parent=f"workspaces/{workspace_id}",
            page_size=page_size,
            page_token=page_token,
            order_by=order_by,
            filter=filter_expr,
        )

        return EnginesPage(list_response)

    def list_all_engines(
        self, workspace_id: str, order_by: str = "", filter_expr: str = ""
    ) -> List[Engine]:
        all_engines: List[Engine] = []
        next_page_token = ""
        while True:
            engines_list = self.list_engines(
                workspace_id=workspace_id,
                page_size=0,
                page_token=next_page_token,
                order_by=order_by,
                filter_expr=filter_expr,
            )
            all_engines = all_engines + engines_list.engines
            next_page_token = engines_list.next_page_token
            if next_page_token == "":
                break

        return all_engines
