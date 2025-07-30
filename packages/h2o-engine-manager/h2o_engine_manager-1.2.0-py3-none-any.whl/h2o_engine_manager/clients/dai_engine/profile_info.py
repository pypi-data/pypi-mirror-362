from datetime import datetime
from typing import Dict
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
from h2o_engine_manager.clients.dai_engine_profile import config_editability
from h2o_engine_manager.clients.dai_engine_profile.config_editability import (
    ConfigEditability,
)
from h2o_engine_manager.gen.model.v1_dai_engine_profile_info import (
    V1DAIEngineProfileInfo,
)


class DAIEngineProfileInfo:
    """
    The original DAIEngineProfile data used by DAIEngine when using the DAIEngineProfile.
    For more info about each field see the original DAIEngineProfile resource.
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
        max_non_interaction_duration: Optional[str] = None,
        max_unused_duration: Optional[str] = None,
        configuration_override: Optional[Dict[str, str]] = None,
        base_configuration: Optional[Dict[str, str]] = None,
        config_editability: ConfigEditability = ConfigEditability.CONFIG_EDITABILITY_UNSPECIFIED,
        yaml_pod_template_spec: str = "",
        yaml_gpu_tolerations: str = "",
        triton_enabled: bool = False,
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        creator: str = "",
        updater: str = "",
        creator_display_name: str = "",
        updater_display_name: str = "",
        gpu_resource_name: str = "",
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
        self.max_non_interaction_duration = max_non_interaction_duration
        self.max_unused_duration = max_unused_duration
        self.configuration_override = configuration_override
        self.base_configuration = base_configuration
        self.config_editability = config_editability
        self.yaml_pod_template_spec = yaml_pod_template_spec
        self.yaml_gpu_tolerations = yaml_gpu_tolerations
        self.triton_enabled = triton_enabled
        self.create_time = create_time
        self.update_time = update_time
        self.creator = creator
        self.updater = updater
        self.creator_display_name = creator_display_name
        self.updater_display_name = updater_display_name
        self.gpu_resource_name = gpu_resource_name


def from_dai_engine_profile_info_api_obj(api_obj: V1DAIEngineProfileInfo) -> DAIEngineProfileInfo:
    return DAIEngineProfileInfo(
        name=api_obj.name,
        display_name=api_obj.display_name,
        priority=api_obj.priority,
        enabled=api_obj.enabled,
        assigned_oidc_roles_enabled=api_obj.assigned_oidc_roles_enabled,
        assigned_oidc_roles=api_obj.assigned_oidc_roles,
        max_running_engines=api_obj.max_running_engines,
        cpu_constraint=profile_constraint_numeric.from_api_object(api_object=api_obj.cpu_constraint),
        gpu_constraint=profile_constraint_numeric.from_api_object(api_object=api_obj.gpu_constraint),
        memory_bytes_constraint=profile_constraint_numeric.from_api_object(api_object=api_obj.memory_bytes_constraint),
        storage_bytes_constraint=profile_constraint_numeric.from_api_object(
            api_object=api_obj.storage_bytes_constraint
        ),
        max_idle_duration_constraint=profile_constraint_duration.from_api_object(
            api_object=api_obj.max_idle_duration_constraint,
        ),
        max_running_duration_constraint=profile_constraint_duration.from_api_object(
            api_object=api_obj.max_running_duration_constraint,
        ),
        max_non_interaction_duration=api_obj.max_non_interaction_duration,
        max_unused_duration=api_obj.max_unused_duration,
        configuration_override=api_obj.configuration_override,
        base_configuration=api_obj.base_configuration,
        config_editability=config_editability.from_api_object(api_obj.config_editability),
        yaml_pod_template_spec=api_obj.yaml_pod_template_spec,
        yaml_gpu_tolerations=api_obj.yaml_gpu_tolerations,
        triton_enabled=api_obj.triton_enabled,
        create_time=api_obj.create_time,
        update_time=api_obj.update_time,
        creator=api_obj.creator,
        updater=api_obj.updater,
        creator_display_name=api_obj.creator_display_name,
        updater_display_name=api_obj.updater_display_name,
        gpu_resource_name=api_obj.gpu_resource_name,
    )
