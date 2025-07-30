import pytest

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


@pytest.fixture(scope="function")
def dai_engine_profile_p1(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 1",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["admin", "super_admin"],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
            gpu_resource_name="profile1.com/gpu",
            data_directory_storage_class="storage-class-1"
        ),
        dai_engine_profile_id="p1",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p2(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 2",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
            gpu_resource_name="whatever.com/gpu",
            data_directory_storage_class="storage-class-2",
        ),
        dai_engine_profile_id="p2",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p3(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 3",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["admin", "super_admin"],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
        ),
        dai_engine_profile_id="p3",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p4(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 4",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            assigned_oidc_roles=[],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
        ),
        dai_engine_profile_id="p4",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p5(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 5",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            assigned_oidc_roles=[],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
            gpu_resource_name="nvidia.com/gpu",
            data_directory_storage_class="storage-class-5",
        ),
        dai_engine_profile_id="p5",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p6(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1", maximum="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="1", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 6",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            assigned_oidc_roles=[],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "new-bar"},
            base_configuration={"alice": "new-bob"},
            gpu_resource_name="amd.com/gpu",
            data_directory_storage_class="storage-class-6",
        ),
        dai_engine_profile_id="p6",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p7(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 7",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            max_running_engines=1,
        ),
        dai_engine_profile_id="p7",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="session")
def dai_engine_profile_p8_for_all(dai_engine_profile_client_super_admin):
    # DO NOT MODIFY THIS PROFILE. Can be shared in multiple tests concurrently.
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile p8 for all",
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p8-for-all",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p9(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile p9",
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p9",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p10(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile p10",
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p10",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p11(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="8Gi", default="8Gi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="8Gi", default="8Gi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile p11",
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p11",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_12(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p12",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_13(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p13",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_14(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p14",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_15(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="0s", default="2h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="0s", default="2h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            configuration_override={
                "disk_limit_gb": "10",
                "my_new_config": "my-new-value",
            },
            yaml_pod_template_spec="""
                metadata:
                  annotations:
                    custom-key: custom-value
                spec:
                  containers:
                    - name: driverless-ai
                      env:
                        - name: CUSTOM_VAR
                          value: "CUSTOM_VAL"
                        - name: DRIVERLESS_AI_OVERRIDE_VIRTUAL_CORES
                          value: "20"
                    - name: custom-container
                      image: 353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai
                      ports:
                        - containerPort: 21212
                      # Use different port to avoid collision with driverless-ai container.
                      args: [ "--port", "1111" ]
                  tolerations:
                    - key: "dedicated"
                      operator: "Equal"
                      value: "steam"
                      effect: "NoSchedule"           
            """,
            yaml_gpu_tolerations="""
                - key: "gpu"
                  operator: "Equal"
                  value: "value1"
                  effect: "NoSchedule"
            """,
        ),
        dai_engine_profile_id="p15",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_16(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="0s", default="2h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="0s", default="2h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            configuration_override={
                "disk_limit_gb": "10",
                "my_new_config": "my-new-value",
            },
            yaml_pod_template_spec="""
                metadata:
                  annotations:
                    custom-key: custom-value
                spec:
                  containers:
                    - name: driverless-ai
                      env:
                        - name: CUSTOM_VAR
                          value: "CUSTOM_VAL"
                        - name: DRIVERLESS_AI_OVERRIDE_VIRTUAL_CORES
                          value: "20"
                    - name: custom-container
                      image: 353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai
                      ports:
                        - containerPort: 21212
                      # Use different port to avoid collision with driverless-ai container.
                      args: [ "--port", "1111" ]
                  tolerations:
                    - key: "dedicated"
                      operator: "Equal"
                      value: "steam"
                      effect: "NoSchedule"           
            """,
            yaml_gpu_tolerations="""
                - key: "gpu"
                  operator: "Equal"
                  value: "value1"
                  effect: "NoSchedule"
            """,
        ),
        dai_engine_profile_id="p16",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_17(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(
                minimum="1073741824",
                default="1073741824",
                maximum="1099511627776",
            ),
            storage_bytes_constraint=ProfileConstraintNumeric(
                minimum="1073741824",
                default="1073741824",
                maximum="1099511627776",
            ),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            yaml_pod_template_spec="""
                spec:
                  containers:
                    - name: driverless-ai
                  tolerations:
                    - key: "dedicated"
                      operator: "Equal"
                      value: "steam"
                      effect: "NoSchedule"
            """
        ),
        dai_engine_profile_id="p17",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_18(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(
                minimum="1073741824",
                default="1073741824",
                maximum="1099511627776",
            ),
            storage_bytes_constraint=ProfileConstraintNumeric(
                minimum="1073741824",
                default="1073741824",
                maximum="1099511627776",
            ),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            yaml_pod_template_spec="""
                spec:
                  containers:
                    - name: driverless-ai
                  tolerations:
                    - key: "dedicated"
                      operator: "Equal"
                      value: "steam"
                      effect: "NoSchedule"
            """,
            triton_enabled=True,
        ),
        dai_engine_profile_id="p18",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_19(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(
                minimum="1073741824",
                default="1073741824",
                maximum="1099511627776",
            ),
            storage_bytes_constraint=ProfileConstraintNumeric(
                minimum="1073741824",
                default="1073741824",
                maximum="1099511627776",
            ),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            yaml_pod_template_spec="""
                spec:
                  containers:
                    - name: driverless-ai
                  tolerations:
                    - key: "dedicated"
                      operator: "Equal"
                      value: "steam"
                      effect: "NoSchedule"
            """,
            triton_enabled=False,
        ),
        dai_engine_profile_id="p19",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_20(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p20",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_21(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p21",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_22(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p22",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_23(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p23",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_24(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p24",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_25(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p25",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_26(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="16Gi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="32Gi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p26",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p27(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="0s", default="2h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="0s", default="2h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p27",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p28(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="0s", default="2h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="0s", default="2h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p28",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_29(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="16Gi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="32Gi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p29",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_30(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="16Gi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="32Gi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p30",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_31(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="16Gi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="32Gi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p31",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_32(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="16Gi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="32Gi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p32",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_33(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="16Gi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="1Gi", default="1Gi", maximum="32Gi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        dai_engine_profile_id="p33",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)
