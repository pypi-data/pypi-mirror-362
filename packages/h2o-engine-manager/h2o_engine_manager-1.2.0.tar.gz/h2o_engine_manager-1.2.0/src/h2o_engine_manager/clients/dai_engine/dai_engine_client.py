from typing import Dict
from typing import List
from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.convert import duration_convertor
from h2o_engine_manager.clients.convert import quantity_convertor
from h2o_engine_manager.clients.dai_engine.client_info import ClientInfo
from h2o_engine_manager.clients.dai_engine.dai_engine import DAIEngine
from h2o_engine_manager.clients.dai_engine.dai_engine import from_dai_engine_api_object
from h2o_engine_manager.clients.dai_engine.dai_engine_page import DAIEnginesPage
from h2o_engine_manager.clients.dai_engine_profile.client import DAIEngineProfileClient
from h2o_engine_manager.clients.dai_engine_version.client import DAIEngineVersionClient
from h2o_engine_manager.clients.engine_id.generator import generate_engine_id_candidate
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.gen import ApiException as DAIEngineApiException
from h2o_engine_manager.gen.api.dai_engine_service_api import DAIEngineServiceApi
from h2o_engine_manager.gen.configuration import Configuration
from h2o_engine_manager.gen.model.v1_dai_engine import V1DAIEngine
from h2o_engine_manager.gen.model.v1_list_dai_engines_response import (
    V1ListDAIEnginesResponse,
)


class DAIEngineClient:
    """DAIEngineClient manages Driverless AI engines."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        default_workspace_id: str,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes DAIEngineClient.
        Do not initialize manually, use `h2o_engine_manager.login()` instead.

        Args:
            connection_config (ConnectionConfig): AIEM connection configuration object.
            default_workspace_id (str): The default workspace ID which will client use to manipulate with DAI engines.
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
            api_instance = DAIEngineServiceApi(api_client)

        self.client_info = ClientInfo(
            url=connection_config.aiem_url,
            token_provider=connection_config.token_provider,
            api_instance=api_instance,
            ssl_ca_cert=ssl_ca_cert,
        )

        self.dai_engine_profile_client = DAIEngineProfileClient(
            connection_config=connection_config,
            verify_ssl=verify_ssl,
            ssl_ca_cert=ssl_ca_cert,
        )

        self.dai_engine_version_client = DAIEngineVersionClient(
            connection_config=connection_config,
            verify_ssl=verify_ssl,
            ssl_ca_cert=ssl_ca_cert,
        )

    def set_default_workspace_id(self, default_workspace_id: str):
        """Sets default workspace for subsequest requests made by the client. Value can be overwritten by optional arguments of individual functions.

        Args:
            default_workspace_id (str): The workspace resource id to be used in subsequent requests.
        """
        self.default_workspace_id = default_workspace_id

    def create_engine(
        self,
        workspace_id: str = "",
        engine_id: Optional[str] = None,
        cpu: Optional[int] = None,
        gpu: Optional[int] = None,
        memory_bytes: Optional[str] = None,
        storage_bytes: Optional[str] = None,
        max_idle_duration: Optional[str] = None,
        max_running_duration: Optional[str] = None,
        display_name: str = "",
        config: Dict[str, str] = {},
        annotations: Dict[str, str] = {},
        validate_only: bool = False,
        profile: str = "",
        dai_engine_version: str = "",
    ) -> DAIEngine:
        """Creates Driverless AI engine and initiates launch. Immediately returned engine had just begun launching.

        Args:
            workspace_id (str, optional): The workspace ID where the engine is to be created.
                Defaults to DriverlessClients default value (`default` if not set).
            engine_id (str, optional): The ID to use for the Driverless AI engine,
                which will become the final component of the engine's resource name.
                If left unspecified, the client will generate a random value.
                This value must:
                    - contain 1-63 characters
                    - contain only lowercase alphanumeric characters or hyphen ('-')
                    - start with an alphabetic character
                    - end with an alphanumeric character
            cpu (int, optional): The amount of [CPU units](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu) allocated for the engine.
                If not specified, a default value will be set by server.
            gpu (int, optional): Number of nvidia.com/gpu Kubernetes resource units.
                If not specified, a default value will be set by server.
            memory_bytes (str, optional): Quantity of bytes.
                If not specified, a default value will be set by server.
                Example `8G`, `16Gi`. Detailed syntax:
                    - [quantity] = [number][suffix]
                    - [suffix] = [binarySI] | [decimalSI]
                    - [binarySI] = Ki | Mi | Gi | Ti | Pi
                    - [decimalSI] = k | M | G | T | P
            storage_bytes (str, optional): Quantity of bytes. Example `250G`, `2T`.
                Same syntax applies as `memory_bytes` parameter.
                If not specified, a default value will be set by server.
            max_idle_duration (str, optional): Maximum time an engine can be idle. When exceeded, the engine will pause.
                Must be specified as a number with `s` suffix. Example `3600s`.
                If not specified, a default value will be set by server.
            max_running_duration (str, optional):  Maximum time na engine can be running.
                When exceeded, the engine will pause. Must be specified as a number with `s` suffix. Example `36000s`.
                If not specified, a default value will be set by server.
            display_name (str): Human-readable name of the DAIEngine. Must contain at most 63 characters.
                Does not have to be unique.
            config (Dict[str, str], optional): Additional Driverless AI configuration.
            annotations (Dict[str, str], optional): Additional arbitrary metadata associated with the DAIEngine.
                Annotations are key/value pairs. The key must:
                    - be 63 characters or less
                    - begin and end with an alphanumeric character ([a-z0-9A-Z])
                    - with dashes (-), underscores (_), dots (.), and alphanumerics between
                    - regex used for validation is: `^[A-Za-z0-9]([-A-Za-z0-9_.]{0,61}[A-Za-z0-9])?$`
            validate_only (bool, optional): If set to True, server will validate the request,
                but no engine will be created. Defaults to False.
            profile: resource name of the DAIEngineProfile that is used by this DAIEngine.
                Format: "workspace/*/daiEngineProfiles/*".
                If unspecified, client will pick some profile.
            dai_engine_version: DAIEngineVersion assigned to DAIEngine.
                Format: "workspaces/*/daiEngineVersions/*".
                If unspecified, client will pick some version.

        Returns:
            DAIEngine: Driverless AI engine.
        """
        # Use client-wide workspace_id if no method value is provided.
        if workspace_id == "":
            workspace_id = self.default_workspace_id

        if engine_id is None:
            engine_id = self.generate_engine_id(display_name=display_name, workspace_id=workspace_id)

        if memory_bytes is not None:
            memory_bytes = quantity_convertor.quantity_to_number_str(memory_bytes)

        if storage_bytes is not None:
            storage_bytes = quantity_convertor.quantity_to_number_str(storage_bytes)

        if max_idle_duration is not None:
            max_idle_duration = duration_convertor.duration_to_seconds(
                max_idle_duration
            )

        if max_running_duration is not None:
            max_running_duration = duration_convertor.duration_to_seconds(
                max_running_duration
            )

        if profile == "":
            first_profile = self.dai_engine_profile_client.get_first_dai_engine_profile(
                workspace="workspaces/global",
            )
            if first_profile is None:
                raise Exception("no profile available")
            profile = first_profile.name

        if dai_engine_version == "":
            first_dai_engine_version = self.dai_engine_version_client.get_first_dai_engine_version(
                workspace="workspaces/global",
            )
            if first_dai_engine_version is None:
                raise Exception("no dai_engine_version available")
            dai_engine_version = first_dai_engine_version.name

        api_engine = V1DAIEngine(
            cpu=cpu,
            gpu=gpu,
            memory_bytes=memory_bytes,
            storage_bytes=storage_bytes,
            config=config,
            annotations=annotations,
            max_idle_duration=max_idle_duration,
            max_running_duration=max_running_duration,
            display_name=display_name,
            profile=profile,
            dai_engine_version=dai_engine_version,
        )
        parent_resource = f"workspaces/{workspace_id}"
        created_api_engine: V1DAIEngine

        try:
            created_api_engine = (
                self.client_info.api_instance.d_ai_engine_service_create_dai_engine(
                    parent_resource, engine_id, api_engine, validate_only=validate_only
                ).dai_engine
            )
        except DAIEngineApiException as e:
            raise CustomApiException(e)

        created_engine = from_dai_engine_api_object(
            client_info=self.client_info, api_engine=created_api_engine
        )

        return created_engine

    def get_engine(self, engine_id: str, workspace_id: str = "") -> DAIEngine:
        """Returns a specific engine.

        Args:
            engine_id (str): The ID of an engine.
            workspace_id (str, optional): ID of the workspace. Defaults to DAIEngineClient's default value (`default` if not set).

        Returns:
            DAIEngine: Driverless AI engine.
        """
        if workspace_id == "":
            workspace_id = self.default_workspace_id

        api_engine: V1DAIEngine

        try:
            api_engine = (
                self.client_info.api_instance.d_ai_engine_service_get_dai_engine(
                    name_1=self.__build_api_engine_name(
                        workspace_id=workspace_id, engine_id=engine_id
                    )
                ).dai_engine
            )
        except DAIEngineApiException as e:
            raise CustomApiException(e)

        return from_dai_engine_api_object(
            client_info=self.client_info, api_engine=api_engine
        )

    def list_engines(
        self,
        workspace_id: str = "",
        page_size: int = 0,
        page_token: str = "",
        order_by: str = "",
        filter: str = "",
    ) -> DAIEnginesPage:
        """Returns a list of engines within a parent workspace.

        Args:
            workspace_id (str, optional): ID of the workspace. Defaults to DAIEngineClient's default value (`default` if not set).
            page_size (int, optional): Maximum number of DAIEngines to return in a response.
                If unspecified (or set to 0), at most 50 DAIEngines will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str, optional): Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the DAIEnginesPage.
            order_by (str, optional): Used to specify the sorting order.
                When unset, DAIEngines are ordered by their time of creation in
                descending order. This is equivalent to "create_time desc".
                When specified, the value must be a comma separated list of supported
                fields. The supported fields are:

                - name
                - cpu
                - gpu
                - memory_bytes
                - storage_bytes
                - creator
                - create_time
                - update_time
                - delete_time
                - resume_time
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
            filter (str, optional): Used to filter DAIEngines.
                When unset, no filtering is applied.
                When specified, the filter string must follow this formatting rules:

                - filter expression: [term] AND [term] AND [term] ...
                - term: [filter_field] [operator] [value]
                - filter_field: (name|version|state|cpu|gpu|memory_bytes|storage_bytes|creator|create_time|update_time|delete_time|resume_time|reconciling|uid|display_name|max_idle_duration|max_running_duration|uid)
                - operator: (=|!=|<=|<|>=|>)
                - value: ([text]|[string])
                - text: free-form set of characters without whitespace (WS) or . (DOT) within it. (e.g. `28`, `abc`, `@5_6_7$`)
                - string: a quoted string. Text may contain whitespace (WS) or . (DOT) within it. (e.g. `"28"`, `"abc"`, `"@5_6_7$"`, `"   foo .  "`)

                Filter expression is case sensitive.
                Additional constraints:

                - You MUST use separator `<space>AND<space>` between terms.
                - String value MUST NOT contain `<space>AND<space>`.

                Each field may support only some operators:

                - string fields (name, version, creator, uid) support: =, !=, <=, <, >=, >
                - number fields (cpu, gpu, memory_bytes, storage_bytes) support: =, !=, <=, <, >=, >
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
            DAIEnginesPage: A list of Driverless AI engines together with a next_page_token for the next page.
        """
        if workspace_id == "":
            workspace_id = self.default_workspace_id

        parent_resource = f"workspaces/{workspace_id}"
        api_response: V1ListDAIEnginesResponse

        try:
            api_response = (
                self.client_info.api_instance.d_ai_engine_service_list_dai_engines(
                    parent=parent_resource,
                    page_size=page_size,
                    page_token=page_token,
                    order_by=order_by,
                    filter=filter,
                )
            )
        except DAIEngineApiException as e:
            raise CustomApiException(e)

        return DAIEnginesPage(
            client_info=self.client_info, list_api_response=api_response
        )

    def list_all_engines(
        self, workspace_id: str = "", order_by: str = "", filter: str = ""
    ) -> List[DAIEngine]:
        """Returns a list of all engines within a parent workspace.

        Args:
            workspace_id (str, optional): ID of the workspace. Defaults to DriverlessClients default value (`default` if not set).
            order_by (str, optional): Identical to the list_engines function order_by parameter.
            filter (str, optional): Identical to the list_engines function filter parameter.

        Returns:
            List[DAIEngine]: A list of Driverless AI engines.
        """
        if workspace_id == "":
            workspace_id = self.default_workspace_id

        all_engines: List[DAIEngine] = []
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

    def __build_api_engine_name(self, workspace_id: str, engine_id: str) -> str:
        """Function builds full resource name of an engine.
        Args:
            workspace_id (str): ID of the workspace.
            engine_id (str): The ID of an engine.
        Returns:
            str: Full resource name of an engine.
        """
        return f"workspaces/{workspace_id}/daiEngines/{engine_id}"

    def generate_engine_id(
        self,
        display_name: str,
        workspace_id: str,
    ) -> str:
        for n in range(50):
            engine_id_candidate = generate_engine_id_candidate(display_name=display_name, engine_type="dai", attempt=n)
            try:
                self.get_engine(engine_id=engine_id_candidate, workspace_id=workspace_id)
            except CustomApiException as e:
                if e.status == 404:
                    return engine_id_candidate
                else:
                    continue

        raise Exception("Unable to generate random unused engine_id, please provide one manually.")
