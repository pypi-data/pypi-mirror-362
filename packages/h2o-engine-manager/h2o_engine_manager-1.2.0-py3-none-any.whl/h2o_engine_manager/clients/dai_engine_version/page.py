import pprint

from h2o_engine_manager.clients.dai_engine_version.version import from_api_object
from h2o_engine_manager.gen.model.v1_list_dai_engine_versions_response import (
    V1ListDAIEngineVersionsResponse,
)


class DAIEngineVersionsPage:
    """
    Represents a list of DAIEngineVersions together with a next_page_token for listing all DAIEngineVersions.
    """

    def __init__(self, list_api_response: V1ListDAIEngineVersionsResponse) -> None:
        api_objects = list_api_response.dai_engine_versions
        self.dai_engine_versions = []
        for api_version in api_objects:
            self.dai_engine_versions.append(from_api_object(api_version))

        self.next_page_token = list_api_response.next_page_token

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
