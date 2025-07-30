from h2o_engine_manager.clients.constraint.profile_constraint_duration import (
    ProfileConstraintDuration,
)
from h2o_engine_manager.clients.constraint.profile_constraint_numeric import (
    ProfileConstraintNumeric,
)
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile import (
    H2OEngineProfile,
)
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_list_assigned_h2o_engine_profiles(
        h2o_engine_profile_client_super_admin,
        h2o_engine_profile_client_admin,
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
            assigned_oidc_roles=["super_admin"],
            priority=3,
        )),
        h2o_engine_profile_id="p1",
    )

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
            assigned_oidc_roles=["super_admin", "admin"],
            priority=2,
        )),
        h2o_engine_profile_id="p2",
    )

    h2o_engine_profile_client_super_admin.create_h2o_engine_profile(
        parent=GLOBAL_WORKSPACE,
        h2o_engine_profile=(H2OEngineProfile(
            node_count_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            assigned_oidc_roles_enabled=False,
            priority=1,
        )),
        h2o_engine_profile_id="p3",
    )

    # super-admin role is assigned to all profiles with assigned_oidc_roles_enabled
    profiles = h2o_engine_profile_client_super_admin.list_all_assigned_h2o_engine_profiles(parent=GLOBAL_WORKSPACE)
    assert profiles[0].name == "workspaces/global/h2oEngineProfiles/p3"
    assert profiles[1].name == "workspaces/global/h2oEngineProfiles/p2"
    assert profiles[2].name == "workspaces/global/h2oEngineProfiles/p1"

    # admin role can list only p1 (has assigned its role) and p3 (has disabled roles).
    profiles = h2o_engine_profile_client_admin.list_all_assigned_h2o_engine_profiles(parent=GLOBAL_WORKSPACE)
    print(profiles)
    assert len(profiles) == 2
    assert profiles[0].name == "workspaces/global/h2oEngineProfiles/p3"
    assert profiles[1].name == "workspaces/global/h2oEngineProfiles/p2"

    # user has no role so he can list only p3 (has disabled roles).
    profiles = h2o_engine_profile_client.list_all_assigned_h2o_engine_profiles(parent=GLOBAL_WORKSPACE)
    print(profiles)
    assert len(profiles) == 1
    assert profiles[0].name == "workspaces/global/h2oEngineProfiles/p3"

    # test pagination
    page = h2o_engine_profile_client_super_admin.list_assigned_h2o_engine_profiles(parent=GLOBAL_WORKSPACE, page_size=1)
    assert len(page.h2o_engine_profiles) == 1
    assert page.h2o_engine_profiles[0].name == "workspaces/global/h2oEngineProfiles/p3"
    assert page.next_page_token != ""

    page = h2o_engine_profile_client_super_admin.list_assigned_h2o_engine_profiles(
        parent=GLOBAL_WORKSPACE,
        page_size=1,
        page_token=page.next_page_token
    )
    assert len(page.h2o_engine_profiles) == 1
    assert page.h2o_engine_profiles[0].name == "workspaces/global/h2oEngineProfiles/p2"
    assert page.next_page_token != ""

    page = h2o_engine_profile_client_super_admin.list_assigned_h2o_engine_profiles(
        parent=GLOBAL_WORKSPACE,
        page_size=1,
        page_token=page.next_page_token
    )
    assert len(page.h2o_engine_profiles) == 1
    assert page.h2o_engine_profiles[0].name == "workspaces/global/h2oEngineProfiles/p1"
    assert page.next_page_token == ""
