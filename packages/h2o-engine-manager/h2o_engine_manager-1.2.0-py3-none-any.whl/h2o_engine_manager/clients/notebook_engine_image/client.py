from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine_image.image import NotebookEngineImage
from h2o_engine_manager.clients.notebook_engine_image.image import from_api_object
from h2o_engine_manager.clients.notebook_engine_image.image_config import (
    NotebookEngineImageConfig,
)
from h2o_engine_manager.clients.notebook_engine_image.page import (
    NotebookEngineImagesPage,
)
from h2o_engine_manager.gen import ApiException
from h2o_engine_manager.gen.api.notebook_engine_image_service_api import (
    NotebookEngineImageServiceApi,
)
from h2o_engine_manager.gen.configuration import Configuration
from h2o_engine_manager.gen.model.v1_list_notebook_engine_images_response import (
    V1ListNotebookEngineImagesResponse,
)
from h2o_engine_manager.gen.model.v1_notebook_engine_image import V1NotebookEngineImage


class NotebookEngineImageClient:
    """NotebookEngineImageClient manages NotebookEngineImages."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes NotebookEngineImageClient.

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
            self.service_api = NotebookEngineImageServiceApi(api_client)

    def create_notebook_engine_image(
        self,
        parent: str,
        notebook_engine_image: NotebookEngineImage,
        notebook_engine_image_id: str,
    ) -> NotebookEngineImage:
        """Standard Create method.

        Args:
            parent (str): Name of the version's parent workspace. Format: `workspaces/*`.
            notebook_engine_image (NotebookEngineImage): NotebookEngineImage to create.
            notebook_engine_image_id (str): Specify the NotebookEngineImage ID,
                which will become a part of the NotebookEngineImage resource name.
                It must:
                    - contain 1-63 characters
                    - contain only lowercase alphanumeric characters or hyphen ('-')
                    - start with an alphabetic character
                    - end with an alphanumeric character

        Returns:
            NotebookEngineImage: created NotebookEngineImage.
        """
        created_api_object: V1NotebookEngineImage
        try:
            created_api_object = self.service_api.notebook_engine_image_service_create_notebook_engine_image(
                parent=parent,
                notebook_engine_image_id=notebook_engine_image_id,
                notebook_engine_image=notebook_engine_image.to_api_object(),
            ).notebook_engine_image
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(created_api_object)

    def get_notebook_engine_image(self, name: str) -> NotebookEngineImage:
        """Standard Get method.

        Args:
            name: Name of the NotebookEngineImage to retrieve. Format: `workspaces/*/NotebookEngineImages/*`
        """
        api_object: V1NotebookEngineImage

        try:
            api_object = self.service_api.notebook_engine_image_service_get_notebook_engine_image(
                name_6=name
            ).notebook_engine_image
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_notebook_engine_images(
        self,
        parent: str,
        page_size: int = 0,
        page_token: str = "",
    ) -> NotebookEngineImagesPage:
        """Standard list method.

        Args:
            parent (str): Name of the workspace from which to list versions. Format: `workspaces/*`.
            page_size (int): Maximum number of NotebookEngineImages to return in a response.
                If unspecified (or set to 0), at most 50 NotebookEngineImages will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the NotebookEngineImagesPage.

        Returns:
            NotebookEngineImagesPage: NotebookEngineImagesPage object.
        """
        list_response: V1ListNotebookEngineImagesResponse

        try:
            list_response = (
                self.service_api.notebook_engine_image_service_list_notebook_engine_images(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return NotebookEngineImagesPage(list_response)

    def list_all_notebook_engine_images(self, parent: str) -> List[NotebookEngineImage]:
        """Help method for listing all NotebookEngineImages.

        Args:
            parent (str): Name of the workspace from which to list versions. Format: `workspaces/*`.
        """

        all_versions: List[NotebookEngineImage] = []
        next_page_token = ""
        while True:
            versions_page = self.list_notebook_engine_images(
                parent=parent,
                page_size=1000,
                page_token=next_page_token,
            )
            all_versions = all_versions + versions_page.notebook_engine_images
            next_page_token = versions_page.next_page_token
            if next_page_token == "":
                break

        return all_versions

    def update_notebook_engine_image(
        self,
        notebook_engine_image: NotebookEngineImage,
        update_mask: str = "*",
    ) -> NotebookEngineImage:
        """Standard Update method.

        Args:
            notebook_engine_image (NotebookEngineImage): version to update.
            update_mask (str): The field mask to use for the update.
                Allowed field paths are:
                    - display_name
                    - enabled
                    - image
                    - image_pull_policy
                    - image_pull_secrets
                Default value "*" will update all updatable fields.

        Returns:
            NotebookEngineImage: Updated NotebookEngineImage.
        """
        updated_api_object: V1NotebookEngineImage

        try:
            updated_api_object = (
                self.service_api.notebook_engine_image_service_update_notebook_engine_image(
                    notebook_engine_image_name=notebook_engine_image.name,
                    update_mask=update_mask,
                    notebook_engine_image=notebook_engine_image.to_resource(),
                ).notebook_engine_image
            )
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=updated_api_object)

    def delete_notebook_engine_image(self, name: str) -> None:
        """Standard Delete method.

        Args:
            name (str): Name of the NotebookEngineImage to delete. Format is `workspaces/*/NotebookEngineImages/*`
        """
        try:
            self.service_api.notebook_engine_image_service_delete_notebook_engine_image(
                name_6=name
            )
        except ApiException as e:
            raise CustomApiException(e)

    def delete_all_notebook_engine_images(self, parent: str) -> None:
        """Help method for deleting all NotebookEngineImages in a specified parent workspace.

        Args:
            parent (str): Parent workspace name. Format is `workspaces/*`.
        """
        versions = self.list_all_notebook_engine_images(parent=parent)
        for version in versions:
            self.delete_notebook_engine_image(name=version.name)

    def apply_notebook_engine_image_configs(
        self,
        configs: List[NotebookEngineImageConfig],
        parent: str = "workspaces/global",
    ) -> List[NotebookEngineImage]:
        """
        Set all NotebookEngineImages to a state defined in the configs in the specified parent workspace.
        NotebookEngineImages that are not specified in the configs will be deleted in the specified parent workspace.
        NotebookEngineImages that are specified in the configs will be recreated with the new values
            in the specified parent workspace.

        Args:
            configs: NotebookEngineImage configurations that should be applied.
            parent: Workspace name in which to apply configs. Format is `workspaces/*`.

        Returns: applied NotebookEngineImages

        """
        self.delete_all_notebook_engine_images(parent=parent)

        for cfg in configs:
            self.create_notebook_engine_image(
                parent=parent,
                notebook_engine_image=cfg.to_notebook_engine_image(),
                notebook_engine_image_id=cfg.notebook_engine_image_id,
            )

        return self.list_all_notebook_engine_images(parent=parent)
