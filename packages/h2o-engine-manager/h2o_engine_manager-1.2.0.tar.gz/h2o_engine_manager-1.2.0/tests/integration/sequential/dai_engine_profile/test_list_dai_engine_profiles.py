import http

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
from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_list_dai_engine_profiles(
    dai_engine_profile_client_super_admin,
    dai_engine_profile_client,
    delete_all_dai_engine_profiles_before_after,
):
    dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent=GLOBAL_WORKSPACE,
        dai_engine_profile=(DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["super_admin"],
            priority=3,
        )),
        dai_engine_profile_id="p1",
    )

    dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent=GLOBAL_WORKSPACE,
        dai_engine_profile=(DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["super_admin", "admin"],
            priority=2,
        )),
        dai_engine_profile_id="p2",
    )

    dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent=GLOBAL_WORKSPACE,
        dai_engine_profile=(DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            assigned_oidc_roles_enabled=False,
            priority=1,
        )),
        dai_engine_profile_id="p3",
    )

    # super-admin role is assigned to all profiles with assigned_oidc_roles_enabled
    profiles = dai_engine_profile_client_super_admin.list_all_dai_engine_profiles(parent=GLOBAL_WORKSPACE)
    assert len(profiles) == 3
    assert profiles[0].name == "workspaces/global/daiEngineProfiles/p3"
    assert profiles[1].name == "workspaces/global/daiEngineProfiles/p2"
    assert profiles[2].name == "workspaces/global/daiEngineProfiles/p1"

    # user role cannot list
    with pytest.raises(CustomApiException) as exc:
        dai_engine_profile_client.list_all_dai_engine_profiles(parent=GLOBAL_WORKSPACE)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # test pagination
    page = dai_engine_profile_client_super_admin.list_dai_engine_profiles(parent=GLOBAL_WORKSPACE, page_size=1)
    assert len(page.dai_engine_profiles) == 1
    assert page.dai_engine_profiles[0].name == "workspaces/global/daiEngineProfiles/p3"
    assert page.next_page_token != ""

    page = dai_engine_profile_client_super_admin.list_dai_engine_profiles(
        parent=GLOBAL_WORKSPACE,
        page_size=1,
        page_token=page.next_page_token
    )
    assert len(page.dai_engine_profiles) == 1
    assert page.dai_engine_profiles[0].name == "workspaces/global/daiEngineProfiles/p2"
    assert page.next_page_token != ""

    page = dai_engine_profile_client_super_admin.list_dai_engine_profiles(
        parent=GLOBAL_WORKSPACE,
        page_size=1,
        page_token=page.next_page_token
    )
    assert len(page.dai_engine_profiles) == 1
    assert page.dai_engine_profiles[0].name == "workspaces/global/daiEngineProfiles/p1"
    assert page.next_page_token == ""
