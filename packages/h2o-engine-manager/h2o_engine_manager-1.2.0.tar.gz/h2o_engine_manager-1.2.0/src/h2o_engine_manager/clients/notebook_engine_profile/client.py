from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine_profile.config import (
    NotebookEngineProfileConfig,
)
from h2o_engine_manager.clients.notebook_engine_profile.page import (
    NotebookEngineProfilesPage,
)
from h2o_engine_manager.clients.notebook_engine_profile.profile import (
    NotebookEngineProfile,
)
from h2o_engine_manager.clients.notebook_engine_profile.profile import from_api_object
from h2o_engine_manager.gen import ApiException
from h2o_engine_manager.gen.api.notebook_engine_profile_service_api import (
    NotebookEngineProfileServiceApi,
)
from h2o_engine_manager.gen.configuration import Configuration
from h2o_engine_manager.gen.model.v1_list_assigned_notebook_engine_profiles_response import (
    V1ListAssignedNotebookEngineProfilesResponse,
)
from h2o_engine_manager.gen.model.v1_list_notebook_engine_profiles_response import (
    V1ListNotebookEngineProfilesResponse,
)
from h2o_engine_manager.gen.model.v1_notebook_engine_profile import (
    V1NotebookEngineProfile,
)


class NotebookEngineProfileClient:
    """NotebookEngineProfileClient manages NotebookEngineProfiles."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes NotebookEngineProfileClient.

        Args:
            connection_config (ConnectionConfig): AIEM connection configuration object.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """

        configuration = Configuration(host=connection_config.aiem_url)
        configuration.verify_ssl = verify_ssl
        configuration.ssl_ca_cert = ssl_ca_cert

        with TokenApiClient(
            configuration, connection_config.token_provider
        ) as api_client:
            self.service_api = NotebookEngineProfileServiceApi(api_client)

    def create_notebook_engine_profile(
        self,
        parent: str,
        notebook_engine_profile: NotebookEngineProfile,
        notebook_engine_profile_id: str,
    ) -> NotebookEngineProfile:
        """Standard Create method.

        Args:
            parent (str): Name of the profile's parent workspace. Format: `workspaces/*`.
            notebook_engine_profile (NotebookEngineProfile): NotebookEngineProfile to create.
            notebook_engine_profile_id (str): The ID to use for the NotebookEngineProfile, which will form
                the profile's resource name.
                This value must:
                - contain 1-63 characters
                - contain only lowercase alphanumeric characters or hyphen ('-')
                - start with an alphabetic character
                - end with an alphanumeric character
        Returns:
            NotebookEngineProfile: created NotebookEngineProfile.
        """
        created_api_object: V1NotebookEngineProfile
        try:
            created_api_object = self.service_api.notebook_engine_profile_service_create_notebook_engine_profile(
                parent=parent,
                notebook_engine_profile_id=notebook_engine_profile_id,
                notebook_engine_profile=notebook_engine_profile.to_api_object(),
            ).notebook_engine_profile
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(created_api_object)

    def get_notebook_engine_profile(self, name: str) -> NotebookEngineProfile:
        """Standard Get method.

        Args:
            name: Name of the NotebookEngineProfile to retrieve. Format: `workspaces/*/notebookEngineProfiles/*`
        """
        api_object: V1NotebookEngineProfile

        try:
            api_object = self.service_api.notebook_engine_profile_service_get_notebook_engine_profile(
                name_7=name
            ).notebook_engine_profile
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_notebook_engine_profiles(
        self,
        parent: str,
        page_size: int = 0,
        page_token: str = "",
    ) -> NotebookEngineProfilesPage:
        """Standard list method.

        Args:
            parent (str): Name of the workspace from which to list profiles. Format: `workspaces/*`.
            page_size (int): Maximum number of NotebookEngineProfiles to return in a response.
                If unspecified (or set to 0), at most 50 NotebookEngineProfiles will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the NotebookEngineProfilesPage.

        Returns:
            NotebookEngineProfilesPage: NotebookEngineProfilesPage object.
        """
        list_response: V1ListNotebookEngineProfilesResponse

        try:
            list_response = (
                self.service_api.notebook_engine_profile_service_list_notebook_engine_profiles(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return NotebookEngineProfilesPage(list_response)

    def list_assigned_notebook_engine_profiles(
            self,
            parent: str,
            page_size: int = 0,
            page_token: str = "",
    ) -> NotebookEngineProfilesPage:
        """Returns assigned NotebookEngineProfiles that match OIDC roles of the caller.
        Args:
            parent (str): Name of the workspace from which to list profiles. Format: `workspaces/*`.
            page_size (int): Maximum number of NotebookEngineProfiles to return in a response.
                If unspecified (or set to 0), at most 50 NotebookEngineProfiles will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the NotebookEngineProfilesPage.
        Returns:
            NotebookEngineProfilesPage: NotebookEngineProfilesPage object.
        """
        list_response: V1ListAssignedNotebookEngineProfilesResponse

        try:
            list_response = (
                self.service_api.notebook_engine_profile_service_list_assigned_notebook_engine_profiles(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return NotebookEngineProfilesPage(list_response)

    def list_all_notebook_engine_profiles(self, parent: str) -> List[NotebookEngineProfile]:
        """Help method for listing all NotebookEngineProfiles.

        Args:
            parent (str): Name of the workspace from which to list profiles. Format: `workspaces/*`.
        """

        all_profiles: List[NotebookEngineProfile] = []
        next_page_token = ""
        while True:
            profiles_page = self.list_notebook_engine_profiles(
                parent=parent,
                page_size=0,
                page_token=next_page_token,
            )
            all_profiles = all_profiles + profiles_page.notebook_engine_profiles
            next_page_token = profiles_page.next_page_token
            if next_page_token == "":
                break

        return all_profiles

    def list_all_assigned_notebook_engine_profiles(self, parent: str) -> List[NotebookEngineProfile]:
        """Help method for listing all assigned NotebookEngineProfiles.
        Args:
            parent (str): Name of the workspace from which to list assigned profiles. Format: `workspaces/*`.
        """

        all_profiles: List[NotebookEngineProfile] = []
        next_page_token = ""
        while True:
            profiles_page = self.list_assigned_notebook_engine_profiles(
                parent=parent,
                page_size=0,
                page_token=next_page_token,
            )
            all_profiles = all_profiles + profiles_page.notebook_engine_profiles
            next_page_token = profiles_page.next_page_token
            if next_page_token == "":
                break

        return all_profiles

    def update_notebook_engine_profile(
        self,
        notebook_engine_profile: NotebookEngineProfile,
        update_mask: str = "*",
    ) -> NotebookEngineProfile:
        """Standard Update method.

        Args:
            notebook_engine_profile (NotebookEngineProfile): profile to update.
            update_mask (str): The field mask to use for the update.
                Allowed field paths are:
                    - display_name
                    - priority
                    - enabled
                    - assigned_oidc_roles_enabled
                    - assigned_oidc_roles
                    - max_running_engines
                    - cpu_constraint
                    - gpu_constraint
                    - memory_bytes_constraint
                    - storage_bytes_constraint
                    - max_idle_duration_constraint
                    - max_running_duration_constraint
                    - yaml_pod_template_spec
                    - yaml_gpu_tolerations
                    - storage_class_name
                    - gpu_resource_name

                Default value "*" will update all updatable fields.

        Returns:
            NotebookEngineProfile: Updated NotebookEngineProfile.
        """
        updated_api_object: V1NotebookEngineProfile

        try:
            updated_api_object = (
                self.service_api.notebook_engine_profile_service_update_notebook_engine_profile(
                    notebook_engine_profile_name=notebook_engine_profile.name,
                    update_mask=update_mask,
                    notebook_engine_profile=notebook_engine_profile.to_resource(),
                ).notebook_engine_profile
            )
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=updated_api_object)

    def delete_notebook_engine_profile(self, name: str) -> None:
        """Standard Delete method.

        Args:
            name (str): Name of the NotebookEngineProfile to delete. Format is `workspaces/*/notebookEngineProfiles/*`
        """
        try:
            self.service_api.notebook_engine_profile_service_delete_notebook_engine_profile(
                name_7=name
            )
        except ApiException as e:
            raise CustomApiException(e)

    def delete_all_notebook_engine_profiles(self, parent: str) -> None:
        """Help method for deleting all NotebookEngineProfiles in a specified parent workspace.

        Args:
            parent (str): Parent workspace name. Format is `workspaces/*`.
        """
        profiles = self.list_all_notebook_engine_profiles(parent=parent)
        for profile in profiles:
            self.delete_notebook_engine_profile(name=profile.name)

    def apply_notebook_engine_profile_configs(
        self,
        configs: List[NotebookEngineProfileConfig],
        parent: str = "workspaces/global",
    ) -> List[NotebookEngineProfile]:
        """
        Set all NotebookEngineProfiles to a state defined in the configs in the specified parent workspace.
        NotebookEngineProfiles that are not specified in the configs will be deleted in the specified parent workspace.
        NotebookEngineProfiles that are specified in the configs will be recreated with the new values
            in the specified parent workspace.

        Args:
            configs: NotebookEngineProfile configurations that should be applied.
            parent: Workspace name in which to apply configs. Format is `workspaces/*`.

        Returns: applied NotebookEngineProfiles

        """
        self.delete_all_notebook_engine_profiles(parent=parent)

        for cfg in configs:
            self.create_notebook_engine_profile(
                parent=parent,
                notebook_engine_profile=cfg.to_notebook_engine_profile(),
                notebook_engine_profile_id=cfg.notebook_engine_profile_id,
            )

        return self.list_all_notebook_engine_profiles(parent=parent)
