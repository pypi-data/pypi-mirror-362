import pprint

from h2o_engine_manager.clients.dai_engine_profile.dai_engine_profile import (
    from_api_object,
)
from h2o_engine_manager.gen.model.v1_list_assigned_dai_engine_profiles_response import (
    V1ListAssignedDAIEngineProfilesResponse,
)
from h2o_engine_manager.gen.model.v1_list_dai_engine_profiles_response import (
    V1ListDAIEngineProfilesResponse,
)


class DAIEngineProfilesPage:
    """
    Class represents a list of DAIEngineProfiles together with a next_page_token for listing all DAIEngineProfiles.
    """

    def __init__(self, list_api_response: V1ListDAIEngineProfilesResponse | V1ListAssignedDAIEngineProfilesResponse) -> None:
        api_objects = list_api_response.dai_engine_profiles
        self.dai_engine_profiles = []
        for api_profile in api_objects:
            self.dai_engine_profiles.append(from_api_object(api_profile))

        self.next_page_token = list_api_response.next_page_token

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
