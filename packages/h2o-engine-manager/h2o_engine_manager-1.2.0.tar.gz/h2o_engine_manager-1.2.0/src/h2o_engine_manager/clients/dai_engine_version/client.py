from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.dai_engine_version.dai_engine_version_config import (
    DAIEngineVersionConfig,
)
from h2o_engine_manager.clients.dai_engine_version.page import DAIEngineVersionsPage
from h2o_engine_manager.clients.dai_engine_version.version import DAIEngineVersion
from h2o_engine_manager.clients.dai_engine_version.version import from_api_object
from h2o_engine_manager.clients.dai_engine_version.version import from_api_objects
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.gen import ApiException
from h2o_engine_manager.gen.api.dai_engine_version_service_api import (
    DAIEngineVersionServiceApi,
)
from h2o_engine_manager.gen.configuration import Configuration
from h2o_engine_manager.gen.model.dai_engine_version_service_assign_dai_engine_version_aliases_request import (
    DAIEngineVersionServiceAssignDAIEngineVersionAliasesRequest,
)
from h2o_engine_manager.gen.model.v1_assign_dai_engine_version_aliases_response import (
    V1AssignDAIEngineVersionAliasesResponse,
)
from h2o_engine_manager.gen.model.v1_dai_engine_version import V1DAIEngineVersion
from h2o_engine_manager.gen.model.v1_list_dai_engine_versions_response import (
    V1ListDAIEngineVersionsResponse,
)


class DAIEngineVersionClient:
    """DAIEngineVersionClient manages DAIEngineVersions."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes DAIEngineVersionClient.

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
            self.service_api = DAIEngineVersionServiceApi(api_client)

    def create_dai_engine_version(
        self,
        parent: str,
        dai_engine_version: DAIEngineVersion,
        dai_engine_version_id: str,
    ) -> DAIEngineVersion:
        """Standard Create method.

        Args:
            parent (str): Name of the version's parent workspace. Format: `workspaces/*`.
            dai_engine_version (DAIEngineVersion): DAIEngineVersion to create.
            dai_engine_version_id (str): Specify the DAIEngineVersion ID,
                which will become a part of the DAIEngineVersion resource name.
                It must:
                - be in semver format (more segments than three segments allowed)
                - contain max 63 characters
                Examples: "1.10.3", "1.10.3-alpha", "1.10.3.2", "1.10.3.2-alpha"
        Returns:
            DAIEngineVersion: created DAIEngineVersion.
        """
        created_api_object: V1DAIEngineVersion
        try:
            created_api_object = self.service_api.d_ai_engine_version_service_create_dai_engine_version(
                parent=parent,
                dai_engine_version_id=dai_engine_version_id,
                dai_engine_version=dai_engine_version.to_api_object(),
            ).dai_engine_version
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(created_api_object)

    def get_dai_engine_version(self, name: str) -> DAIEngineVersion:
        """Standard Get method.

        Args:
            name: Name of the DAIEngineVersion to retrieve. Format: `workspaces/*/daiEngineVersions/*`
        """
        api_object: V1DAIEngineVersion

        try:
            api_object = self.service_api.d_ai_engine_version_service_get_dai_engine_version(
                name_2=name
            ).dai_engine_version
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_dai_engine_versions(
        self,
        parent: str,
        page_size: int = 0,
        page_token: str = "",
    ) -> DAIEngineVersionsPage:
        """Standard list method.

        Args:
            parent (str): Name of the workspace from which to list versions. Format: `workspaces/*`.
            page_size (int): Maximum number of DAIEngineVersions to return in a response.
                If unspecified (or set to 0), at most 50 DAIEngineVersions will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the DAIEngineVersionsPage.

        Returns:
            DAIEngineVersionsPage: DAIEngineVersionsPage object.
        """
        list_response: V1ListDAIEngineVersionsResponse

        try:
            list_response = (
                self.service_api.d_ai_engine_version_service_list_dai_engine_versions(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return DAIEngineVersionsPage(list_response)

    def list_all_dai_engine_versions(self, parent: str) -> List[DAIEngineVersion]:
        """Help method for listing all DAIEngineVersions.

        Args:
            parent (str): Name of the workspace from which to list versions. Format: `workspaces/*`.
        """

        all_versions: List[DAIEngineVersion] = []
        next_page_token = ""
        while True:
            versions_page = self.list_dai_engine_versions(
                parent=parent,
                page_size=1000,
                page_token=next_page_token,
            )
            all_versions = all_versions + versions_page.dai_engine_versions
            next_page_token = versions_page.next_page_token
            if next_page_token == "":
                break

        return all_versions

    def update_dai_engine_version(
        self,
        dai_engine_version: DAIEngineVersion,
        update_mask: str = "*",
    ) -> DAIEngineVersion:
        """Standard Update method.

        Args:
            dai_engine_version (DAIEngineVersion): version to update.
            update_mask (str): The field mask to use for the update.
                Allowed field paths are:
                    - deprecated
                    - image
                    - image_pull_policy
                    - image_pull_secrets
                Default value "*" will update all updatable fields.

        Returns:
            DAIEngineVersion: Updated DAIEngineVersion.
        """
        updated_api_object: V1DAIEngineVersion

        try:
            updated_api_object = (
                self.service_api.d_ai_engine_version_service_update_dai_engine_version(
                    dai_engine_version_name=dai_engine_version.name,
                    update_mask=update_mask,
                    dai_engine_version=dai_engine_version.to_resource(),
                ).dai_engine_version
            )
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=updated_api_object)

    def delete_dai_engine_version(self, name: str) -> None:
        """Standard Delete method.

        Args:
            name (str): Name of the DAIEngineVersion to delete. Format is `workspaces/*/daiEngineVersions/*`
        """
        try:
            self.service_api.d_ai_engine_version_service_delete_dai_engine_version(
                name_2=name
            )
        except ApiException as e:
            raise CustomApiException(e)

    def delete_all_dai_engine_versions(self, parent: str) -> None:
        """Help method for deleting all DAIEngineVersions in a specified parent workspace.

        Args:
            parent (str): Parent workspace name. Format is `workspaces/*`.
        """
        versions = self.list_all_dai_engine_versions(parent=parent)
        for version in versions:
            self.delete_dai_engine_version(name=version.name)

    def assign_dai_engine_version_aliases(
        self,
        name: str,
        aliases: Optional[List[str]] = None
    ) -> List[DAIEngineVersion]:
        """
        Assign new set of resourceID aliases to DAIEngineVersion.
        This will replace existing DAIEngineVersion resourceID aliases with the new aliases.
        If there are other DAIEngineVersions with the same alias that we try to assign to this DAIEngineVersion,
        they will be deleted from the other DAIEngineVersions.

        Example 1 - two versions in the same workspace:
        - daiw1v1(name="workspaces/w1/daiEngineVersions/v1", aliases=["latest", "bar"])
        - daiw1v2(name="workspaces/w1/daiEngineVersions/v2", aliases=["baz", "foo"])
        - AssignAliases(daiw1v1, aliases=["latest", "baz"])
        => daiw1v1.aliases=["latest", "baz"] (changed)
        => daiw1v2.aliases=["foo"] (changed)

        Example 2 - two versions in different workspaces:
        - daiw1v1(name="workspaces/w1/daiEngineVersions/v1", aliases=["latest", "bar"])
        - daiw2v1(name="workspaces/w2/daiEngineVersions/v1", aliases=["latest", "baz"])
        - AssignAliases(daiw1v1, aliases=["latest", "baz"])
        => daiw1v1.aliases=["latest", "baz"] (changed)
        => daiw2v1.aliases=["latest", "baz"] (unchanged)

        Args:
            name: DAIEngineVersion resource name. Format is `workspaces/*/daiEngineVersions/*`.
            aliases: New resourceID aliases of the DAIEngineVersion.

        Returns: all DAIEngineVersions from the same workspace.
        """
        if aliases is None:
            aliases = []

        response: V1AssignDAIEngineVersionAliasesResponse

        try:
            response = self.service_api.d_ai_engine_version_service_assign_dai_engine_version_aliases(
                name=name,
                body=DAIEngineVersionServiceAssignDAIEngineVersionAliasesRequest(
                    aliases=aliases,
                ),
            )
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_objects(api_objects=response.dai_engine_versions)

    def apply_dai_engine_version_configs(
        self,
        configs: List[DAIEngineVersionConfig],
        parent: str = "workspaces/global",
    ) -> List[DAIEngineVersion]:
        """
        Set all DAIEngineVersions to a state defined in the configs in the specified parent workspace.
        DAIEngineVersions that are not specified in the configs will be deleted in the specified parent workspace.
        DAIEngineVersions that are specified in the configs will be recreated with the new values
            in the specified parent workspace.

        Args:
            configs: DAIEngineVersion configurations that should be applied.
            parent: Workspace name in which to apply configs. Format is `workspaces/*`.

        Returns: applied DAIEngineVersions

        """
        self.delete_all_dai_engine_versions(parent=parent)

        for cfg in configs:
            self.create_dai_engine_version(
                parent=parent,
                dai_engine_version=cfg.to_dai_engine_version(),
                dai_engine_version_id=cfg.dai_engine_version_id,
            )

        return self.list_all_dai_engine_versions(parent=parent)

    def get_first_dai_engine_version(self, workspace: str) -> Optional[DAIEngineVersion]:
        resp = self.list_dai_engine_versions(parent=workspace)

        if len(resp.dai_engine_versions) == 0:
            return None

        return resp.dai_engine_versions[0]
