import pprint
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
from h2o_engine_manager.clients.convert import duration_convertor
from h2o_engine_manager.clients.dai_engine_profile import config_editability
from h2o_engine_manager.clients.dai_engine_profile.config_editability import (
    ConfigEditability,
)
from h2o_engine_manager.gen.model.required_dai_engine_profile_resource import (
    RequiredDAIEngineProfileResource,
)
from h2o_engine_manager.gen.model.v1_dai_engine_profile import V1DAIEngineProfile


class DAIEngineProfile:
    """
    DAIEngineProfile represents a set of values that are used for DAIEngine.
    """

    def __init__(
        self,
        cpu_constraint: ProfileConstraintNumeric,
        gpu_constraint: ProfileConstraintNumeric,
        memory_bytes_constraint: ProfileConstraintNumeric,
        storage_bytes_constraint: ProfileConstraintNumeric,
        max_idle_duration_constraint: ProfileConstraintDuration,
        max_running_duration_constraint: ProfileConstraintDuration,
        config_editability: ConfigEditability,
        name: str = "",
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
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        creator: str = "",
        updater: str = "",
        creator_display_name: str = "",
        updater_display_name: str = "",
        gpu_resource_name: str = "",
        data_directory_storage_class: str = "",
    ):
        """
        DAIEngineProfile represents a set of values that are used for DAIEngine.

        Args:
            cpu_constraint: Constraint for each DAIEngine's cpu that uses this profile.
            gpu_constraint: Constraint for each DAIEngine's gpu that uses this profile.
            memory_bytes_constraint: Constraint for each DAIEngine's memory_bytes that uses this profile.
            storage_bytes_constraint: Constraint for each DAIEngine's storage_bytes that uses this profile.
            max_idle_duration_constraint: Constraint for each DAIEngine's max_idle_duration that uses this profile.
            max_running_duration_constraint: Constraint for each DAIEngine's max_running_duration
                that uses this profile.
            config_editability: Specifies the behavior of DAIEngine.config editability
                when DAIEngine is using this profile.
            name: Resource name. Format "workspaces/*/daiEngineProfiles/*".
            display_name: Human-readable name.
            priority: Priority of the DAIEngineProfile. Lower value means higher priority.
                Priority is NOT a unique value (any two DAIEngineProfiles can have the same priority value).
            enabled: When set to true, the DAIEngineProfile is enabled and can be used in DAIEngine.
                When set to false, the DAIEngineProfile is disabled and cannot be used in any DAIEngine.
            assigned_oidc_roles_enabled: When set to true, the assigned_oidc_roles field is verified
                when a user uses this profile.
            assigned_oidc_roles: List of OIDC roles assigned to this DAIEngineProfile.
                When profile has assigned some OIDC roles and verification of this list is enabled
                (assigned_oidc_roles_enabled=true), then this profile can be used only by users who have assigned
                at least one role from this list.
            max_running_engines: Maximum number of DAIEngines per user that can be running
                when using this DAIEngineProfile.
            max_non_interaction_duration: Max non-interation duration applied on all DAIEngines that use this profile.
            max_unused_duration: Max unused duration applied on all DAIEngines that use this profile.
            configuration_override: configuration_override is applied on top of all other configurations
                when creating the final configuration that is passed to the DAI server.
            base_configuration: base configuration forms the basis of the final configuration
                that is passed to the DAI server.
            yaml_pod_template_spec: YAML representation of custom PodTemplateSpec.
                Definition of PodTemplateSpec: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#podtemplatespec-v1-core
                When specified, then it is applied for each DAIEngine that uses this profile.
                PodTemplateSpec describes what will be applied on top of a regular DriverlessAI pod before it is created.
                This template is merged into DriverlessAI default pod using StrategicMergePatch method (it overrides the
                default pod).
                More info about StrategicMergePatch: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/
            yaml_gpu_tolerations: YAML representation of custom GPU Tolerations.
                Definition of one Toleration: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#toleration-v1-core
                When specified, then it is applied for each DAIEngine that uses this profile.
                GPUTolerations sets DriverlessAI's pod.spec.tolerations in case DAIEngine has GPU > 0.
                This will override any tolerations defined in yaml_pod_template_spec.PodSpec.Tolerations field.
            triton_enabled: True when DAI built-in Triton inference server is enabled, false when it is disabled.
            create_time: Time when the DAIEngineProfile was created.
            update_time: Time when the DAIEngineProfile was last updated.
            creator: Name of entity that created the DAIEngineProfile.
            updater: Name of entity that last updated the DAIEngineProfile.
            creator_display_name: Human-readable name of entity that created the DAIEngineProfile.
            updater_display_name: Human-readable name of entity that last updated the DAIEngineProfile.
            gpu_resource_name: K8s GPU resource name. For example: `nvidia.com/gpu` or `amd.com/gpu`.
                When unset, server will choose a default value.
            data_directory_storage_class: Name of the storage class used by Driverless AI when using this DAIVersion.
                When unset, the default storage class of the k8s cluster will be used.
        """

        if assigned_oidc_roles is None:
            assigned_oidc_roles = []

        if configuration_override is None:
            configuration_override = {}

        if base_configuration is None:
            base_configuration = {}

        self.cpu_constraint = cpu_constraint
        self.gpu_constraint = gpu_constraint
        self.memory_bytes_constraint = memory_bytes_constraint
        self.storage_bytes_constraint = storage_bytes_constraint
        self.max_idle_duration_constraint = max_idle_duration_constraint
        self.max_running_duration_constraint = max_running_duration_constraint
        self.config_editability = config_editability
        self.name = name
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
        self.create_time = create_time
        self.update_time = update_time
        self.creator = creator
        self.updater = updater
        self.creator_display_name = creator_display_name
        self.updater_display_name = updater_display_name
        self.gpu_resource_name = gpu_resource_name
        self.data_directory_storage_class = data_directory_storage_class

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_api_object(self) -> V1DAIEngineProfile:
        max_non_interaction_duration = None
        if self.max_non_interaction_duration is not None:
            max_non_interaction_duration = duration_convertor.duration_to_seconds(self.max_non_interaction_duration)

        max_unused_duration = None
        if self.max_unused_duration is not None:
            max_unused_duration = duration_convertor.duration_to_seconds(self.max_unused_duration)

        return V1DAIEngineProfile(
            display_name=self.display_name,
            priority=self.priority,
            enabled=self.enabled,
            assigned_oidc_roles_enabled=self.assigned_oidc_roles_enabled,
            assigned_oidc_roles=self.assigned_oidc_roles,
            max_running_engines=self.max_running_engines,
            cpu_constraint=self.cpu_constraint.to_api_object(),
            gpu_constraint=self.gpu_constraint.to_api_object(),
            memory_bytes_constraint=self.memory_bytes_constraint.to_api_object(),
            storage_bytes_constraint=self.storage_bytes_constraint.to_api_object(),
            max_idle_duration_constraint=self.max_idle_duration_constraint.to_api_object(),
            max_running_duration_constraint=self.max_running_duration_constraint.to_api_object(),
            max_non_interaction_duration=max_non_interaction_duration,
            max_unused_duration=max_unused_duration,
            configuration_override=self.configuration_override,
            base_configuration=self.base_configuration,
            config_editability=self.config_editability.to_api_object(),
            yaml_pod_template_spec=self.yaml_pod_template_spec,
            yaml_gpu_tolerations=self.yaml_gpu_tolerations,
            triton_enabled=self.triton_enabled,
            gpu_resource_name=self.gpu_resource_name,
            data_directory_storage_class=self.data_directory_storage_class,
        )

    def to_resource(self) -> RequiredDAIEngineProfileResource:
        max_non_interaction_duration = None
        if self.max_non_interaction_duration is not None:
            max_non_interaction_duration = duration_convertor.duration_to_seconds(self.max_non_interaction_duration)

        max_unused_duration = None
        if self.max_unused_duration is not None:
            max_unused_duration = duration_convertor.duration_to_seconds(self.max_unused_duration)

        return RequiredDAIEngineProfileResource(
            display_name=self.display_name,
            priority=self.priority,
            enabled=self.enabled,
            assigned_oidc_roles_enabled=self.assigned_oidc_roles_enabled,
            assigned_oidc_roles=self.assigned_oidc_roles,
            max_running_engines=self.max_running_engines,
            cpu_constraint=self.cpu_constraint.to_api_object(),
            gpu_constraint=self.gpu_constraint.to_api_object(),
            memory_bytes_constraint=self.memory_bytes_constraint.to_api_object(),
            storage_bytes_constraint=self.storage_bytes_constraint.to_api_object(),
            max_idle_duration_constraint=self.max_idle_duration_constraint.to_api_object(),
            max_running_duration_constraint=self.max_running_duration_constraint.to_api_object(),
            max_non_interaction_duration=max_non_interaction_duration,
            max_unused_duration=max_unused_duration,
            configuration_override=self.configuration_override,
            base_configuration=self.base_configuration,
            config_editability=self.config_editability.to_api_object(),
            yaml_pod_template_spec=self.yaml_pod_template_spec,
            yaml_gpu_tolerations=self.yaml_gpu_tolerations,
            triton_enabled=self.triton_enabled,
            gpu_resource_name=self.gpu_resource_name,
            data_directory_storage_class=self.data_directory_storage_class,
        )


def from_api_object(api_object: V1DAIEngineProfile) -> DAIEngineProfile:
    return DAIEngineProfile(
        cpu_constraint=profile_constraint_numeric.from_api_object(api_object.cpu_constraint),
        gpu_constraint=profile_constraint_numeric.from_api_object(api_object.gpu_constraint),
        memory_bytes_constraint=profile_constraint_numeric.from_api_object(api_object.memory_bytes_constraint),
        storage_bytes_constraint=profile_constraint_numeric.from_api_object(api_object.storage_bytes_constraint),
        max_idle_duration_constraint=profile_constraint_duration.from_api_object(
            api_object.max_idle_duration_constraint),
        max_running_duration_constraint=profile_constraint_duration.from_api_object(
            api_object.max_running_duration_constraint),
        config_editability=config_editability.from_api_object(api_object.config_editability),
        name=api_object.name,
        display_name=api_object.display_name,
        priority=api_object.priority,
        enabled=api_object.enabled,
        assigned_oidc_roles_enabled=api_object.assigned_oidc_roles_enabled,
        assigned_oidc_roles=api_object.assigned_oidc_roles,
        max_running_engines=api_object.max_running_engines,
        max_non_interaction_duration=api_object.max_non_interaction_duration,
        max_unused_duration=api_object.max_unused_duration,
        configuration_override=api_object.configuration_override,
        base_configuration=api_object.base_configuration,
        yaml_pod_template_spec=api_object.yaml_pod_template_spec,
        yaml_gpu_tolerations=api_object.yaml_gpu_tolerations,
        triton_enabled=api_object.triton_enabled,
        create_time=api_object.create_time,
        update_time=api_object.update_time,
        creator=api_object.creator,
        updater=api_object.updater,
        creator_display_name=api_object.creator_display_name,
        updater_display_name=api_object.updater_display_name,
        gpu_resource_name=api_object.gpu_resource_name,
        data_directory_storage_class=api_object.data_directory_storage_class
    )
