from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.h2o_engine_version.h2o_engine_version_config import (
    H2OEngineVersionConfig,
)
from h2o_engine_manager.clients.h2o_engine_version.page import H2OEngineVersionsPage
from h2o_engine_manager.clients.h2o_engine_version.version import H2OEngineVersion
from h2o_engine_manager.clients.h2o_engine_version.version import from_api_object
from h2o_engine_manager.clients.h2o_engine_version.version import from_api_objects
from h2o_engine_manager.gen import ApiException
from h2o_engine_manager.gen.api.h2_o_engine_version_service_api import (
    H2OEngineVersionServiceApi,
)
from h2o_engine_manager.gen.configuration import Configuration
from h2o_engine_manager.gen.model.h2_o_engine_version_service_assign_h2_o_engine_version_aliases_request import (
    H2OEngineVersionServiceAssignH2OEngineVersionAliasesRequest,
)
from h2o_engine_manager.gen.model.v1_assign_h2_o_engine_version_aliases_response import (
    V1AssignH2OEngineVersionAliasesResponse,
)
from h2o_engine_manager.gen.model.v1_h2_o_engine_version import V1H2OEngineVersion
from h2o_engine_manager.gen.model.v1_list_h2_o_engine_versions_response import (
    V1ListH2OEngineVersionsResponse,
)


class H2OEngineVersionClient:
    """H2OEngineVersionClient manages H2OEngineVersions."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes H2OEngineVersionClient.

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
            self.service_api = H2OEngineVersionServiceApi(api_client)

    def create_h2o_engine_version(
        self,
        parent: str,
        h2o_engine_version: H2OEngineVersion,
        h2o_engine_version_id: str,
    ) -> H2OEngineVersion:
        """Standard Create method.

        Args:
            parent (str): Name of the version's parent workspace. Format: `workspaces/*`.
            h2o_engine_version (H2OEngineVersion): H2OEngineVersion to create.
            h2o_engine_version_id (str): Specify the H2OEngineVersion ID,
                which will become a part of the H2OEngineVersion resource name.
                It must:
                - be in semver format (more segments than three segments allowed)
                - contain max 63 characters
                Examples: "1.10.3", "1.10.3-alpha", "1.10.3.2", "1.10.3.2-alpha"
        Returns:
            H2OEngineVersion: created H2OEngineVersion.
        """
        created_api_object: V1H2OEngineVersion
        try:
            created_api_object = self.service_api.h2_o_engine_version_service_create_h2_o_engine_version(
                parent=parent,
                h2o_engine_version_id=h2o_engine_version_id,
                h2o_engine_version=h2o_engine_version.to_api_object(),
            ).h2o_engine_version
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(created_api_object)

    def get_h2o_engine_version(self, name: str) -> H2OEngineVersion:
        """Standard Get method.

        Args:
            name: Name of the H2OEngineVersion to retrieve. Format: `workspaces/*/h2oEngineVersions/*`
        """
        api_object: V1H2OEngineVersion

        try:
            api_object = self.service_api.h2_o_engine_version_service_get_h2_o_engine_version(
                name_5=name
            ).h2o_engine_version
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_h2o_engine_versions(
        self,
        parent: str,
        page_size: int = 0,
        page_token: str = "",
    ) -> H2OEngineVersionsPage:
        """Standard list method.

        Args:
            parent (str): Name of the workspace from which to list versions. Format: `workspaces/*`.
            page_size (int): Maximum number of H2OEngineVersions to return in a response.
                If unspecified (or set to 0), at most 50 H2OEngineVersions will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the H2OEngineVersionsPage.

        Returns:
            H2OEngineVersionsPage: H2OEngineVersionsPage object.
        """
        list_response: V1ListH2OEngineVersionsResponse

        try:
            list_response = (
                self.service_api.h2_o_engine_version_service_list_h2_o_engine_versions(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return H2OEngineVersionsPage(list_response)

    def list_all_h2o_engine_versions(self, parent: str) -> List[H2OEngineVersion]:
        """Help method for listing all H2OEngineVersions.

        Args:
            parent (str): Name of the workspace from which to list versions. Format: `workspaces/*`.
        """

        all_versions: List[H2OEngineVersion] = []
        next_page_token = ""
        while True:
            versions_page = self.list_h2o_engine_versions(
                parent=parent,
                page_size=1000,
                page_token=next_page_token,
            )
            all_versions = all_versions + versions_page.h2o_engine_versions
            next_page_token = versions_page.next_page_token
            if next_page_token == "":
                break

        return all_versions

    def update_h2o_engine_version(
        self,
        h2o_engine_version: H2OEngineVersion,
        update_mask: str = "*",
    ) -> H2OEngineVersion:
        """Standard Update method.

        Args:
            h2o_engine_version (H2OEngineVersion): version to update.
            update_mask (str): The field mask to use for the update.
                Allowed field paths are:
                    - deprecated
                    - image
                    - image_pull_policy
                    - image_pull_secrets
                Default value "*" will update all updatable fields.

        Returns:
            H2OEngineVersion: Updated H2OEngineVersion.
        """
        updated_api_object: V1H2OEngineVersion

        try:
            updated_api_object = (
                self.service_api.h2_o_engine_version_service_update_h2_o_engine_version(
                    h2o_engine_version_name=h2o_engine_version.name,
                    update_mask=update_mask,
                    h2o_engine_version=h2o_engine_version.to_resource(),
                ).h2o_engine_version
            )
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=updated_api_object)

    def delete_h2o_engine_version(self, name: str) -> None:
        """Standard Delete method.

        Args:
            name (str): Name of the H2OEngineVersion to delete. Format is `workspaces/*/h2oEngineVersions/*`
        """
        try:
            self.service_api.h2_o_engine_version_service_delete_h2_o_engine_version(
                name_5=name
            )
        except ApiException as e:
            raise CustomApiException(e)

    def delete_all_h2o_engine_versions(self, parent: str) -> None:
        """Help method for deleting all H2OEngineVersions in a specified parent workspace.

        Args:
            parent (str): Parent workspace name. Format is `workspaces/*`.
        """
        versions = self.list_all_h2o_engine_versions(parent=parent)
        for version in versions:
            self.delete_h2o_engine_version(name=version.name)

    def assign_h2o_engine_version_aliases(
        self,
        name: str,
        aliases: Optional[List[str]] = None
    ) -> List[H2OEngineVersion]:
        """
        Assign new set of resourceID aliases to H2OEngineVersion.
        This will replace existing H2OEngineVersion resourceID aliases with the new aliases.
        If there are other H2OEngineVersions with the same alias that we try to assign to this H2OEngineVersion,
        they will be deleted from the other H2OEngineVersions.

        Example 1 - two versions in the same workspace:
        - h2ow1v1(name="workspaces/w1/h2oEngineVersions/v1", aliases=["latest", "bar"])
        - h2ow1v2(name="workspaces/w1/h2oEngineVersions/v2", aliases=["baz", "foo"])
        - AssignAliases(h2ow1v1, aliases=["latest", "baz"])
        => h2ow1v1.aliases=["latest", "baz"] (changed)
        => h2ow1v2.aliases=["foo"] (changed)

        Example 2 - two versions in different workspaces:
        - h2ow1v1(name="workspaces/w1/h2oEngineVersions/v1", aliases=["latest", "bar"])
        - h2ow2v1(name="workspaces/w2/h2oEngineVersions/v1", aliases=["latest", "baz"])
        - AssignAliases(h2ow1v1, aliases=["latest", "baz"])
        => h2ow1v1.aliases=["latest", "baz"] (changed)
        => h2ow2v1.aliases=["latest", "baz"] (unchanged)

        Args:
            name: H2OEngineVersion resource name. Format is `workspaces/*/h2oEngineVersions/*`.
            aliases: New resourceID aliases of the H2OEngineVersion.

        Returns: all H2OEngineVersions from the same workspace.
        """
        if aliases is None:
            aliases = []

        response: V1AssignH2OEngineVersionAliasesResponse

        try:
            response = self.service_api.h2_o_engine_version_service_assign_h2_o_engine_version_aliases(
                name_1=name,
                body=H2OEngineVersionServiceAssignH2OEngineVersionAliasesRequest(
                    aliases=aliases,
                ),
            )
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_objects(api_objects=response.h2o_engine_versions)

    def apply_h2o_engine_version_configs(
        self,
        configs: List[H2OEngineVersionConfig],
        parent: str = "workspaces/global",
    ) -> List[H2OEngineVersion]:
        """
        Set all H2OEngineVersions to a state defined in the configs in the specified parent workspace.
        H2OEngineVersions that are not specified in the configs will be deleted in the specified parent workspace.
        H2OEngineVersions that are specified in the configs will be recreated with the new values
            in the specified parent workspace.

        Args:
            configs: H2OEngineVersion configurations that should be applied.
            parent: Workspace name in which to apply configs. Format is `workspaces/*`.

        Returns: applied H2OEngineVersions

        """
        self.delete_all_h2o_engine_versions(parent=parent)

        for cfg in configs:
            self.create_h2o_engine_version(
                parent=parent,
                h2o_engine_version=cfg.to_h2o_engine_version(),
                h2o_engine_version_id=cfg.h2o_engine_version_id,
            )

        return self.list_all_h2o_engine_versions(parent=parent)

    def get_first_h2o_engine_version(self, workspace: str) -> Optional[H2OEngineVersion]:
        resp = self.list_h2o_engine_versions(parent=workspace)

        if len(resp.h2o_engine_versions) == 0:
            return None

        return resp.h2o_engine_versions[0]
