import pprint
from datetime import datetime
from typing import Dict
from typing import Optional

from h2o_engine_manager.clients.engine.state import EngineState
from h2o_engine_manager.clients.engine.type import EngineType


class Engine:
    def __init__(
        self,
        name: str = "",
        uid: str = "",
        creator: str = "",
        creator_display_name: str = "",
        engine_type: EngineType = EngineType.TYPE_UNSPECIFIED,
        state: EngineState = EngineState.STATE_UNSPECIFIED,
        reconciling: bool = False,
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        delete_time: Optional[datetime] = None,
        resume_time: Optional[datetime] = None,
        login_url: str = "",
        annotations: Optional[Dict[str, str]] = None,
        display_name: str = "",
        version: str = "",
        deprecated_version: bool = False,
        deleted_version: bool = False,
        cpu: int = 0,
        gpu: int = 0,
        memory_bytes: str = "",
        storage_bytes: str = "",
        storage_resizing: bool = False,
        total_disk_size_bytes: Optional[str] = None,
        free_disk_size_bytes: Optional[str] = None,
        profile: str = "",
        visitable: bool = False,
    ) -> None:
        self.name = name
        self.uid = uid
        self.creator = creator
        self.creator_display_name = creator_display_name
        self.engine_type = engine_type
        self.state = state
        self.reconciling = reconciling
        self.create_time = create_time
        self.update_time = update_time
        self.delete_time = delete_time
        self.resume_time = resume_time
        self.login_url = login_url
        self.annotations = annotations
        self.display_name = display_name
        self.version = version
        self.deprecated_version = deprecated_version
        self.deleted_version = deleted_version
        self.cpu = cpu
        self.gpu = gpu
        self.memory_bytes = memory_bytes
        self.storage_bytes = storage_bytes
        self.storage_resizing = storage_resizing
        self.total_disk_size_bytes = total_disk_size_bytes
        self.free_disk_size_bytes = free_disk_size_bytes
        self.profile = profile
        self.visitable = visitable

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
