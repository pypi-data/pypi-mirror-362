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
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile import (
    H2OEngineProfile,
)
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile_config import (
    H2OEngineProfileConfig,
)
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_apply_h2o_engine_profiles_super_admin(
    h2o_engine_profile_client_super_admin,
    delete_all_h2o_engine_profiles_before_after,
):
    # Let already exist some profiles.
    h2o_engine_profile_client_super_admin.create_h2o_engine_profile(
        parent=GLOBAL_WORKSPACE,
        h2o_engine_profile=H2OEngineProfile(
            node_count_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            cpu_constraint=ProfileConstraintNumeric(minimum="2", default="2"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            display_name="Profile 1"
        ),
        h2o_engine_profile_id="p1",
    )
    h2o_engine_profile_client_super_admin.create_h2o_engine_profile(
        parent=GLOBAL_WORKSPACE,
        h2o_engine_profile=H2OEngineProfile(
            node_count_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
        ),
        h2o_engine_profile_id="p4",
    )
    profiles = h2o_engine_profile_client_super_admin.list_all_h2o_engine_profiles(parent=GLOBAL_WORKSPACE)
    assert len(profiles) == 2
    assert profiles[0].name == "workspaces/global/h2oEngineProfiles/p1"
    assert profiles[0].display_name == "Profile 1"
    assert profiles[1].name == "workspaces/global/h2oEngineProfiles/p4"

    configs: List[H2OEngineProfileConfig] = [
        H2OEngineProfileConfig(
            h2o_engine_profile_id="p1",
            node_count_constraint=ProfileConstraintNumeric(minimum="2", default="2"),
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            display_name="Applied Profile 1",
        ),
        H2OEngineProfileConfig(
            h2o_engine_profile_id="p2",
            node_count_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            display_name="Applied Profile 2",
        ),
        H2OEngineProfileConfig(
            h2o_engine_profile_id="p3",
            node_count_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            display_name="Applied Profile 3",
        )
    ]

    # When applying H2OEngineProfile configs.
    applied_profiles = h2o_engine_profile_client_super_admin.apply_h2o_engine_profile_configs(configs=configs)

    # Then only applied profiles exist with specified params.
    assert len(applied_profiles) == 3
    assert applied_profiles[0].name == "workspaces/global/h2oEngineProfiles/p1"
    assert applied_profiles[1].name == "workspaces/global/h2oEngineProfiles/p2"
    assert applied_profiles[2].name == "workspaces/global/h2oEngineProfiles/p3"

    assert applied_profiles[0].node_count_constraint == ProfileConstraintNumeric(minimum="2", default="2")
    assert applied_profiles[0].cpu_constraint == ProfileConstraintNumeric(minimum="1", default="1")
    assert applied_profiles[0].gpu_constraint == ProfileConstraintNumeric(
        minimum="0", default="0", maximum="10", cumulative_maximum="100"
    )
    assert applied_profiles[0].memory_bytes_constraint == ProfileConstraintNumeric(minimum="100", default="100")
    assert applied_profiles[0].max_idle_duration_constraint == ProfileConstraintDuration(minimum="100s", default="200s")
    assert applied_profiles[0].max_running_duration_constraint == ProfileConstraintDuration(
        minimum="100s", default="200s", maximum="400s"
    )
    assert applied_profiles[0].name == "workspaces/global/h2oEngineProfiles/p1"
    assert applied_profiles[0].display_name == "Applied Profile 1"
    assert applied_profiles[0].priority == 0
    assert applied_profiles[0].enabled is True
    assert applied_profiles[0].assigned_oidc_roles_enabled is True
    assert applied_profiles[0].assigned_oidc_roles == []
    assert applied_profiles[0].max_running_engines is None
    assert applied_profiles[0].yaml_pod_template_spec == ""
    assert applied_profiles[0].yaml_gpu_tolerations == ""
    assert applied_profiles[0].create_time is not None
    assert applied_profiles[0].update_time is None
    assert re.match(r"^users/.+$", applied_profiles[0].creator)
    assert applied_profiles[0].updater == ""
    assert applied_profiles[0].creator_display_name == "test-super-admin"
    assert applied_profiles[0].updater_display_name == ""
    assert applied_profiles[0].gpu_resource_name == "nvidia.com/gpu"


def test_apply_h2o_engine_profiles_user(
    h2o_engine_profile_client,
    delete_all_h2o_engine_profiles_before_after,
):
    configs: List[H2OEngineProfileConfig] = [
        H2OEngineProfileConfig(
            h2o_engine_profile_id="p1",
            node_count_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            display_name="Applied Profile 1",
        ),
    ]

    # Regular user cannot apply h2oEngineProfileConfigs (cannot create / delete).
    with pytest.raises(CustomApiException) as exc:
        h2o_engine_profile_client.apply_h2o_engine_profile_configs(configs=configs)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN
