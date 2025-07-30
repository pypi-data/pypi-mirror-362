import pprint

from h2o_engine_manager.clients.notebook_engine_profile.profile import from_api_object
from h2o_engine_manager.gen.model.v1_list_assigned_notebook_engine_profiles_response import (
    V1ListAssignedNotebookEngineProfilesResponse,
)
from h2o_engine_manager.gen.model.v1_list_notebook_engine_profiles_response import (
    V1ListNotebookEngineProfilesResponse,
)


class NotebookEngineProfilesPage:
    """
    Class represents a list of NotebookEngineProfiles together with a next_page_token for listing all NotebookEngineProfiles.
    """

    def __init__(self, list_api_response: V1ListNotebookEngineProfilesResponse | V1ListAssignedNotebookEngineProfilesResponse) -> None:
        api_objects = list_api_response.notebook_engine_profiles
        self.notebook_engine_profiles = []
        for api_profile in api_objects:
            self.notebook_engine_profiles.append(from_api_object(api_profile))

        self.next_page_token = list_api_response.next_page_token

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
