from typing import Dict
from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.convert import duration_convertor
from h2o_engine_manager.clients.convert import quantity_convertor
from h2o_engine_manager.clients.engine_id.generator import generate_engine_id_candidate
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.h2o_engine.client_info import ClientInfo
from h2o_engine_manager.clients.h2o_engine.h2o_engine import H2OEngine
from h2o_engine_manager.clients.h2o_engine.h2o_engine import build_api_engine_name
from h2o_engine_manager.clients.h2o_engine.h2o_engine import from_h2o_engine_api_object
from h2o_engine_manager.clients.h2o_engine.page import H2OEnginesPage
from h2o_engine_manager.clients.h2o_engine.size import H2OEngineSize
from h2o_engine_manager.clients.h2o_engine.size import H2OEngineSizeLimits
from h2o_engine_manager.clients.h2o_engine.size import h2o_engine_size_from_api_obj
from h2o_engine_manager.clients.h2o_engine_profile.client import H2OEngineProfileClient
from h2o_engine_manager.clients.h2o_engine_version.client import H2OEngineVersionClient
from h2o_engine_manager.gen import ApiException as H2OEngineApiException
from h2o_engine_manager.gen import Configuration
from h2o_engine_manager.gen.api.h2_o_engine_service_api import H2OEngineServiceApi
from h2o_engine_manager.gen.model.v1_calculate_h2_o_engine_size_compressed_dataset_request import (
    V1CalculateH2OEngineSizeCompressedDatasetRequest,
)
from h2o_engine_manager.gen.model.v1_calculate_h2_o_engine_size_compressed_dataset_response import (
    V1CalculateH2OEngineSizeCompressedDatasetResponse,
)
from h2o_engine_manager.gen.model.v1_calculate_h2_o_engine_size_raw_dataset_request import (
    V1CalculateH2OEngineSizeRawDatasetRequest,
)
from h2o_engine_manager.gen.model.v1_calculate_h2_o_engine_size_raw_dataset_response import (
    V1CalculateH2OEngineSizeRawDatasetResponse,
)
from h2o_engine_manager.gen.model.v1_h2_o_engine import V1H2OEngine
from h2o_engine_manager.gen.model.v1_h2_o_engine_size_limits import (
    V1H2OEngineSizeLimits,
)
from h2o_engine_manager.gen.model.v1_list_h2_o_engines_response import (
    V1ListH2OEnginesResponse,
)


class H2OEngineClient:
    """H2OEngineClient manages H2O engines."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        default_workspace_id: str,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes H2OEngineClient.
        Do not initialize manually, use `h2o_engine_manager.login()` instead.

        Args:
            connection_config (ConnectionConfig): AIEM connection configuration object.
            default_workspace_id (str): The default workspace ID which will client use to manipulate with H2O engines.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """
        self.default_workspace_id = default_workspace_id

        configuration = Configuration(host=connection_config.aiem_url)
        configuration.verify_ssl = verify_ssl
        configuration.ssl_ca_cert = ssl_ca_cert

        with TokenApiClient(
            configuration, connection_config.token_provider
        ) as api_client:
            api_instance = H2OEngineServiceApi(api_client)

        self.client_info = ClientInfo(
            url=connection_config.aiem_url,
            token_provider=connection_config.token_provider,
            api_instance=api_instance,
            ssl_ca_cert=ssl_ca_cert,
        )

        self.h2o_engine_profile_client = H2OEngineProfileClient(
            connection_config=connection_config,
            verify_ssl=verify_ssl,
            ssl_ca_cert=ssl_ca_cert,
        )

        self.h2o_engine_version_client = H2OEngineVersionClient(
            connection_config=connection_config,
            verify_ssl=verify_ssl,
            ssl_ca_cert=ssl_ca_cert,
        )

    def create_engine(
        self,
        engine_id: Optional[str] = None,
        node_count: Optional[int] = None,
        cpu: Optional[int] = None,
        gpu: Optional[int] = None,
        memory_bytes: Optional[str] = None,
        max_idle_duration: Optional[str] = None,
        max_running_duration: Optional[str] = None,
        workspace_id: str = "",
        display_name: str = "",
        annotations: Dict[str, str] = {},
        validate_only: bool = False,
        profile: str = "",
        h2o_engine_version: str = "",
    ) -> H2OEngine:
        """Creates H2O engine and initiates launch.

        Args:
            engine_id (str, optional): The ID to use for the H2O engine, which will become the final component of the engine's resource name.
                If left unspecified, the client will generate a random value.
                This value must:

                - contain 1-63 characters
                - contain only lowercase alphanumeric characters or hyphen ('-')
                - start with an alphabetic character
                - end with an alphanumeric character
            node_count (int, optional): Number of nodes of the H2O cluster.
                If not specified, a default value will be set by server.
            cpu (int, optional): The amount of [CPU units](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu) per node allocated for the engine.
                If not specified, a default value will be set by server.
            gpu (int, optional): Number of nvidia.com/gpu Kubernetes resource units per node.
                If not specified, a default value will be set by server.
            memory_bytes (str, optional): The amount of memory per node. Quantity of bytes. Example `8G`, `16Gi`.
                If not specified, a default value will be set by server.
                Detailed syntax:

                - [quantity] = [number][suffix]
                - [suffix] = [binarySI] | [decimalSI]
                - [binarySI] = Ki | Mi | Gi | Ti | Pi
                - [decimalSI] = k | M | G | T | P
            max_idle_duration (str, optional): Maximum time an engine can be idle. When exceeded, the engine will terminate. Must be specified as a number with `s` suffix. Example `3600s`.
                If not specified, a default value will be set by server.
            max_running_duration (str, optional):  Maximum time na engine can be running. When exceeded, the engine will terminate. Must be specified as a number with `s` suffix. Example `36000s`.
                If not specified, a default value will be set by server.
            workspace_id (str, optional): The workspace ID where the engine is to be created. Defaults to client's workspace_id default value.
            display_name (str): Human-readable name of the H2OEngine. Must contain at most 63 characters. Does not have to be unique.
            annotations (Dict[str, str], optional): Additional arbitrary metadata associated with the H2OEngine. Defaults to {}.
                Annotations are key/value pairs. The key must:

                - be 63 characters or less
                - begin and end with an alphanumeric character ([a-z0-9A-Z])
                - with dashes (-), underscores (_), dots (.), and alphanumerics between
                - regex used for validation is: `^[A-Za-z0-9]([-A-Za-z0-9_.]{0,61}[A-Za-z0-9])?$`
            validate_only (bool, optional): If set to True, server will validate the request, but no engine will be created. Defaults to False.
            profile (str): The resource name of the H2OEngineProfile that is used by this H2OEngine.
                Format is `workspaces/*/h2oEngineProfiles/*`.
            h2o_engine_version: H2OEngineVersion assigned to H2OEngine.
                Format: "workspaces/*/h2oEngineVersions/*".

        Returns:
            H2OEngine: H2O engine.
        """
        # Use client-wide workspace_id if no method value is provided.
        if workspace_id == "":
            workspace_id = self.default_workspace_id

        if memory_bytes is not None:
            memory_bytes = quantity_convertor.quantity_to_number_str(memory_bytes)

        if max_idle_duration is not None:
            max_idle_duration = duration_convertor.duration_to_seconds(
                max_idle_duration
            )

        if max_running_duration is not None:
            max_running_duration = duration_convertor.duration_to_seconds(
                max_running_duration
            )

        if engine_id is None:
            engine_id = self.generate_engine_id(display_name=display_name, workspace_id=workspace_id)

        if profile == "":
            first_profile = self.h2o_engine_profile_client.get_first_h2o_engine_profile(
                workspace="workspaces/global",
            )
            if first_profile is None:
                raise Exception("no profile available")
            profile = first_profile.name

        if h2o_engine_version == "":
            first_h2o_engine_version = self.h2o_engine_version_client.get_first_h2o_engine_version(
                workspace="workspaces/global",
            )
            if first_h2o_engine_version is None:
                raise Exception("no dai_engine_version available")
            h2o_engine_version = first_h2o_engine_version.name

        api_engine = V1H2OEngine(
            node_count=node_count,
            cpu=cpu,
            gpu=gpu,
            memory_bytes=memory_bytes,
            annotations=annotations,
            max_idle_duration=max_idle_duration,
            max_running_duration=max_running_duration,
            display_name=display_name,
            profile=profile,
            h2o_engine_version=h2o_engine_version,
        )

        parent_resource = f"workspaces/{workspace_id}"

        created_api_engine: V1H2OEngine

        try:
            created_api_engine = (
                self.client_info.api_instance.h2_o_engine_service_create_h2_o_engine(
                    parent=parent_resource,
                    h2o_engine_id=engine_id,
                    h2o_engine=api_engine,
                    validate_only=validate_only,
                ).h2o_engine
            )
        except H2OEngineApiException as e:
            raise CustomApiException(e)

        created_engine = from_h2o_engine_api_object(
            client_info=self.client_info, api_engine=created_api_engine
        )

        return created_engine

    def get_engine(self, engine_id: str, workspace_id: str = "") -> H2OEngine:
        """Returns a specific engine.

        Args:
            engine_id (str): The ID of an engine.
            workspace_id (str, optional): ID of the workspace. Defaults to client's workspace_id default value.

        Returns:
            H2OEngine: H2O engine.
        """

        if workspace_id == "":
            workspace_id = self.default_workspace_id

        api_response: V1ListH2OEnginesResponse

        try:
            api_engine = self.client_info.api_instance.h2_o_engine_service_get_h2_o_engine(
                name_4=build_api_engine_name(
                    workspace_id=workspace_id, engine_id=engine_id
                )
            ).h2o_engine
        except H2OEngineApiException as e:
            raise CustomApiException(e)

        return from_h2o_engine_api_object(
            client_info=self.client_info, api_engine=api_engine
        )

    def list_engines(
        self,
        workspace_id: str = "",
        page_size: int = 0,
        page_token: str = "",
        order_by: str = "",
        filter: str = "",
    ) -> H2OEnginesPage:
        """Returns a list of engines within a parent workspace.

        Args:
            workspace_id (str, optional): ID of the workspace. Defaults to H2OEngineClient's default value (`default` if not set).
            page_size (int, optional): Maximum number of H2OEngines to return in a response.
                If unspecified (or set to 0), at most 50 H2OEngines will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str, optional): Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the H2OEnginesPage.
            order_by (str, optional): Used to specify the sorting order.
                When unset, H2OEngines are ordered by their time of creation in
                descending order. This is equivalent to "create_time desc".
                When specified, the value must be a comma separated list of supported
                fields. The supported fields are:

                - name
                - cpu
                - gpu
                - memory_bytes
                - creator
                - create_time
                - update_time
                - delete_time
                - display_name
                - max_idle_duration
                - max_running_duration
                - uid

                The default sorting order is ascending. For example: "name" and "name asc" are equivalent values.
                To specify descending order for a field, append a " desc" suffix. For example: "name desc".
                Redundant space characters are insignificant. For example these values are all equal:

                - "  name, cpu     desc"
                - "name, cpu desc"
                - "name   , cpu desc   "

                Undefined (empty) time is interpreted as a zero time (0s since epoch, i.e. 1970-01-01T00:00:00Z).
                Undefined (empty) duration is interpreted as a zero duration (0 seconds).
            filter (str, optional): Used to filter H2OEngines.
                When unset, no filtering is applied.
                When specified, the filter string must follow this formatting rules:

                - filter expression: [term] AND [term] AND [term] ...
                - term: [filter_field] [operator] [value]
                - filter_field: (name|state|cpu|gpu|memory_bytes|creator|create_time|update_time|delete_time|reconciling|uid|display_name|max_idle_duration|max_running_duration|uid)
                - operator: (=|!=|<=|<|>=|>)
                - value: ([text]|[string])
                - text: free-form set of characters without whitespace (WS) or . (DOT) within it. (e.g. `28`, `abc`, `@5_6_7$`)
                - string: a quoted string. Text may contain whitespace (WS) or . (DOT) within it. (e.g. `"28"`, `"abc"`, `"@5_6_7$"`, `"   foo .  "`)

                Filter expression is case sensitive.
                Additional constraints:

                - You MUST use separator `<space>AND<space>` between terms.
                - String value MUST NOT contain `<space>AND<space>`.

                Each field may support only some operators:

                - string fields (name, creator, uid) support: =, !=, <=, <, >=, >
                - number fields (cpu, gpu, memory_bytes) support: =, !=, <=, <, >=, >
                - bool fields (reconciling) support: =, !=
                - enum fields (state) support: =, !=
                - time fields (create_time) support: =, !=, <=, <, >=, >

                Each field may expect values in a specified format:

                - string fields expect: text or string. For example `foo`, `"f oo"`. For example `f oo` is invalid.
                - number fields expect: numbers (can be wrapped in parentheses). For example: `28`, `-100`, `56.8`, `"666"`
                - integer number fields expect: integers. For example: `cpu = 10.5` is invalid.
                - bool fields expect: `true` or `false` literals. For example: `reconciling = true` is valid. `reconciling = 1` or `reconciling = TRUE` is invalid.
                - enum fields expect: enum's string representation. For example `state = STATE_RUNNING` is valid. `state = RUNNING` or `state = state_running` is invalid.
                - time fields expect: RFC-3339 formatted string. UTC offsets are supported. For example `2012-04-21T11:30:00-04:00` is valid. `2012-04-21` is invalid.

                Valid filter expression examples:

                - `state = STATE_RUNNING AND cpu <= 5 AND gpu != 0 AND create_time > 2012-04-21T11:30:00-04:00`
                - `state=STATE_RUNNING AND cpu<=5` (there may be no whitespace between term parts: `[filter_field][operator][value]`)

                Invalid filter expression examples:

                - `state = STATE_RUNNING    AND    cpu <= 5` (invalid separator between terms)
                - `state = STATE_RUNNING OR cpu <= 5` (unsupported logical operator)
                - `(state = STATE_RUNNING) AND (cpu <= 5)` (unsupported parentheses)

        Returns:
            H2OEnginesPage: A list of H2O engines together with a next_page_token for the next page.
        """
        if workspace_id == "":
            workspace_id = self.default_workspace_id

        parent_resource = f"workspaces/{workspace_id}"
        api_response: V1ListH2OEnginesResponse

        try:
            api_response = (
                self.client_info.api_instance.h2_o_engine_service_list_h2_o_engines(
                    parent=parent_resource,
                    page_size=page_size,
                    page_token=page_token,
                    order_by=order_by,
                    filter=filter,
                )
            )
        except H2OEngineApiException as e:
            raise CustomApiException(e)

        return H2OEnginesPage(
            client_info=self.client_info, list_api_response=api_response
        )

    def list_all_engines(
        self, workspace_id: str = "", order_by: str = "", filter: str = ""
    ) -> List[H2OEngine]:
        """Returns a list of all engines within a parent workspace.

        Args:
            workspace_id (str, optional): ID of the workspace. Defaults to client's default value (`default` if not set).
            order_by (str, optional): Identical to the list_engines function order_by parameter.
            filter (str, optional): Identical to the list_engines function filter parameter.

        Returns:
            List[H2OEngine]: A list of H2O engines.
        """
        if workspace_id == "":
            workspace_id = self.default_workspace_id

        all_engines: List[H2OEngine] = []
        next_page_token = ""
        while True:
            engines_list = self.list_engines(
                workspace_id=workspace_id,
                page_size=0,
                page_token=next_page_token,
                order_by=order_by,
                filter=filter,
            )
            all_engines = all_engines + engines_list.engines
            next_page_token = engines_list.next_page_token
            if next_page_token == "":
                break

        return all_engines

    def generate_engine_id(
        self,
        display_name: str,
        workspace_id: str,
    ) -> str:
        for n in range(50):
            engine_id_candidate = generate_engine_id_candidate(display_name=display_name, engine_type="h2o", attempt=n)
            try:
                self.get_engine(engine_id=engine_id_candidate, workspace_id=workspace_id)
            except CustomApiException as e:
                if e.status == 404:
                    return engine_id_candidate
                else:
                    continue

        raise Exception("Unable to generate random unused engine_id, please provide one manually.")

    def calculate_h2o_engine_size_raw_dataset(
        self,
        dataset_size_bytes: str,
        limits: H2OEngineSizeLimits,
    ) -> H2OEngineSize:
        """
        Calculate recommended engine size based on the raw size of the expected raw dataset size
        and given engine size limits.

        Args:
            dataset_size_bytes: raw size of the expected raw dataset size in bytes. Supports quantity suffixes.
                Examples values: "1000", "1Mi", "20Gi", "20G".
            limits: H2OEngine size limits

        Returns: recommended H2OEngine size
        """

        dataset_size_bytes_number_str = quantity_convertor.quantity_to_number_str(quantity=dataset_size_bytes)

        api_response: V1CalculateH2OEngineSizeRawDatasetResponse

        try:
            api_response = self.client_info.api_instance.h2_o_engine_service_calculate_h2_o_engine_size_raw_dataset(
                body=V1CalculateH2OEngineSizeRawDatasetRequest(
                    dataset_size_bytes=dataset_size_bytes_number_str,
                    limits=limits.h2o_engine_size_limits_to_api_obj()
                ),
            )
        except H2OEngineApiException as e:
            raise CustomApiException(e)

        return h2o_engine_size_from_api_obj(api_obj=api_response.h2o_engine_size)

    def calculate_h2o_engine_size_compressed_dataset(
        self,
        rows_count: int,
        columns_count: int,
        limits: H2OEngineSizeLimits,
    ) -> H2OEngineSize:
        """
        Calculate recommended engine size based on the dimensions of the compressed dataset
        and given engine size limits.

        Args:
            rows_count: number of rows of the compressed dataset
            columns_count: number of columns of the compressed dataset
            limits: H2OEngine size limits

        Returns: recommended H2OEngine size
        """

        api_instance = self.client_info.api_instance
        api_response: V1CalculateH2OEngineSizeCompressedDatasetResponse

        try:
            api_response = (api_instance.h2_o_engine_service_calculate_h2_o_engine_size_compressed_dataset(
                body=V1CalculateH2OEngineSizeCompressedDatasetRequest(
                    rows_count=str(rows_count),
                    columns_count=str(columns_count),
                    limits=limits.h2o_engine_size_limits_to_api_obj()
                ),
            ))
        except H2OEngineApiException as e:
            raise CustomApiException(e)

        return h2o_engine_size_from_api_obj(api_obj=api_response.h2o_engine_size)
