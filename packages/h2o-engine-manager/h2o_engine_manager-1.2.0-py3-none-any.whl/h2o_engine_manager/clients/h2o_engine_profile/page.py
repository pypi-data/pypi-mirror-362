import pprint

from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile import (
    from_api_object,
)
from h2o_engine_manager.gen.model.v1_list_assigned_h2_o_engine_profiles_response import (
    V1ListAssignedH2OEngineProfilesResponse,
)
from h2o_engine_manager.gen.model.v1_list_h2_o_engine_profiles_response import (
    V1ListH2OEngineProfilesResponse,
)


class H2OEngineProfilesPage:
    """
    Class represents a list of H2OEngineProfiles together with a next_page_token for listing all H2OEngineProfiles.
    """

    def __init__(self, list_api_response: V1ListH2OEngineProfilesResponse | V1ListAssignedH2OEngineProfilesResponse) -> None:
        api_objects = list_api_response.h2o_engine_profiles
        self.h2o_engine_profiles = []
        for api_profile in api_objects:
            self.h2o_engine_profiles.append(from_api_object(api_profile))

        self.next_page_token = list_api_response.next_page_token

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
