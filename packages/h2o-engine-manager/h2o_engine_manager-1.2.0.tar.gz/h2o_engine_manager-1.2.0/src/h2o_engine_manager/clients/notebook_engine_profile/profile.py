import pprint
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
from h2o_engine_manager.gen.model.required_notebook_engine_profile_resource import (
    RequiredNotebookEngineProfileResource,
)
from h2o_engine_manager.gen.model.v1_notebook_engine_profile import (
    V1NotebookEngineProfile,
)


class NotebookEngineProfile:
    """
    NotebookEngineProfile represents a set of values that are used for NotebookEngine.
    """

    def __init__(
        self,
        cpu_constraint: ProfileConstraintNumeric,
        gpu_constraint: ProfileConstraintNumeric,
        memory_bytes_constraint: ProfileConstraintNumeric,
        storage_bytes_constraint: ProfileConstraintNumeric,
        max_idle_duration_constraint: ProfileConstraintDuration,
        max_running_duration_constraint: ProfileConstraintDuration,
        name: str = "",
        display_name: str = "",
        priority: int = 0,
        enabled: bool = True,
        assigned_oidc_roles_enabled: bool = True,
        assigned_oidc_roles: Optional[List[str]] = None,
        max_running_engines: Optional[int] = None,
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
        """
        NotebookEngineProfile represents a set of values that are used for NotebookEngine.

        Args:
            cpu_constraint: Constraint for each NotebookEngine's cpu that uses this profile.
            gpu_constraint: Constraint for each NotebookEngine's gpu that uses this profile.
            memory_bytes_constraint: Constraint for each NotebookEngine's memory_bytes that uses this profile.
            storage_bytes_constraint: Constraint for each NotebookEngine's storage_bytes that uses this profile.
            max_idle_duration_constraint: Constraint for each NotebookEngine's max_idle_duration that uses this profile.
            max_running_duration_constraint: Constraint for each NotebookEngine's max_running_duration
                that uses this profile.
            name: Resource name. Format "workspaces/*/notebookEngineProfiles/*".
            display_name: Human-readable name.
            priority: Priority of the NotebookEngineProfile. Lower value means higher priority.
                Priority is NOT a unique value (any two NotebookEngineProfiles can have the same priority value).
            enabled: When set to true, the NotebookEngineProfile is enabled and can be used in NotebookEngine.
                When set to false, the NotebookEngineProfile is disabled and cannot be used in any NotebookEngine.
            assigned_oidc_roles_enabled: When set to true, the assigned_oidc_roles field is verified
                when a user uses this profile.
            assigned_oidc_roles: List of OIDC roles assigned to this NotebookEngineProfile.
                When profile has assigned some OIDC roles and verification of this list is enabled
                (assigned_oidc_roles_enabled=true), then this profile can be used only by users who have assigned
                at least one role from this list.
            max_running_engines: Maximum number of NotebookEngines per user that can be running
                when using this NotebookEngineProfile.
            yaml_pod_template_spec: YAML representation of custom PodTemplateSpec.
                Definition of PodTemplateSpec: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#podtemplatespec-v1-core
                When specified, then it is applied for each NotebookEngine that uses this profile.
                PodTemplateSpec describes what will be applied on top of a regular Notebook pod before it is created.
                This template is merged into Notebook default pod using StrategicMergePatch method (it overrides the
                default pod).
                More info about StrategicMergePatch: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/
            yaml_gpu_tolerations: YAML representation of custom GPU Tolerations.
                Definition of one Toleration: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#toleration-v1-core
                When specified, then it is applied for each NotebookEngine that uses this profile.
                GPUTolerations sets Notebook's pod.spec.tolerations in case NotebookEngine has GPU > 0.
                This will override any tolerations defined in yaml_pod_template_spec.PodSpec.Tolerations field.
            create_time: Time when the NotebookEngineProfile was created.
            update_time: Time when the NotebookEngineProfile was last updated.
            creator: Name of entity that created the NotebookEngineProfile.
            updater: Name of entity that last updated the NotebookEngineProfile.
            creator_display_name: Human-readable name of entity that created the NotebookEngineProfile.
            updater_display_name: Human-readable name of entity that last updated the NotebookEngineProfile.
            storage_class_name: Name of the storage class used by NotebookEngine when using this profile.
            gpu_resource_name: K8s GPU resource name. For example: `nvidia.com/gpu` or `amd.com/gpu`.
            sync_git_repository_enabled: Enables syncing of the git repository when NotebookEngine is created.
            git_repository: The git repository to sync.
            git_ref: The git revision (branch, tag, or hash) to check out.
                If not specified, this defaults to "HEAD" (of the upstream repo's default branch).
            git_directory_name: The name of the directory in the user's home folder, where the Git repo is synced into.
                Defaults to "Example".
        """

        if assigned_oidc_roles is None:
            assigned_oidc_roles = []

        self.cpu_constraint = cpu_constraint
        self.gpu_constraint = gpu_constraint
        self.memory_bytes_constraint = memory_bytes_constraint
        self.storage_bytes_constraint = storage_bytes_constraint
        self.max_idle_duration_constraint = max_idle_duration_constraint
        self.max_running_duration_constraint = max_running_duration_constraint
        self.name = name
        self.display_name = display_name
        self.priority = priority
        self.enabled = enabled
        self.assigned_oidc_roles_enabled = assigned_oidc_roles_enabled
        self.assigned_oidc_roles = assigned_oidc_roles
        self.max_running_engines = max_running_engines
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

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_api_object(self) -> V1NotebookEngineProfile:
        return V1NotebookEngineProfile(
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
            yaml_pod_template_spec=self.yaml_pod_template_spec,
            yaml_gpu_tolerations=self.yaml_gpu_tolerations,
            storage_class_name=self.storage_class_name,
            gpu_resource_name=self.gpu_resource_name,
            sync_git_repository_enabled=self.sync_git_repository_enabled,
            git_repository=self.git_repository,
            git_ref=self.git_ref,
            git_directory_name=self.git_directory_name,
        )

    def to_resource(self) -> RequiredNotebookEngineProfileResource:
        return RequiredNotebookEngineProfileResource(
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
            yaml_pod_template_spec=self.yaml_pod_template_spec,
            yaml_gpu_tolerations=self.yaml_gpu_tolerations,
            storage_class_name=self.storage_class_name,
            gpu_resource_name=self.gpu_resource_name,
            sync_git_repository_enabled=self.sync_git_repository_enabled,
            git_repository=self.git_repository,
            git_ref=self.git_ref,
            git_directory_name=self.git_directory_name,
        )


def from_api_object(api_object: V1NotebookEngineProfile) -> NotebookEngineProfile:
    return NotebookEngineProfile(
        cpu_constraint=profile_constraint_numeric.from_api_object(api_object.cpu_constraint),
        gpu_constraint=profile_constraint_numeric.from_api_object(api_object.gpu_constraint),
        memory_bytes_constraint=profile_constraint_numeric.from_api_object(api_object.memory_bytes_constraint),
        storage_bytes_constraint=profile_constraint_numeric.from_api_object(api_object.storage_bytes_constraint),
        max_idle_duration_constraint=profile_constraint_duration.from_api_object(
            api_object.max_idle_duration_constraint),
        max_running_duration_constraint=profile_constraint_duration.from_api_object(
            api_object.max_running_duration_constraint),
        name=api_object.name,
        display_name=api_object.display_name,
        priority=api_object.priority,
        enabled=api_object.enabled,
        assigned_oidc_roles_enabled=api_object.assigned_oidc_roles_enabled,
        assigned_oidc_roles=api_object.assigned_oidc_roles,
        max_running_engines=api_object.max_running_engines,
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
