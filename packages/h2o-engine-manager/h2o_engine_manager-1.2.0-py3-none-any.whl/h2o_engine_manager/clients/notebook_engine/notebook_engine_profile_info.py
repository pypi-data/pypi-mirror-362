from datetime import datetime
from typing import List
from typing import Optional

from h2o_engine_manager.clients.constraint import profile_constraint_duration
from h2o_engine_manager.clients.constraint import profile_constraint_numeric
from h2o_engine_manager.clients.constraint.profile_constraint_duration import (
    ProfileConstraintDuration,
)
from h2o_engine_manager.clients.constraint.profile_constraint_numeric import (
    ProfileConstraintNumeric,
)
from h2o_engine_manager.gen.model.v1_notebook_engine_profile_info import (
    V1NotebookEngineProfileInfo,
)


class NotebookEngineProfileInfo:
    """
    Contains original data from the NotebookEngineProfile used in NotebookEngine.
    """

    def __init__(
        self,
        name: str = "",
        display_name: str = "",
        priority: int = 0,
        enabled: bool = True,
        assigned_oidc_roles_enabled: bool = True,
        assigned_oidc_roles: Optional[List[str]] = None,
        max_running_engines: Optional[int] = None,
        cpu_constraint: Optional[ProfileConstraintNumeric] = None,
        gpu_constraint: Optional[ProfileConstraintNumeric] = None,
        memory_bytes_constraint: Optional[ProfileConstraintNumeric] = None,
        storage_bytes_constraint: Optional[ProfileConstraintNumeric] = None,
        max_idle_duration_constraint: Optional[ProfileConstraintDuration] = None,
        max_running_duration_constraint: Optional[ProfileConstraintDuration] = None,
        yaml_pod_template_spec: str = "",
        yaml_gpu_tolerations: str = "",
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        creator: str = "",
        updater: str = "",
        creator_display_name: str = "",
        updater_display_name: str = "",
        storage_class_name: str = "",
        gpu_resource_name: str = "",
        sync_git_repository_enabled: bool = False,
        git_repository: str = "",
        git_ref: str = "",
        git_directory_name: str = "",
    ):
        self.name = name
        self.display_name = display_name
        self.priority = priority
        self.enabled = enabled
        self.assigned_oidc_roles_enabled = assigned_oidc_roles_enabled
        self.assigned_oidc_roles = assigned_oidc_roles
        self.max_running_engines = max_running_engines
        self.cpu_constraint = cpu_constraint
        self.gpu_constraint = gpu_constraint
        self.memory_bytes_constraint = memory_bytes_constraint
        self.storage_bytes_constraint = storage_bytes_constraint
        self.max_idle_duration_constraint = max_idle_duration_constraint
        self.max_running_duration_constraint = max_running_duration_constraint
        self.yaml_pod_template_spec = yaml_pod_template_spec
        self.yaml_gpu_tolerations = yaml_gpu_tolerations
        self.create_time = create_time
        self.update_time = update_time
        self.creator = creator
        self.updater = updater
        self.creator_display_name = creator_display_name
        self.updater_display_name = updater_display_name
        self.storage_class_name = storage_class_name
        self.gpu_resource_name = gpu_resource_name
        self.sync_git_repository_enabled = sync_git_repository_enabled
        self.git_repository = git_repository
        self.git_ref = git_ref
        self.git_directory_name = git_directory_name


def notebook_engine_profile_info_from_api_object(
    api_object: Optional[V1NotebookEngineProfileInfo]
) -> Optional[NotebookEngineProfileInfo]:
    if api_object is None:
        return None

    return NotebookEngineProfileInfo(
        name=api_object.name,
        display_name=api_object.display_name,
        priority=api_object.priority,
        enabled=api_object.enabled,
        assigned_oidc_roles_enabled=api_object.assigned_oidc_roles_enabled,
        assigned_oidc_roles=api_object.assigned_oidc_roles,
        max_running_engines=api_object.max_running_engines,
        cpu_constraint=profile_constraint_numeric.from_api_object(api_object=api_object.cpu_constraint),
        gpu_constraint=profile_constraint_numeric.from_api_object(api_object=api_object.gpu_constraint),
        memory_bytes_constraint=profile_constraint_numeric.from_api_object(
            api_object=api_object.memory_bytes_constraint
        ),
        storage_bytes_constraint=profile_constraint_numeric.from_api_object(
            api_object=api_object.storage_bytes_constraint
        ),
        max_idle_duration_constraint=profile_constraint_duration.from_api_object(
            api_object=api_object.max_idle_duration_constraint,
        ),
        max_running_duration_constraint=profile_constraint_duration.from_api_object(
            api_object=api_object.max_running_duration_constraint,
        ),
        yaml_pod_template_spec=api_object.yaml_pod_template_spec,
        yaml_gpu_tolerations=api_object.yaml_gpu_tolerations,
        create_time=api_object.create_time,
        update_time=api_object.update_time,
        creator=api_object.creator,
        updater=api_object.updater,
        creator_display_name=api_object.creator_display_name,
        updater_display_name=api_object.updater_display_name,
        storage_class_name=api_object.storage_class_name,
        gpu_resource_name=api_object.gpu_resource_name,
        sync_git_repository_enabled=api_object.sync_git_repository_enabled,
        git_repository=api_object.git_repository,
        git_ref=api_object.git_ref,
        git_directory_name=api_object.git_directory_name,
    )
