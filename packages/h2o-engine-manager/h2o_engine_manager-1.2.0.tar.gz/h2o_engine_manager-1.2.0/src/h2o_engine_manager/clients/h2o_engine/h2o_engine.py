import asyncio
import base64
import http
import pprint
import time
from datetime import datetime
from datetime import timezone
from typing import Dict
from typing import Optional
from urllib.parse import urlparse

from h2o_engine_manager.clients.convert import duration_convertor
from h2o_engine_manager.clients.convert import quantity_convertor
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.exception import FailedEngineException
from h2o_engine_manager.clients.exception import TimeoutException
from h2o_engine_manager.clients.h2o_engine.client_info import ClientInfo
from h2o_engine_manager.clients.h2o_engine.h2o_engine_version_info import (
    H2OEngineVersionInfo,
)
from h2o_engine_manager.clients.h2o_engine.h2o_engine_version_info import (
    from_h2o_engine_version_info_api_object,
)
from h2o_engine_manager.clients.h2o_engine.profile_info import H2OEngineProfileInfo
from h2o_engine_manager.clients.h2o_engine.profile_info import (
    from_h2o_engine_profile_info_api_obj,
)
from h2o_engine_manager.clients.h2o_engine.state import H2OEngineState
from h2o_engine_manager.clients.h2o_engine.state import final_states
from h2o_engine_manager.clients.h2o_engine.state import from_h2o_engine_state_api_object
from h2o_engine_manager.gen.exceptions import ApiException as H2OEngineApiException
from h2o_engine_manager.gen.model.v1_h2_o_engine import V1H2OEngine
from h2o_engine_manager.gen.model.v1_h2_o_engine_service_download_logs_response import (
    V1H2OEngineServiceDownloadLogsResponse,
)


class H2OClusterConnectionConfig(Dict):
    """Represents H2O cluster connection configuration object."""

    https: bool
    verify_ssl_certificates: bool
    cacert: str
    context_path: str
    ip: str
    port: int


class H2OEngine:
    def __init__(
        self,
        node_count: int,
        cpu: int,
        gpu: int,
        memory_bytes: str,
        annotations: Dict[str, str],
        max_idle_duration: str,
        max_running_duration: str,
        display_name: str,
        name: str = "",
        state: H2OEngineState = H2OEngineState.STATE_UNSPECIFIED,
        creator: str = "",
        creator_display_name: str = "",
        create_time: datetime = datetime.fromtimestamp(0, tz=timezone.utc),
        update_time: Optional[datetime] = None,
        delete_time: Optional[datetime] = None,
        login_url: str = "",
        api_url: str = "",
        reconciling: bool = False,
        uid: str = "",
        client_info: Optional[ClientInfo] = None,
        current_running_duration: Optional[str] = None,
        current_idle_duration: Optional[str] = None,
        profile: str = "",
        profile_info: Optional[H2OEngineProfileInfo] = None,
        h2o_engine_version: str = "",
        h2o_engine_version_info: Optional[H2OEngineVersionInfo] = None,
    ) -> None:
        self.node_count = node_count
        self.cpu = cpu
        self.gpu = gpu
        self.memory_bytes = memory_bytes
        self.annotations = annotations
        self.max_idle_duration = max_idle_duration
        self.max_running_duration = max_running_duration
        self.display_name = display_name

        self.name = name
        self.state = state
        self.creator = creator
        self.creator_display_name = creator_display_name
        self.create_time = create_time
        self.update_time = update_time
        self.delete_time = delete_time
        self.login_url = login_url
        self.api_url = api_url
        self.reconciling = reconciling
        self.uid = uid

        self.workspace_id = ""
        self.engine_id = ""
        if name:
            self.workspace_id = self.name.split("/")[1]
            self.engine_id = self.name.split("/")[3]

        self.client_info = client_info
        self.current_running_duration = current_running_duration
        self.current_idle_duration = current_idle_duration
        self.profile = profile
        self.profile_info = profile_info
        self.h2o_engine_version = h2o_engine_version
        self.h2o_engine_version_info = h2o_engine_version_info

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def terminate(self):
        """Terminates the engine and updates its data from the server response."""
        api_engine: V1H2OEngine

        if self.client_info is None:
            raise Exception("h2o_engine has None client_info")

        try:
            api_engine = (
                self.client_info.api_instance.h2_o_engine_service_terminate_h2_o_engine(
                    name=self.name,
                    body=None,
                ).h2o_engine
            )
        except H2OEngineApiException as e:
            raise CustomApiException(e)

        self.__update_data(api_engine)

    def delete(self, allow_missing: bool = False, validate_only: bool = False):
        """Initiates deletion of the engine from its workspace.
           Once the engine is deleted, any further action with the engine will result in an error.

        Args:
            allow_missing (bool, optional): When set to True and the H2OEngine
            is not found, then the request will succeed but no changes are made.
            validate_only(bool, optional): When set to True, request is
            validated but no changes are made.
        """
        api_engine: V1H2OEngine

        if self.client_info is None:
            raise Exception("h2o_engine has None client_info")

        try:
            api_engine = (
                self.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
                    name_4=self.name,
                    allow_missing=allow_missing,
                    validate_only=validate_only,
                )
            )
        except H2OEngineApiException as e:
            raise CustomApiException(e)

        if api_engine.h2o_engine is not None:
            self.__update_data(api_engine.h2o_engine)
        else:
            self.delete_time = datetime.now()
            self.state = H2OEngineState.STATE_DELETING

    def __update_data(self, engine: V1H2OEngine):
        if self.client_info is None:
            raise Exception("h2o_engine has None client_info")

        updated_engine = from_h2o_engine_api_object(
            client_info=self.client_info, api_engine=engine
        )

        self.__dict__.update(updated_engine.__dict__)

    def to_api_object(self) -> V1H2OEngine:
        mb = None
        if self.memory_bytes is not None:
            mb = quantity_convertor.quantity_to_number_str(self.memory_bytes)

        mid = None
        if self.max_idle_duration is not None:
            mid = duration_convertor.duration_to_seconds(self.max_idle_duration)

        mrd = None
        if self.max_running_duration is not None:
            mrd = duration_convertor.duration_to_seconds(self.max_running_duration)

        cid = None
        if self.current_idle_duration is not None:
            cid = duration_convertor.duration_to_seconds(self.current_idle_duration)

        crd = None
        if self.current_running_duration is not None:
            crd = duration_convertor.duration_to_seconds(self.current_running_duration)

        return V1H2OEngine._from_openapi_data(
            profile=self.profile,
            h2o_engine_version=self.h2o_engine_version,
            node_count=self.node_count,
            cpu=self.cpu,
            gpu=self.gpu,
            memory_bytes=mb,
            max_idle_duration=mid,
            max_running_duration=mrd,
            current_idle_duration=cid,
            current_running_duration=crd,
            display_name=self.display_name,
            name=self.name,
            state=self.state.to_api_object(),
            creator=self.creator,
            creator_display_name=self.creator_display_name,
            create_time=self.create_time,
            update_time=self.update_time,
            delete_time=self.delete_time,
            login_url=self.login_url,
            api_url=self.api_url,
            annotations=self.annotations,
            reconciling=self.reconciling,
            uid=self.uid,
        )

    def get_connection_config(
        self,
        https: bool = True,
        verify_ssl_certificates: bool = True,
        cacert: Optional[str] = "",
        port: int = 443,
    ) -> H2OClusterConnectionConfig:
        """Returns configuration used for h2o.connect.

        Args:
            https (bool): True to use https. False to use http.
            verify_ssl_certificates (bool): True to enable SSL certificate verification. False to disable.
            cacert (str, optional): Path to a CA cert bundle with certificates of trusted CAs. Defaults to CA bundle from the AIEM client login function
            port (int): Which port to connect to.
        """

        if self.state is not H2OEngineState.STATE_RUNNING:
            raise RuntimeError(
                f"H2OEngine {self.name} in not in a running state. Current state: {self.state}."
            )

        if self.client_info is None:
            raise Exception("h2o_engine has None client_info")

        if cacert == "" and self.client_info.ssl_ca_cert is not None:
            cacert = self.client_info.ssl_ca_cert

        return H2OClusterConnectionConfig(
            https=https,
            verify_ssl_certificates=verify_ssl_certificates,
            cacert=cacert,
            context_path=self.name,
            ip=urlparse(self.login_url).hostname,
            port=port,
        )

    def wait(self, timeout_seconds: Optional[float] = None):
        """Waits for the engine to reach a final (stable) state.

        Args:
            timeout_seconds (float, optional): Time limit in seconds for how
            long to wait. If no timeout is specified, function will be blocking
            until the waiting is finished. Potentially forever in case of an unexpected error.
            Defaults to None.
        """
        start = time.time()

        while True:
            if timeout_seconds is not None and time.time() - start > timeout_seconds:
                raise TimeoutException()

            time.sleep(5)
            if self.__is_in_final_state_and_update_exc():
                return

    async def wait_async(self, timeout_seconds: Optional[float] = None):
        """Waits for an engine to reach a final (stable) state.

        Args:
            timeout_seconds (float, optional): Time limit in seconds for how
            long to wait. If no timeout is specified, function will be blocking
            until the waiting is finished. Potentially forever in case of an unexpected error.
            Defaults to None.
        """
        start = time.time()

        while True:
            if timeout_seconds is not None and time.time() - start > timeout_seconds:
                raise TimeoutException()

            await asyncio.sleep(5)
            if self.__is_in_final_state_and_update_exc():
                return

    def download_logs(self) -> str:
        """Download H2O logs.
        Returns:
            H2O logs
        """
        resp: V1H2OEngineServiceDownloadLogsResponse

        if self.client_info is None:
            raise Exception("h2o_engine has None client_info")

        try:
            resp = self.client_info.api_instance.h2_o_engine_service_download_logs(
                h2o_engine=self.name, body=None
            )
        except H2OEngineApiException as e:
            raise CustomApiException(e)

        return base64.b64decode(resp.logs.data).decode("utf-8")

    def __is_in_final_state_and_update_exc(self) -> bool:
        result: bool

        try:
            result = self.__is_in_final_state_and_update()
        except H2OEngineApiException as e:
            raise CustomApiException(e)

        return result

    def __is_in_final_state_and_update(self) -> bool:
        """Returns True if engine is in final state. Potentially updates the calling engine as well."""
        engine = self.__get_or_none_if_not_found()
        if self.state == H2OEngineState.STATE_DELETING and engine is None:
            return True

        if engine is None:
            raise Exception("h2o_engine not found")

        # Always update pythonH2OEngine with the latest APIH2OEngine.
        self.__update_data(engine.h2o_engine)

        if self.__is_api_engine_in_final_state(engine):
            return True

        return False

    def __get_or_none_if_not_found(self) -> Optional[V1H2OEngine]:
        """Returns engine if found, None value if not found.

        Returns:
            engine: engine or None value.
        """
        if self.client_info is None:
            raise Exception("h2o_engine has None client_info")

        engine: V1H2OEngine
        try:
            engine = self.client_info.api_instance.h2_o_engine_service_get_h2_o_engine(
                name_4=self.name
            )
        except H2OEngineApiException as exc:
            if exc.status == http.HTTPStatus.NOT_FOUND:
                return None
            raise exc

        return engine

    def __is_api_engine_in_final_state(self, api_engine: V1H2OEngine) -> bool:
        """Returns True if API engine is in a final state.

        Args:
            api_engine (V1H2OEngine): API H2OEngine

        Raises:
            FailedEngineException: Raises exception when FAILED state is observed.

        Returns:
            bool: True if final state is observed, False otherwise.
        """
        if self.client_info is None:
            raise Exception("h2o_engine has None client_info")

        engine = from_h2o_engine_api_object(
            client_info=self.client_info, api_engine=api_engine.h2o_engine
        )
        if engine.state == H2OEngineState.STATE_FAILED:
            raise FailedEngineException()

        if engine.state in final_states():
            return True

        return False


def from_h2o_engine_api_object(
    client_info: ClientInfo, api_engine: V1H2OEngine
) -> H2OEngine:
    profile_info = None
    if api_engine.profile_info is not None:
        profile_info = from_h2o_engine_profile_info_api_obj(api_obj=api_engine.profile_info)

    h2o_engine_version_info = None
    if api_engine.h2o_engine_version_info is not None:
        h2o_engine_version_info = from_h2o_engine_version_info_api_object(
            api_object=api_engine.h2o_engine_version_info
        )

    return H2OEngine(
        node_count=api_engine.node_count,
        cpu=api_engine.cpu,
        gpu=api_engine.gpu,
        memory_bytes=quantity_convertor.number_str_to_quantity(api_engine.memory_bytes),
        annotations=api_engine.annotations,
        max_idle_duration=duration_convertor.seconds_to_duration(
            api_engine.max_idle_duration
        ),
        max_running_duration=duration_convertor.seconds_to_duration(
            api_engine.max_running_duration
        ),
        display_name=api_engine.display_name,
        name=api_engine.name,
        state=from_h2o_engine_state_api_object(api_engine.state),
        creator=api_engine.creator,
        creator_display_name=api_engine.creator_display_name,
        create_time=api_engine.create_time,
        update_time=api_engine.update_time,
        delete_time=api_engine.delete_time,
        login_url=api_engine.login_url,
        api_url=api_engine.api_url,
        reconciling=api_engine.reconciling,
        uid=api_engine.uid,
        client_info=client_info,
        current_idle_duration=duration_convertor.optional_seconds_to_duration(
            api_engine.current_idle_duration
        ),
        current_running_duration=duration_convertor.optional_seconds_to_duration(
            api_engine.current_running_duration
        ),
        profile=api_engine.profile,
        profile_info=profile_info,
        h2o_engine_version=api_engine.h2o_engine_version,
        h2o_engine_version_info=h2o_engine_version_info,
    )


def build_api_engine_name(workspace_id: str, engine_id: str) -> str:
    """Function builds full OpenAPI resource name of an engine.
    Args:
        workspace_id (str): ID of the workspace.
        engine_id (str): The ID of an engine.
    Returns:
        str: Full resource name of an engine.
    """

    return f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
