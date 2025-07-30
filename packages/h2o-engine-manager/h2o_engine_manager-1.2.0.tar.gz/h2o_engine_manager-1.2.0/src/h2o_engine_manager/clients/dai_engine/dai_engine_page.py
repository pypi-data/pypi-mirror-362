import pprint

from h2o_engine_manager.clients.dai_engine.client_info import ClientInfo
from h2o_engine_manager.clients.dai_engine.dai_engine import from_dai_engine_api_object
from h2o_engine_manager.gen.model.v1_list_dai_engines_response import (
    V1ListDAIEnginesResponse,
)


class DAIEnginesPage:
    """Class represents a list of DAIEngine objects together with a
    next_page_token and a total_size used for listing AI engines."""

    def __init__(
        self, client_info: ClientInfo, list_api_response: V1ListDAIEnginesResponse
    ) -> None:
        api_engines = list_api_response.dai_engines
        self.engines = []
        for api_engine in api_engines:
            self.engines.append(
                from_dai_engine_api_object(
                    client_info=client_info, api_engine=api_engine
                )
            )

        self.next_page_token = list_api_response.next_page_token
        self.total_size = list_api_response.total_size

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
