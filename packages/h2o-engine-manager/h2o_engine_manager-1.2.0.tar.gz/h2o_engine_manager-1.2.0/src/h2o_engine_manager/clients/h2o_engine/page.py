import pprint

from h2o_engine_manager.clients.h2o_engine.client_info import ClientInfo
from h2o_engine_manager.clients.h2o_engine.h2o_engine import from_h2o_engine_api_object
from h2o_engine_manager.gen.model.v1_list_h2_o_engines_response import (
    V1ListH2OEnginesResponse,
)


class H2OEnginesPage:
    """Class represents a list of H2OEngine objects together with a
    next_page_token and a total_size used for listing engines."""

    def __init__(
        self, client_info: ClientInfo, list_api_response: V1ListH2OEnginesResponse
    ) -> None:
        api_engines = list_api_response.h2o_engines
        self.engines = []
        for api_engine in api_engines:
            self.engines.append(
                from_h2o_engine_api_object(
                    client_info=client_info, api_engine=api_engine
                )
            )

        self.next_page_token = list_api_response.next_page_token
        self.total_size = list_api_response.total_size

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
