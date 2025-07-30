import http
import time
from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.exception import TimeoutException
from h2o_engine_manager.clients.notebook_engine.engine import NotebookEngine
from h2o_engine_manager.clients.notebook_engine.engine import (
    notebook_engine_from_api_object,
)
from h2o_engine_manager.clients.notebook_engine.engine import (
    notebook_engine_to_api_object,
)
from h2o_engine_manager.clients.notebook_engine.engine import (
    notebook_engine_to_resource,
)
from h2o_engine_manager.clients.notebook_engine.page import NotebookEnginesPage
from h2o_engine_manager.gen import ApiException
from h2o_engine_manager.gen import Configuration
from h2o_engine_manager.gen.api.notebook_engine_service_api import (
    NotebookEngineServiceApi,
)
from h2o_engine_manager.gen.model.v1_list_notebook_engines_response import (
    V1ListNotebookEnginesResponse,
)
from h2o_engine_manager.gen.model.v1_notebook_engine import V1NotebookEngine


class NotebookEngineClient:
    """NotebookEngineClient manages NotebookEngines."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """
        Args:
            connection_config: AIEM connection configuration object.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """

        configuration = Configuration(host=connection_config.aiem_url)
        configuration.verify_ssl = verify_ssl
        configuration.ssl_ca_cert = ssl_ca_cert

        with TokenApiClient(
            configuration, connection_config.token_provider
        ) as api_client:
            self.service_api = NotebookEngineServiceApi(api_client)

    def create_notebook_engine(
        self,
        parent: str,
        notebook_engine: NotebookEngine,
        notebook_engine_id: str,
    ) -> NotebookEngine:
        """
        Create notebook engine.

        Args:
            parent (str): Name of the engine's parent workspace. Format: "workspaces/*".
            notebook_engine (NotebookEngine): NotebookEngine to create.
            notebook_engine_id (str): The ID to use for the NotebookEngine, which will form
                the engine's resource name.
                This value must:
                - contain 1-63 characters
                - contain only lowercase alphanumeric characters or hyphen ('-')
                - start with an alphabetic character
                - end with an alphanumeric character
        Returns:
            NotebookEngine: created NotebookEngine.
        """
        created_api_object: V1NotebookEngine
        try:
            created_api_object = self.service_api.notebook_engine_service_create_notebook_engine(
                parent=parent,
                notebook_engine=notebook_engine_to_api_object(notebook_engine=notebook_engine),
                notebook_engine_id=notebook_engine_id,
            ).notebook_engine
        except ApiException as e:
            raise CustomApiException(e)

        return notebook_engine_from_api_object(api_object=created_api_object)

    def get_notebook_engine(
        self,
        name: str,
    ) -> NotebookEngine:
        """
        Get notebook engine.

        Args:
            name: NotebookEngine resource name. Format: "workspaces/*/notebookEngines/*"
        Returns:
            NotebookEngine: notebook engine
        """

        api_object: V1NotebookEngine

        try:
            api_object = self.service_api.notebook_engine_service_get_notebook_engine(name_8=name).notebook_engine
        except ApiException as e:
            raise CustomApiException(e)

        return notebook_engine_from_api_object(api_object=api_object)

    def list_notebook_engines(
        self,
        parent: str,
        page_size: int = 0,
        page_token: str = "",
    ) -> NotebookEnginesPage:
        """Standard list method.

        Args:
            parent (str): Name of the workspace from which to list notebookEngines. Format: `workspaces/*`.
            page_size (int): Maximum number of NotebookEngines to return in a response.
                If unspecified (or set to 0), at most 50 NotebookEngines will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the NotebookEnginesPage.

        Returns:
            NotebookEnginesPage: NotebookEnginesPage object.
        """
        list_response: V1ListNotebookEnginesResponse

        try:
            list_response = (
                self.service_api.notebook_engine_service_list_notebook_engines(
                    parent=parent,
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return NotebookEnginesPage(list_api_response=list_response)

    def list_all_notebook_engines(self, parent: str) -> List[NotebookEngine]:
        """Help method for listing all NotebookEngines.

        Args:
            parent (str): Name of the workspace from which to list notebookEngines. Format: `workspaces/*`.
        """

        all_notebook_engines: List[NotebookEngine] = []
        next_page_token = ""
        while True:
            page = self.list_notebook_engines(
                parent=parent,
                page_size=1000,
                page_token=next_page_token,
            )
            all_notebook_engines = all_notebook_engines + page.notebook_engines
            next_page_token = page.next_page_token
            if next_page_token == "":
                break

        return all_notebook_engines

    def update_notebook_engine(
        self,
        notebook_engine: NotebookEngine,
        update_mask: str = "*",
    ) -> NotebookEngine:
        """Standard Update method.

        Args:
            notebook_engine (NotebookEngine): notebookEngine to update.
            update_mask (str): The field mask to use for the update.
                Allowed field paths are:
                    - profile
                    - notebook_image
                    - cpu
                    - gpu
                    - memory_bytes
                    - display_name
                    - max_idle_duration
                    - max_running_duration
                Default value "*" will update all updatable fields.

        Returns:
            NotebookEngine: Updated NotebookEngine.
        """
        updated_api_object: V1NotebookEngine

        try:
            updated_api_object = (
                self.service_api.notebook_engine_service_update_notebook_engine(
                    notebook_engine_name=notebook_engine.name,
                    update_mask=update_mask,
                    notebook_engine=notebook_engine_to_resource(notebook_engine=notebook_engine),
                ).notebook_engine
            )
        except ApiException as e:
            raise CustomApiException(e)

        return notebook_engine_from_api_object(api_object=updated_api_object)

    def delete_notebook_engine(
        self,
        name: str,
    ) -> None:
        """
        Start notebook engine deletion.
        Method returns instantly, but it may take some time until the engine is deleted.

        Args:
            name: NotebookEngine resource name. Format: "workspaces/*/notebookEngines/*"
        """
        try:
            self.service_api.notebook_engine_service_delete_notebook_engine(name_8=name)
        except ApiException as e:
            raise CustomApiException(e)

    def pause_notebook_engine(
        self,
        name: str,
    ) -> NotebookEngine:
        """
        Pause notebook engine.
        Method returns instantly, but it may take some time until the engine is paused.

        Args:
            name: NotebookEngine resource name. Format: "workspaces/*/notebookEngines/*"
        Returns: paused notebookEngine
        """
        api_engine: V1NotebookEngine

        try:
            api_engine = self.service_api.notebook_engine_service_pause_notebook_engine(
                name_1=name,
                body=None,
            ).notebook_engine
        except ApiException as e:
            raise CustomApiException(e)

        return notebook_engine_from_api_object(api_object=api_engine)

    def resume_notebook_engine(
        self,
        name: str,
    ) -> NotebookEngine:
        """
        Resume notebook engine.
        Method returns instantly, but it may take some time until the engine is running.

        Args:
            name: NotebookEngine resource name. Format: "workspaces/*/notebookEngines/*"
        Returns: resumed notebookEngine
        """
        api_engine: V1NotebookEngine

        try:
            api_engine = self.service_api.notebook_engine_service_resume_notebook_engine(
                name_1=name,
                body=None,
            ).notebook_engine
        except ApiException as e:
            raise CustomApiException(e)

        return notebook_engine_from_api_object(api_object=api_engine)

    def access_notebook_engine(
        self,
        name: str,
    ) -> str:
        """
        Returns the notebook engine access URI.

        Args:
            name: NotebookEngine resource name. Format: "workspaces/*/notebookEngines/*"
        Returns: The notebook engine access URI
        """

        try:
            uri = self.service_api.notebook_engine_service_access_notebook_engine(
                notebook_engine=name,
            ).uri
        except ApiException as e:
            raise CustomApiException(e)

        return uri

    def wait(self, name: str, timeout_seconds: Optional[float] = None) -> Optional[NotebookEngine]:
        """
        Blocks execution until the notebookEngine with the given name is in the process of reconciling
        or until it is no longer found.

        Args:
            name: NotebookEngine resource name for which to wait. Format: "workspaces/*/notebookEngines/*"
            timeout_seconds: Time limit in seconds for how long to wait.
        Returns: engine that has finished waiting or nothing, if engine is no longer found.
        """
        start = time.time()

        while True:
            try:
                engine = self.get_notebook_engine(name=name)

                if not engine.reconciling:
                    return engine

                if timeout_seconds is not None and time.time() - start > timeout_seconds:
                    raise TimeoutException()

                time.sleep(5)
            except CustomApiException as exc:
                if exc.status == http.HTTPStatus.NOT_FOUND:
                    return None

                raise exc
