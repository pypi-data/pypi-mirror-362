import http
import re
import time

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


def test_list_h2o_engine_profiles(
    h2o_engine_profile_client_super_admin,
    h2o_engine_profile_client_admin,
    h2o_engine_profile_client,
    delete_all_h2o_engine_profiles_before_after,
):
    created = h2o_engine_profile_client_super_admin.create_h2o_engine_profile(
        parent=GLOBAL_WORKSPACE,
        h2o_engine_profile=(H2OEngineProfile(
            node_count_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["admin"],
            priority=1,
        )),
        h2o_engine_profile_id="p1",
    )

    creator = created.creator
    re.match(r"^users/.+$", creator)
    create_time = created.create_time
    now_before = time.time()

    created.priority = 2
    created.creator = "whatever"
    created.node_count_constraint = ProfileConstraintNumeric(
        minimum="2", default="3", maximum="4", cumulative_maximum="5"
    )
    created.cpu_constraint = ProfileConstraintNumeric(minimum="2", default="3", maximum="4", cumulative_maximum="5")
    created.gpu_resource_name = "amd.com/gpu"

    # Regular user cannot update.
    with pytest.raises(CustomApiException) as exc:
        h2o_engine_profile_client.update_h2o_engine_profile(h2o_engine_profile=created)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # Non-super-admin cannot update.
    # Even if the user has matching assigned OIDC roles.
    with pytest.raises(CustomApiException) as exc:
        h2o_engine_profile_client_admin.update_h2o_engine_profile(h2o_engine_profile=created)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # Only super-admin can update.
    updated = h2o_engine_profile_client_super_admin.update_h2o_engine_profile(h2o_engine_profile=created)

    assert updated.node_count_constraint == ProfileConstraintNumeric(
        minimum="2", default="3", maximum="4", cumulative_maximum="5"
    )
    assert updated.cpu_constraint == ProfileConstraintNumeric(
        minimum="2", default="3", maximum="4", cumulative_maximum="5"
    )
    assert updated.gpu_constraint == ProfileConstraintNumeric(
        minimum="0", default="0", maximum="10", cumulative_maximum="100"
    )
    assert updated.memory_bytes_constraint == ProfileConstraintNumeric(minimum="100", default="100")
    assert updated.max_idle_duration_constraint == ProfileConstraintDuration(minimum="100s", default="200s")
    assert updated.max_running_duration_constraint == ProfileConstraintDuration(
        minimum="100s", default="200s", maximum="400s"
    )
    assert updated.name == "workspaces/global/h2oEngineProfiles/p1"
    assert updated.display_name == ""
    assert updated.priority == 2
    assert updated.enabled is True
    assert updated.assigned_oidc_roles_enabled is True
    assert updated.assigned_oidc_roles == ["admin"]
    assert updated.max_running_engines is None
    assert updated.yaml_pod_template_spec == ""
    assert updated.yaml_gpu_tolerations == ""
    assert updated.create_time == create_time
    assert updated.create_time != updated.update_time
    now_after = time.time()
    assert now_before <= updated.update_time.timestamp() <= now_after
    assert updated.creator == creator
    assert updated.creator == updated.updater
    assert updated.creator_display_name == "test-super-admin"
    assert updated.updater_display_name == "test-super-admin"
    assert updated.gpu_resource_name == "amd.com/gpu"
