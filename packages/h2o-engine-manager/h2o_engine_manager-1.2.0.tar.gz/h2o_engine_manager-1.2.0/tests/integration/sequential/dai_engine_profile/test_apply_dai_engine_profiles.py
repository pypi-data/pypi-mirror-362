import http
import re
from typing import List

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
from h2o_engine_manager.clients.dai_engine_profile.dai_engine_profile_config import (
    DAIEngineProfileConfig,
)
from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_apply_dai_engine_profiles_super_admin(
    dai_engine_profile_client_super_admin,
    delete_all_dai_engine_profiles_before_after,
):
    # Let already exist some profiles.
    dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent=GLOBAL_WORKSPACE,
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="2", default="2"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="Profile 1"
        ),
        dai_engine_profile_id="p1",
    )
    dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent=GLOBAL_WORKSPACE,
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
        ),
        dai_engine_profile_id="p4",
    )
    profiles = dai_engine_profile_client_super_admin.list_all_dai_engine_profiles(parent=GLOBAL_WORKSPACE)
    assert len(profiles) == 2
    assert profiles[0].name == "workspaces/global/daiEngineProfiles/p1"
    assert profiles[0].display_name == "Profile 1"
    assert profiles[1].name == "workspaces/global/daiEngineProfiles/p4"

    configs: List[DAIEngineProfileConfig] = [
        DAIEngineProfileConfig(
            dai_engine_profile_id="p1",
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="Applied Profile 1",
            gpu_resource_name="amd.com/gpu",
            data_directory_storage_class="ddsc",
        ),
        DAIEngineProfileConfig(
            dai_engine_profile_id="p2",
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="Applied Profile 2",
        ),
        DAIEngineProfileConfig(
            dai_engine_profile_id="p3",
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="Applied Profile 3",
        )
    ]

    # When applying DAIEngineProfile configs.
    applied_profiles = dai_engine_profile_client_super_admin.apply_dai_engine_profile_configs(configs=configs)

    # Then only applied profiles exist with specified params.
    assert len(applied_profiles) == 3
    assert applied_profiles[0].name == "workspaces/global/daiEngineProfiles/p1"
    assert applied_profiles[1].name == "workspaces/global/daiEngineProfiles/p2"
    assert applied_profiles[2].name == "workspaces/global/daiEngineProfiles/p3"

    assert applied_profiles[0].cpu_constraint == ProfileConstraintNumeric(minimum="1", default="1")
    assert applied_profiles[0].gpu_constraint == ProfileConstraintNumeric(
        minimum="0", default="0", maximum="10", cumulative_maximum="100"
    )
    assert applied_profiles[0].memory_bytes_constraint == ProfileConstraintNumeric(minimum="100", default="100")
    assert applied_profiles[0].storage_bytes_constraint == ProfileConstraintNumeric(minimum="100", default="100")
    assert applied_profiles[0].max_idle_duration_constraint == ProfileConstraintDuration(minimum="100s", default="200s")
    assert applied_profiles[0].max_running_duration_constraint == ProfileConstraintDuration(
        minimum="100s", default="200s", maximum="400s"
    )
    assert applied_profiles[0].config_editability == ConfigEditability.CONFIG_EDITABILITY_FULL
    assert applied_profiles[0].name == "workspaces/global/daiEngineProfiles/p1"
    assert applied_profiles[0].display_name == "Applied Profile 1"
    assert applied_profiles[0].priority == 0
    assert applied_profiles[0].enabled is True
    assert applied_profiles[0].assigned_oidc_roles_enabled is True
    assert applied_profiles[0].assigned_oidc_roles == []
    assert applied_profiles[0].max_running_engines is None
    assert applied_profiles[0].max_non_interaction_duration is None
    assert applied_profiles[0].max_unused_duration is None
    assert applied_profiles[0].configuration_override == {}
    assert applied_profiles[0].base_configuration == {}
    assert applied_profiles[0].yaml_pod_template_spec == ""
    assert applied_profiles[0].yaml_gpu_tolerations == ""
    assert applied_profiles[0].triton_enabled is False
    assert applied_profiles[0].create_time is not None
    assert applied_profiles[0].update_time is None
    assert re.match(r"^users/.+$", applied_profiles[0].creator)
    assert applied_profiles[0].updater == ""
    assert applied_profiles[0].creator_display_name == "test-super-admin"
    assert applied_profiles[0].updater_display_name == ""
    assert applied_profiles[0].gpu_resource_name == "amd.com/gpu"
    assert applied_profiles[0].data_directory_storage_class == "ddsc"


def test_apply_dai_engine_profiles_user(
    dai_engine_profile_client,
    delete_all_dai_engine_profiles_before_after,
):
    configs: List[DAIEngineProfileConfig] = [
        DAIEngineProfileConfig(
            dai_engine_profile_id="p1",
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="Applied Profile 1",
        ),
    ]

    # Regular user cannot apply daiEngineProfileConfigs (cannot create / delete).
    with pytest.raises(CustomApiException) as exc:
        dai_engine_profile_client.apply_dai_engine_profile_configs(configs=configs)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN
