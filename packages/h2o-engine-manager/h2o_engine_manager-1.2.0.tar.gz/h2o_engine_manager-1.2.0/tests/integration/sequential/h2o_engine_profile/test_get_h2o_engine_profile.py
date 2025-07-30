import http
import re

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
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_get_h2o_engine_profile(
    h2o_engine_profile_client_super_admin,
    h2o_engine_profile_client,
    delete_all_h2o_engine_profiles_before_after,
):
    h2o_engine_profile_client_super_admin.create_h2o_engine_profile(
        parent=GLOBAL_WORKSPACE,
        h2o_engine_profile=(H2OEngineProfile(
            node_count_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["admin"]
        )),
        h2o_engine_profile_id="p1",
    )

    profile_get = h2o_engine_profile_client_super_admin.get_h2o_engine_profile(
        name="workspaces/global/h2oEngineProfiles/p1"
    )

    # user cannot GET profile in the global WS
    with pytest.raises(CustomApiException) as exc:
        h2o_engine_profile_client.get_h2o_engine_profile(name="workspaces/global/h2oEngineProfiles/p1")
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


    # Check that Get method returns correct data.
    assert profile_get.node_count_constraint == ProfileConstraintNumeric(minimum="1", default="1")
    assert profile_get.cpu_constraint == ProfileConstraintNumeric(minimum="1", default="1")
    assert profile_get.gpu_constraint == ProfileConstraintNumeric(
        minimum="0", default="0", maximum="10", cumulative_maximum="100"
    )
    assert profile_get.memory_bytes_constraint == ProfileConstraintNumeric(minimum="100", default="100")
    assert profile_get.max_idle_duration_constraint == ProfileConstraintDuration(minimum="100s", default="200s")
    assert profile_get.max_running_duration_constraint == ProfileConstraintDuration(
        minimum="100s", default="200s", maximum="400s"
    )
    assert profile_get.name == "workspaces/global/h2oEngineProfiles/p1"
    assert profile_get.display_name == ""
    assert profile_get.priority == 0
    assert profile_get.enabled is True
    assert profile_get.assigned_oidc_roles_enabled is True
    assert profile_get.assigned_oidc_roles == ["admin"]
    assert profile_get.max_running_engines is None
    assert profile_get.yaml_pod_template_spec == ""
    assert profile_get.yaml_gpu_tolerations == ""
    assert profile_get.create_time is not None
    assert profile_get.update_time is None
    assert re.match(r"^users/.+$", profile_get.creator)
    assert profile_get.updater == ""
    assert profile_get.creator_display_name == "test-super-admin"
    assert profile_get.updater_display_name == ""
    assert profile_get.gpu_resource_name == "nvidia.com/gpu"
