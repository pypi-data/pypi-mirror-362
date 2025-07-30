from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.dai_engine_profile.dai_engine_profile import (
    DAIEngineProfile,
)
from h2o_engine_manager.clients.dai_engine_profile.dai_engine_profile import (
    from_api_object,
)
from h2o_engine_manager.clients.dai_engine_profile.dai_engine_profile_config import (
    DAIEngineProfileConfig,
)
from h2o_engine_manager.clients.dai_engine_profile.page import DAIEngineProfilesPage
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.gen import ApiException
from h2o_engine_manager.gen.api.dai_engine_profile_service_api import (
    DAIEngineProfileServiceApi,
)
from h2o_engine_manager.gen.configuration import Configuration
from h2o_engine_manager.gen.model.v1_dai_engine_profile import V1DAIEngineProfile
from h2o_engine_manager.gen.model.v1_list_assigned_dai_engine_profiles_response import (
    V1ListAssignedDAIEngineProfilesResponse,
)
from h2o_engine_manager.gen.model.v1_list_dai_engine_profiles_response import (
    V1ListDAIEngineProfilesResponse,
)


class DAIEngineProfileClient:
    """DAIEngineProfileClient manages DAIEngineProfiles."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes DAIEngineProfileClient.

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
            self.service_api = DAIEngineProfileServiceApi(api_client)

    def create_dai_engine_profile(
        self,
        parent: str,
        dai_engine_profile: DAIEngineProfile,
        dai_engine_profile_id: str,
    ) -> DAIEngineProfile:
        """Standard Create method.

        Args:
            parent (str): Name of the profile's parent workspace. Format: `workspaces/*`.
            dai_engine_profile (DAIEngineProfile): DAIEngineProfile to create.
            dai_engine_profile_id (str): The ID to use for the DAIEngineProfile, which will form
                the profile's resource name.
                This value must:
                - contain 1-63 characters
                - contain only lowercase alphanumeric characters or hyphen ('-')
                - start with an alphabetic character
                - end with an alphanumeric character
        Returns:
            DAIEngineProfile: created DAIEngineProfile.
        """
        created_api_object: V1DAIEngineProfile
        try:
            created_api_object = self.service_api.d_ai_engine_profile_service_create_dai_engine_profile(
                parent=parent,
                dai_engine_profile_id=dai_engine_profile_id,
                dai_engine_profile=dai_engine_profile.to_api_object(),
            ).dai_engine_profile
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(created_api_object)

    def get_dai_engine_profile(self, name: str) -> DAIEngineProfile:
        """Standard Get method.

        Args:
            name: Name of the DAIEngineProfile to retrieve. Format: `workspaces/*/daiEngineProfiles/*`
        """
        api_object: V1DAIEngineProfile

        try:
            api_object = self.service_api.d_ai_engine_profile_service_get_dai_engine_profile(
                name=name
            ).dai_engine_profile
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_dai_engine_profiles(
        self,
        parent: str,
        page_size: int = 0,
        page_token: str = "",
    ) -> DAIEngineProfilesPage:
        """Standard list method.

        Args:
            parent (str): Name of the workspace from which to list profiles. Format: `workspaces/*`.
            page_size (int): Maximum number of DAIEngineProfiles to return in a response.
                If unspecified (or set to 0), at most 50 DAIEngineProfiles will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the DAIEngineProfilesPage.

        Returns:
            DAIEngineProfilesPage: DAIEngineProfilesPage object.
        """
        list_response: V1ListDAIEngineProfilesResponse

        try:
            list_response = (
                self.service_api.d_ai_engine_profile_service_list_dai_engine_profiles(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return DAIEngineProfilesPage(list_response)

    def list_assigned_dai_engine_profiles(
            self,
            parent: str,
            page_size: int = 0,
            page_token: str = "",
    ) -> DAIEngineProfilesPage:
        """Returns assigned DAIEngineProfiles that match OIDC roles of the caller.

        Args:
            parent (str): Name of the workspace from which to list profiles. Format: `workspaces/*`.
            page_size (int): Maximum number of DAIEngineProfiles to return in a response.
                If unspecified (or set to 0), at most 50 DAIEngineProfiles will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the DAIEngineProfilesPage.

        Returns:
            DAIEngineProfilesPage: DAIEngineProfilesPage object.
        """
        list_response: V1ListAssignedDAIEngineProfilesResponse

        try:
            list_response = (
                self.service_api.d_ai_engine_profile_service_list_assigned_dai_engine_profiles(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return DAIEngineProfilesPage(list_response)

    def list_all_dai_engine_profiles(self, parent: str) -> List[DAIEngineProfile]:
        """Help method for listing all DAIEngineProfiles.

        Args:
            parent (str): Name of the workspace from which to list profiles. Format: `workspaces/*`.
        """

        all_profiles: List[DAIEngineProfile] = []
        next_page_token = ""
        while True:
            profiles_page = self.list_dai_engine_profiles(
                parent=parent,
                page_size=0,
                page_token=next_page_token,
            )
            all_profiles = all_profiles + profiles_page.dai_engine_profiles
            next_page_token = profiles_page.next_page_token
            if next_page_token == "":
                break

        return all_profiles

    def list_all_assigned_dai_engine_profiles(self, parent: str) -> List[DAIEngineProfile]:
        """Help method for listing all assigned DAIEngineProfiles.

        Args:
            parent (str): Name of the workspace from which to list assigned profiles. Format: `workspaces/*`.
        """

        all_profiles: List[DAIEngineProfile] = []
        next_page_token = ""
        while True:
            profiles_page = self.list_assigned_dai_engine_profiles(
                parent=parent,
                page_size=0,
                page_token=next_page_token,
            )
            all_profiles = all_profiles + profiles_page.dai_engine_profiles
            next_page_token = profiles_page.next_page_token
            if next_page_token == "":
                break

        return all_profiles

    def update_dai_engine_profile(
        self,
        dai_engine_profile: DAIEngineProfile,
        update_mask: str = "*",
    ) -> DAIEngineProfile:
        """Standard Update method.

        Args:
            dai_engine_profile (DAIEngineProfile): profile to update.
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
                    - data_directory_storage_class

                Default value "*" will update all updatable fields.

        Returns:
            DAIEngineProfile: Updated DAIEngineProfile.
        """
        updated_api_object: V1DAIEngineProfile

        try:
            updated_api_object = (
                self.service_api.d_ai_engine_profile_service_update_dai_engine_profile(
                    dai_engine_profile_name=dai_engine_profile.name,
                    update_mask=update_mask,
                    dai_engine_profile=dai_engine_profile.to_resource(),
                ).dai_engine_profile
            )
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=updated_api_object)

    def delete_dai_engine_profile(self, name: str) -> None:
        """Standard Delete method.

        Args:
            name (str): Name of the DAIEngineProfile to delete. Format is `workspaces/*/daiEngineProfiles/*`
        """
        try:
            self.service_api.d_ai_engine_profile_service_delete_dai_engine_profile(
                name=name
            )
        except ApiException as e:
            raise CustomApiException(e)

    def delete_all_dai_engine_profiles(self, parent: str) -> None:
        """Help method for deleting all DAIEngineProfiles in a specified parent workspace.

        Args:
            parent (str): Parent workspace name. Format is `workspaces/*`.
        """
        profiles = self.list_all_dai_engine_profiles(parent=parent)
        for profile in profiles:
            self.delete_dai_engine_profile(name=profile.name)

    def apply_dai_engine_profile_configs(
        self,
        configs: List[DAIEngineProfileConfig],
        parent: str = "workspaces/global",
    ) -> List[DAIEngineProfile]:
        """
        Set all DAIEngineProfiles to a state defined in the configs in the specified parent workspace.
        DAIEngineProfiles that are not specified in the configs will be deleted in the specified parent workspace.
        DAIEngineProfiles that are specified in the configs will be recreated with the new values
            in the specified parent workspace.

        Args:
            configs: DAIEngineProfile configurations that should be applied.
            parent: Workspace name in which to apply configs. Format is `workspaces/*`.

        Returns: applied DAIEngineProfiles

        """
        self.delete_all_dai_engine_profiles(parent=parent)

        for cfg in configs:
            self.create_dai_engine_profile(
                parent=parent,
                dai_engine_profile=cfg.to_dai_engine_profile(),
                dai_engine_profile_id=cfg.dai_engine_profile_id,
            )

        return self.list_all_dai_engine_profiles(parent=parent)

    def get_first_dai_engine_profile(self, workspace: str) -> Optional[DAIEngineProfile]:
        resp = self.list_assigned_dai_engine_profiles(parent=workspace)

        if len(resp.dai_engine_profiles) == 0:
            return None

        return resp.dai_engine_profiles[0]
