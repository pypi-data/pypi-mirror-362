from typing import List
from typing import Optional

from h2o_engine_manager.clients.constraint.profile_constraint_duration import (
    ProfileConstraintDuration,
)
from h2o_engine_manager.clients.constraint.profile_constraint_numeric import (
    ProfileConstraintNumeric,
)
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile import (
    H2OEngineProfile,
)


class H2OEngineProfileConfig:
    """
    H2OEngineProfile configuration used as input for apply method.
    """

    def __init__(
        self,
        h2o_engine_profile_id: str,
        node_count_constraint: ProfileConstraintNumeric,
        cpu_constraint: ProfileConstraintNumeric,
        gpu_constraint: ProfileConstraintNumeric,
        memory_bytes_constraint: ProfileConstraintNumeric,
        max_idle_duration_constraint: ProfileConstraintDuration,
        max_running_duration_constraint: ProfileConstraintDuration,
        display_name: str = "",
        priority: int = 0,
        enabled: bool = True,
        assigned_oidc_roles_enabled: bool = True,
        assigned_oidc_roles: Optional[List[str]] = None,
        max_running_engines: Optional[int] = None,
        yaml_pod_template_spec: str = "",
        yaml_gpu_tolerations: str = "",
        gpu_resource_name: str = "",
    ):
        self.h2o_engine_profile_id = h2o_engine_profile_id
        self.node_count_constraint = node_count_constraint
        self.cpu_constraint = cpu_constraint
        self.gpu_constraint = gpu_constraint
        self.memory_bytes_constraint = memory_bytes_constraint
        self.max_idle_duration_constraint = max_idle_duration_constraint
        self.max_running_duration_constraint = max_running_duration_constraint
        self.display_name = display_name
        self.priority = priority
        self.enabled = enabled
        self.assigned_oidc_roles_enabled = assigned_oidc_roles_enabled
        self.assigned_oidc_roles = assigned_oidc_roles
        self.max_running_engines = max_running_engines
        self.yaml_pod_template_spec = yaml_pod_template_spec
        self.yaml_gpu_tolerations = yaml_gpu_tolerations
        self.gpu_resource_name = gpu_resource_name

    def to_h2o_engine_profile(self):
        return H2OEngineProfile(
            node_count_constraint=self.node_count_constraint,
            cpu_constraint=self.cpu_constraint,
            gpu_constraint=self.gpu_constraint,
            memory_bytes_constraint=self.memory_bytes_constraint,
            max_idle_duration_constraint=self.max_idle_duration_constraint,
            max_running_duration_constraint=self.max_running_duration_constraint,
            display_name=self.display_name,
            priority=self.priority,
            enabled=self.enabled,
            assigned_oidc_roles_enabled=self.assigned_oidc_roles_enabled,
            assigned_oidc_roles=self.assigned_oidc_roles,
            max_running_engines=self.max_running_engines,
            yaml_pod_template_spec=self.yaml_pod_template_spec,
            yaml_gpu_tolerations=self.yaml_gpu_tolerations,
            gpu_resource_name=self.gpu_resource_name,
        )
