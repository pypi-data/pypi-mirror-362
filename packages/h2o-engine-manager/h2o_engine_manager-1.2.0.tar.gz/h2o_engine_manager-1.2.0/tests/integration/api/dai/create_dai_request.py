from typing import Dict

from h2o_engine_manager.clients.dai_engine.dai_engine import DAIEngine
from h2o_engine_manager.clients.dai_engine.dai_engine_client import DAIEngineClient


class CreateDAIEngineRequest:
    """
    Help class for wrapping create arguments.
    """

    workspace_id: str
    engine_id: str
    version: str
    cpu: int
    gpu: int
    memory_bytes: str
    storage_bytes: str
    max_idle_duration: str
    max_running_duration: str
    display_name: str
    config: Dict[str, str]
    annotations: Dict[str, str]
    validate_only: bool

    def __init__(
        self,
        workspace_id: str = "create-dai",
        profile_id: str = None,
        engine_id: str = "engine1",
        version: str = "mock",
        cpu: int = 1,
        gpu: int = 0,
        memory_bytes: str = "1Gi",
        storage_bytes: str = "1Gi",
        max_idle_duration: str = "2h",
        max_running_duration: str = "12h",
        display_name: str = "",
        config: Dict[str, str] = {},
        annotations: Dict[str, str] = {},
        validate_only: bool = False,
    ):
        self.workspace_id = workspace_id
        self.profile_id = profile_id
        self.engine_id = engine_id
        self.version = version
        self.cpu = cpu
        self.gpu = gpu
        self.memory_bytes = memory_bytes
        self.storage_bytes = storage_bytes
        self.max_idle_duration = max_idle_duration
        self.max_running_duration = max_running_duration
        self.display_name = display_name
        self.config = config
        self.annotations = annotations
        self.validate_only = validate_only


def create_dai_from_request(
    dai_client: DAIEngineClient, req: CreateDAIEngineRequest
) -> DAIEngine:
    """
    Help function for creating engine via CreateDAIRequest.
    """
    return dai_client.create_engine(
        workspace_id=req.workspace_id,
        profile_id=req.profile_id,
        engine_id=req.engine_id,
        version=req.version,
        cpu=req.cpu,
        gpu=req.gpu,
        memory_bytes=req.memory_bytes,
        storage_bytes=req.storage_bytes,
        max_idle_duration=req.max_idle_duration,
        max_running_duration=req.max_running_duration,
        display_name=req.display_name,
        config=req.config,
        annotations=req.annotations,
        validate_only=req.validate_only,
    )
