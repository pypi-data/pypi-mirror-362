import pprint

from h2o_engine_manager.clients.h2o_engine_version.version import from_api_object
from h2o_engine_manager.gen.model.v1_list_h2_o_engine_versions_response import (
    V1ListH2OEngineVersionsResponse,
)


class H2OEngineVersionsPage:
    """
    Represents a list of H2OEngineVersions together with a next_page_token for listing all H2OEngineVersions.
    """

    def __init__(self, list_api_response: V1ListH2OEngineVersionsResponse) -> None:
        api_objects = list_api_response.h2o_engine_versions
        self.h2o_engine_versions = []
        for api_version in api_objects:
            self.h2o_engine_versions.append(from_api_object(api_version))

        self.next_page_token = list_api_response.next_page_token

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
