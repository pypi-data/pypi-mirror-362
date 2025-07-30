import pprint

from h2o_engine_manager.clients.engine.mapper import from_api_engine
from h2o_engine_manager.gen.model.v1_list_engines_response import V1ListEnginesResponse


class EnginesPage:
    """A list of Engines together with a next_page_token and a total_size for listing all Engines."""

    def __init__(self, list_api_response: V1ListEnginesResponse) -> None:
        generated_engines = list_api_response.engines
        self.engines = []
        for api_engine in generated_engines:
            self.engines.append(from_api_engine(api_engine))

        self.next_page_token = list_api_response.next_page_token
        self.total_size = list_api_response.total_size

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
