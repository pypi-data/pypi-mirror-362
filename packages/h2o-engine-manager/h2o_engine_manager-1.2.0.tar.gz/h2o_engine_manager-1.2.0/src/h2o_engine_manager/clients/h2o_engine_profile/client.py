from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile import (
    H2OEngineProfile,
)
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile import (
    from_api_object,
)
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile_config import (
    H2OEngineProfileConfig,
)
from h2o_engine_manager.clients.h2o_engine_profile.page import H2OEngineProfilesPage
from h2o_engine_manager.gen import ApiException
from h2o_engine_manager.gen.api.h2_o_engine_profile_service_api import (
    H2OEngineProfileServiceApi,
)
from h2o_engine_manager.gen.configuration import Configuration
from h2o_engine_manager.gen.model.v1_h2_o_engine_profile import V1H2OEngineProfile
from h2o_engine_manager.gen.model.v1_list_assigned_h2_o_engine_profiles_response import (
    V1ListAssignedH2OEngineProfilesResponse,
)
from h2o_engine_manager.gen.model.v1_list_h2_o_engine_profiles_response import (
    V1ListH2OEngineProfilesResponse,
)


class H2OEngineProfileClient:
    """H2OEngineProfileClient manages H2OEngineProfiles."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes H2OEngineProfileClient.

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
            self.service_api = H2OEngineProfileServiceApi(api_client)

    def create_h2o_engine_profile(
        self,
        parent: str,
        h2o_engine_profile: H2OEngineProfile,
        h2o_engine_profile_id: str,
    ) -> H2OEngineProfile:
        """Standard Create method.

        Args:
            parent (str): Name of the profile's parent workspace. Format: `workspaces/*`.
            h2o_engine_profile (H2OEngineProfile): H2OEngineProfile to create.
            h2o_engine_profile_id (str): The ID to use for the H2OEngineProfile, which will form
                the profile's resource name.
                This value must:
                - contain 1-63 characters
                - contain only lowercase alphanumeric characters or hyphen ('-')
                - start with an alphabetic character
                - end with an alphanumeric character
        Returns:
            H2OEngineProfile: created H2OEngineProfile.
        """
        created_api_object: V1H2OEngineProfile
        try:
            created_api_object = self.service_api.h2_o_engine_profile_service_create_h2_o_engine_profile(
                parent=parent,
                h2o_engine_profile_id=h2o_engine_profile_id,
                h2o_engine_profile=h2o_engine_profile.to_api_object(),
            ).h2o_engine_profile
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(created_api_object)

    def get_h2o_engine_profile(self, name: str) -> H2OEngineProfile:
        """Standard Get method.

        Args:
            name: Name of the H2OEngineProfile to retrieve. Format: `workspaces/*/h2oEngineProfiles/*`
        """
        api_object: V1H2OEngineProfile

        try:
            api_object = self.service_api.h2_o_engine_profile_service_get_h2_o_engine_profile(
                name_3=name
            ).h2o_engine_profile
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_h2o_engine_profiles(
        self,
        parent: str,
        page_size: int = 0,
        page_token: str = "",
    ) -> H2OEngineProfilesPage:
        """Standard list method.

        Args:
            parent (str): Name of the workspace from which to list profiles. Format: `workspaces/*`.
            page_size (int): Maximum number of H2OEngineProfiles to return in a response.
                If unspecified (or set to 0), at most 50 H2OEngineProfiles will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the H2OEngineProfilesPage.

        Returns:
            H2OEngineProfilesPage: H2OEngineProfilesPage object.
        """
        list_response: V1ListH2OEngineProfilesResponse

        try:
            list_response = (
                self.service_api.h2_o_engine_profile_service_list_h2_o_engine_profiles(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return H2OEngineProfilesPage(list_response)

    def list_assigned_h2o_engine_profiles(
            self,
            parent: str,
            page_size: int = 0,
            page_token: str = "",
    ) -> H2OEngineProfilesPage:
        """Returns assigned H2OEngineProfiles that match OIDC roles of the caller.
        Args:
            parent (str): Name of the workspace from which to list profiles. Format: `workspaces/*`.
            page_size (int): Maximum number of H2OEngineProfiles to return in a response.
                If unspecified (or set to 0), at most 50 H2OEngineProfiles will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the H2OEngineProfilesPage.
        Returns:
            H2OEngineProfilesPage: H2OEngineProfilesPage object.
        """
        list_response: V1ListAssignedH2OEngineProfilesResponse

        try:
            list_response = (
                self.service_api.h2_o_engine_profile_service_list_assigned_h2_o_engine_profiles(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return H2OEngineProfilesPage(list_response)

    def list_all_h2o_engine_profiles(self, parent: str) -> List[H2OEngineProfile]:
        """Help method for listing all H2OEngineProfiles.

        Args:
            parent (str): Name of the workspace from which to list profiles. Format: `workspaces/*`.
        """

        all_profiles: List[H2OEngineProfile] = []
        next_page_token = ""
        while True:
            profiles_page = self.list_h2o_engine_profiles(
                parent=parent,
                page_size=0,
                page_token=next_page_token,
            )
            all_profiles = all_profiles + profiles_page.h2o_engine_profiles
            next_page_token = profiles_page.next_page_token
            if next_page_token == "":
                break

        return all_profiles

    def list_all_assigned_h2o_engine_profiles(self, parent: str) -> List[H2OEngineProfile]:
        """Help method for listing all assigned H2OEngineProfiles.
        Args:
            parent (str): Name of the workspace from which to list assigned profiles. Format: `workspaces/*`.
        """

        all_profiles: List[H2OEngineProfile] = []
        next_page_token = ""
        while True:
            profiles_page = self.list_assigned_h2o_engine_profiles(
                parent=parent,
                page_size=0,
                page_token=next_page_token,
            )
            all_profiles = all_profiles + profiles_page.h2o_engine_profiles
            next_page_token = profiles_page.next_page_token
            if next_page_token == "":
                break

        return all_profiles

    def update_h2o_engine_profile(
        self,
        h2o_engine_profile: H2OEngineProfile,
        update_mask: str = "*",
    ) -> H2OEngineProfile:
        """Standard Update method.

        Args:
            h2o_engine_profile (H2OEngineProfile): profile to update.
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
                    - max_non_interaction_duration
                    - max_unused_duration
                    - configuration_override
                    - base_configuration
                    - config_editability
                    - yaml_pod_template_spec
                    - yaml_gpu_tolerations
                    - triton_enabled
                    - gpu_resource_name

                Default value "*" will update all updatable fields.

        Returns:
            H2OEngineProfile: Updated H2OEngineProfile.
        """
        updated_api_object: V1H2OEngineProfile

        try:
            updated_api_object = (
                self.service_api.h2_o_engine_profile_service_update_h2_o_engine_profile(
                    h2o_engine_profile_name=h2o_engine_profile.name,
                    update_mask=update_mask,
                    h2o_engine_profile=h2o_engine_profile.to_resource(),
                ).h2o_engine_profile
            )
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=updated_api_object)

    def delete_h2o_engine_profile(self, name: str) -> None:
        """Standard Delete method.

        Args:
            name (str): Name of the H2OEngineProfile to delete. Format is `workspaces/*/h2oEngineProfiles/*`
        """
        try:
            self.service_api.h2_o_engine_profile_service_delete_h2_o_engine_profile(
                name_3=name
            )
        except ApiException as e:
            raise CustomApiException(e)

    def delete_all_h2o_engine_profiles(self, parent: str) -> None:
        """Help method for deleting all H2OEngineProfiles in a specified parent workspace.

        Args:
            parent (str): Parent workspace name. Format is `workspaces/*`.
        """
        profiles = self.list_all_h2o_engine_profiles(parent=parent)
        for profile in profiles:
            self.delete_h2o_engine_profile(name=profile.name)

    def apply_h2o_engine_profile_configs(
        self,
        configs: List[H2OEngineProfileConfig],
        parent: str = "workspaces/global",
    ) -> List[H2OEngineProfile]:
        """
        Set all H2OEngineProfiles to a state defined in the configs in the specified parent workspace.
        H2OEngineProfiles that are not specified in the configs will be deleted in the specified parent workspace.
        H2OEngineProfiles that are specified in the configs will be recreated with the new values
            in the specified parent workspace.

        Args:
            configs: H2OEngineProfile configurations that should be applied.
            parent: Workspace name in which to apply configs. Format is `workspaces/*`.

        Returns: applied H2OEngineProfiles

        """
        self.delete_all_h2o_engine_profiles(parent=parent)

        for cfg in configs:
            self.create_h2o_engine_profile(
                parent=parent,
                h2o_engine_profile=cfg.to_h2o_engine_profile(),
                h2o_engine_profile_id=cfg.h2o_engine_profile_id,
            )

        return self.list_all_h2o_engine_profiles(parent=parent)

    def get_first_h2o_engine_profile(self, workspace: str) -> Optional[H2OEngineProfile]:
        resp = self.list_assigned_h2o_engine_profiles(parent=workspace)

        if len(resp.h2o_engine_profiles) == 0:
            return None

        return resp.h2o_engine_profiles[0]
