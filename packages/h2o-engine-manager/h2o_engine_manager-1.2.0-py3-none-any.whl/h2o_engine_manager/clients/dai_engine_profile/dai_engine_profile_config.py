from typing import Dict
from typing import List
from typing import Optional

from h2o_engine_manager.clients.constraint.profile_constraint_duration import (
    ProfileConstraintDuration,
)
from h2o_engine_manager.clients.constraint.profile_constraint_numeric import (
    ProfileConstraintNumeric,
)
from h2o_engine_manager.clients.dai_engine_profile.config_editability import (
    ConfigEditability,
)
from h2o_engine_manager.clients.dai_engine_profile.dai_engine_profile import (
    DAIEngineProfile,
)


class DAIEngineProfileConfig:
    """
    DAIEngineProfile configuration used as input for apply method.
    """

    def __init__(
        self,
        dai_engine_profile_id: str,
        cpu_constraint: ProfileConstraintNumeric,
        gpu_constraint: ProfileConstraintNumeric,
        memory_bytes_constraint: ProfileConstraintNumeric,
        storage_bytes_constraint: ProfileConstraintNumeric,
        max_idle_duration_constraint: ProfileConstraintDuration,
        max_running_duration_constraint: ProfileConstraintDuration,
        config_editability: ConfigEditability,
        display_name: str = "",
        priority: int = 0,
        enabled: bool = True,
        assigned_oidc_roles_enabled: bool = True,
        assigned_oidc_roles: Optional[List[str]] = None,
        max_running_engines: Optional[int] = None,
        max_non_interaction_duration: Optional[str] = None,
        max_unused_duration: Optional[str] = None,
        configuration_override: Optional[Dict[str, str]] = None,
        base_configuration: Optional[Dict[str, str]] = None,
        yaml_pod_template_spec: str = "",
        yaml_gpu_tolerations: str = "",
        triton_enabled: bool = False,
        gpu_resource_name: str = "",
        data_directory_storage_class: str = "",
    ):
        self.dai_engine_profile_id = dai_engine_profile_id
        self.cpu_constraint = cpu_constraint
        self.gpu_constraint = gpu_constraint
        self.memory_bytes_constraint = memory_bytes_constraint
        self.storage_bytes_constraint = storage_bytes_constraint
        self.max_idle_duration_constraint = max_idle_duration_constraint
        self.max_running_duration_constraint = max_running_duration_constraint
        self.config_editability = config_editability
        self.display_name = display_name
        self.priority = priority
        self.enabled = enabled
        self.assigned_oidc_roles_enabled = assigned_oidc_roles_enabled
        self.assigned_oidc_roles = assigned_oidc_roles
        self.max_running_engines = max_running_engines
        self.max_non_interaction_duration = max_non_interaction_duration
        self.max_unused_duration = max_unused_duration
        self.configuration_override = configuration_override
        self.base_configuration = base_configuration
        self.yaml_pod_template_spec = yaml_pod_template_spec
        self.yaml_gpu_tolerations = yaml_gpu_tolerations
        self.triton_enabled = triton_enabled
        self.gpu_resource_name = gpu_resource_name
        self.data_directory_storage_class = data_directory_storage_class

    def to_dai_engine_profile(self):
        return DAIEngineProfile(
            cpu_constraint=self.cpu_constraint,
            gpu_constraint=self.gpu_constraint,
            memory_bytes_constraint=self.memory_bytes_constraint,
            storage_bytes_constraint=self.storage_bytes_constraint,
            max_idle_duration_constraint=self.max_idle_duration_constraint,
            max_running_duration_constraint=self.max_running_duration_constraint,
            config_editability=self.config_editability,
            display_name=self.display_name,
            priority=self.priority,
            enabled=self.enabled,
            assigned_oidc_roles_enabled=self.assigned_oidc_roles_enabled,
            assigned_oidc_roles=self.assigned_oidc_roles,
            max_running_engines=self.max_running_engines,
            max_non_interaction_duration=self.max_non_interaction_duration,
            max_unused_duration=self.max_unused_duration,
            configuration_override=self.configuration_override,
            base_configuration=self.base_configuration,
            yaml_pod_template_spec=self.yaml_pod_template_spec,
            yaml_gpu_tolerations=self.yaml_gpu_tolerations,
            triton_enabled=self.triton_enabled,
            gpu_resource_name=self.gpu_resource_name,
            data_directory_storage_class=self.data_directory_storage_class,
        )
