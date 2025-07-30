import pprint
from datetime import datetime
from typing import Optional

from h2o_engine_manager.clients.convert.duration_convertor import (
    optional_duration_to_seconds,
)
from h2o_engine_manager.clients.convert.duration_convertor import (
    optional_seconds_to_duration,
)
from h2o_engine_manager.clients.convert.quantity_convertor import number_str_to_quantity
from h2o_engine_manager.clients.convert.quantity_convertor import (
    optional_quantity_to_number_str,
)
from h2o_engine_manager.clients.notebook_engine.failure_reson import (
    NotebookEngineFailureReason,
)
from h2o_engine_manager.clients.notebook_engine.failure_reson import (
    notebook_engine_failure_reason_from_api_object,
)
from h2o_engine_manager.clients.notebook_engine.notebook_engine_image_info import (
    NotebookEngineImageInfo,
)
from h2o_engine_manager.clients.notebook_engine.notebook_engine_image_info import (
    notebook_engine_image_info_from_api_object,
)
from h2o_engine_manager.clients.notebook_engine.notebook_engine_profile_info import (
    NotebookEngineProfileInfo,
)
from h2o_engine_manager.clients.notebook_engine.notebook_engine_profile_info import (
    notebook_engine_profile_info_from_api_object,
)
from h2o_engine_manager.clients.notebook_engine.state import NotebookEngineState
from h2o_engine_manager.clients.notebook_engine.state import (
    notebook_engine_state_from_api_object,
)
from h2o_engine_manager.gen.model.notebook_engine_resource import NotebookEngineResource
from h2o_engine_manager.gen.model.v1_notebook_engine import V1NotebookEngine


class NotebookEngine:
    """
    Engine that allows to run an interactive computing environment called notebook.
    """

    def __init__(
        self,
        profile: str,
        notebook_image: str,
        name: str = "",
        display_name: str = "",
        cpu: Optional[int] = None,
        gpu: Optional[int] = None,
        memory_bytes: Optional[str] = None,
        storage_bytes: Optional[str] = None,
        max_idle_duration: Optional[str] = None,
        max_running_duration: Optional[str] = None,
        state: NotebookEngineState = NotebookEngineState.STATE_UNSPECIFIED,
        reconciling: bool = False,
        uid: str = "",
        notebook_image_info: Optional[NotebookEngineImageInfo] = None,
        profile_info: Optional[NotebookEngineProfileInfo] = None,
        creator: str = "",
        updater: str = "",
        creator_display_name: str = "",
        updater_display_name: str = "",
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        resume_time: Optional[datetime] = None,
        delete_time: Optional[datetime] = None,
        current_idle_duration: Optional[str] = None,
        current_running_duration: Optional[str] = None,
        storage_class_name: str = "",
        failure_reason: NotebookEngineFailureReason = NotebookEngineFailureReason.FAILURE_REASON_UNSPECIFIED,
        shared: bool = False,
    ):
        """

        Args:
            profile: The resource name of the NotebookEngineProfile that is assigned to this NotebookEngine.
                Format is `workspaces/*/notebookEngineProfiles/*`.
            notebook_image: The resource name of the NotebookEngineImage used to create the NotebookEngine.
                Format is `workspaces/*/notebookEngineImages/*`.
            name: The resource name of the NotebookEngine.
                Format: `workspaces/*/notebookEngines/*`.
            display_name: Human-readable name.
            cpu: The amount of CPU units requested by this NotebookEngine.
            gpu: The amount of GPU units requested by this NotebookEngine.
            memory_bytes: The amount of memory in bytes requested by this NotebookEngine.
                For example "1024", "8G", "16Gi".
            storage_bytes: The amount of storage requested by this NotebookEngine.
                For example "1024", "8G", "16Gi".
            max_idle_duration: Maximum time the NotebookEngine can be idle.
                When exceeded, the NotebookEngine will pause.
            max_running_duration: Maximum time the NotebookEngine can be running.
                When exceeded, the NotebookEngine will pause.
            state: The current state of the NotebookEngine.
            reconciling: Indicates whether changes to the resource are in progress.
            uid: Globally unique identifier of the resource.
            notebook_image_info: NotebookEngineImage data used during the last NotebookEngine startup from the assigned
                notebook_image.
            profile_info: NotebookEngineProfile data used during the last NotebookEngine startup from the assigned
                profile.
            creator: Name of entity that created the NotebookEngine.
            updater: Name of entity that last updated the NotebookEngine.
            creator_display_name: Human-readable name of entity that created the NotebookEngine.
            updater_display_name: Human-readable name of entity that last updated the NotebookEngine.
            create_time: Time when the NotebookEngine was created.
            update_time: Time when the NotebookEngine was last updated.
            resume_time: Time when the NotebookEngine was resumed.
            delete_time: Time when the NotebookEngine was deleted.
            current_idle_duration: Current time the NotebookEngine is idle.
            current_running_duration: Current time the NotebookEngine is running.
            storage_class_name: Name of the storage class used by NotebookEngine.
            failure_reason: Reason why the NotebookEngine is in failed state. If available.
            shared: Indicates whether the NotebookEngine is shared.
        """
        self.profile = profile
        self.notebook_image = notebook_image
        self.name = name
        self.display_name = display_name
        self.cpu = cpu
        self.gpu = gpu
        self.memory_bytes = memory_bytes
        self.storage_bytes = storage_bytes
        self.max_idle_duration = max_idle_duration
        self.max_running_duration = max_running_duration
        self.state = state
        self.reconciling = reconciling
        self.uid = uid
        self.notebook_image_info = notebook_image_info
        self.profile_info = profile_info
        self.creator = creator
        self.updater = updater
        self.creator_display_name = creator_display_name
        self.updater_display_name = updater_display_name
        self.create_time = create_time
        self.update_time = update_time
        self.resume_time = resume_time
        self.delete_time = delete_time
        self.current_idle_duration = current_idle_duration
        self.current_running_duration = current_running_duration
        self.storage_class_name = storage_class_name
        self.failure_reason = failure_reason
        self.shared = shared

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def notebook_engine_to_api_object(notebook_engine: NotebookEngine) -> V1NotebookEngine:
    return V1NotebookEngine(
        profile=notebook_engine.profile,
        notebook_image=notebook_engine.notebook_image,
        display_name=notebook_engine.display_name,
        cpu=notebook_engine.cpu,
        gpu=notebook_engine.gpu,
        memory_bytes=optional_quantity_to_number_str(quantity=notebook_engine.memory_bytes),
        storage_bytes=optional_quantity_to_number_str(quantity=notebook_engine.storage_bytes),
        max_idle_duration=optional_duration_to_seconds(duration=notebook_engine.max_idle_duration),
        max_running_duration=optional_duration_to_seconds(duration=notebook_engine.max_running_duration),
        shared=notebook_engine.shared,
    )


def notebook_engine_from_api_object(api_object: V1NotebookEngine) -> NotebookEngine:
    return NotebookEngine(
        profile=api_object.profile,
        notebook_image=api_object.notebook_image,
        name=api_object.name,
        display_name=api_object.display_name,
        cpu=api_object.cpu,
        gpu=api_object.gpu,
        memory_bytes=number_str_to_quantity(number_str=api_object.memory_bytes),
        storage_bytes=number_str_to_quantity(number_str=api_object.storage_bytes),
        max_idle_duration=optional_seconds_to_duration(seconds=api_object.max_idle_duration),
        max_running_duration=optional_seconds_to_duration(seconds=api_object.max_running_duration),
        state=notebook_engine_state_from_api_object(api_object=api_object.state),
        reconciling=api_object.reconciling,
        uid=api_object.uid,
        notebook_image_info=notebook_engine_image_info_from_api_object(api_object=api_object.notebook_image_info),
        profile_info=notebook_engine_profile_info_from_api_object(api_object=api_object.profile_info),
        creator=api_object.creator,
        updater=api_object.updater,
        creator_display_name=api_object.creator_display_name,
        updater_display_name=api_object.updater_display_name,
        create_time=api_object.create_time,
        update_time=api_object.update_time,
        resume_time=api_object.resume_time,
        delete_time=api_object.delete_time,
        current_idle_duration=optional_seconds_to_duration(seconds=api_object.current_idle_duration),
        current_running_duration=optional_seconds_to_duration(seconds=api_object.current_running_duration),
        storage_class_name=api_object.storage_class_name,
        failure_reason=notebook_engine_failure_reason_from_api_object(api_object=api_object.failure_reason),
        shared=api_object.shared,
    )


def notebook_engine_to_resource(notebook_engine: NotebookEngine) -> NotebookEngineResource:
    return NotebookEngineResource(
        profile=notebook_engine.profile,
        notebook_image=notebook_engine.notebook_image,
        display_name=notebook_engine.display_name,
        cpu=notebook_engine.cpu,
        gpu=notebook_engine.gpu,
        memory_bytes=optional_quantity_to_number_str(quantity=notebook_engine.memory_bytes),
        storage_bytes=optional_quantity_to_number_str(quantity=notebook_engine.storage_bytes),
        max_idle_duration=optional_duration_to_seconds(duration=notebook_engine.max_idle_duration),
        max_running_duration=optional_duration_to_seconds(duration=notebook_engine.max_running_duration),
        shared=notebook_engine.shared,
    )
