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
from h2o_engine_manager.clients.notebook_engine_profile.profile import (
    NotebookEngineProfile,
)
from tests.integration.conftest import GLOBAL_WORKSPACE

pytestmark = pytest.mark.skip("requires role-based authorization")

def test_list_notebook_engine_profiles(
    notebook_engine_profile_client_super_admin,
    notebook_engine_profile_client,
    delete_all_notebook_engine_profiles_before_after,
):
    notebook_engine_profile_client_super_admin.create_notebook_engine_profile(
        parent=GLOBAL_WORKSPACE,
        notebook_engine_profile=(NotebookEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["admin"],
            priority=3,
        )),
        notebook_engine_profile_id="p1",
    )

    notebook_engine_profile_client_super_admin.create_notebook_engine_profile(
        parent=GLOBAL_WORKSPACE,
        notebook_engine_profile=(NotebookEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["super-admin"],
            priority=2,
        )),
        notebook_engine_profile_id="p2",
    )

    notebook_engine_profile_client_super_admin.create_notebook_engine_profile(
        parent=GLOBAL_WORKSPACE,
        notebook_engine_profile=(NotebookEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            assigned_oidc_roles_enabled=False,
            priority=1,
        )),
        notebook_engine_profile_id="p3",
    )

    # super-admin can list all. Default order by priority.
    profiles: list[NotebookEngineProfile] = notebook_engine_profile_client_super_admin.list_all_notebook_engine_profiles(parent=GLOBAL_WORKSPACE)
    assert len(profiles) == 3
    assert profiles[0].name == "workspaces/global/notebookEngineProfiles/p3"
    assert profiles[1].name == "workspaces/global/notebookEngineProfiles/p2"
    assert profiles[2].name == "workspaces/global/notebookEngineProfiles/p1"

    # user cannot list in global ws
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_profile_client.list_all_notebook_engine_profiles(parent=GLOBAL_WORKSPACE)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # test pagination
    page = notebook_engine_profile_client_super_admin.list_notebook_engine_profiles(parent=GLOBAL_WORKSPACE, page_size=1)
    assert len(page.notebook_engine_profiles) == 1
    assert page.notebook_engine_profiles[0].name == "workspaces/global/notebookEngineProfiles/p3"
    assert page.next_page_token != ""

    page = notebook_engine_profile_client_super_admin.list_notebook_engine_profiles(
        parent=GLOBAL_WORKSPACE,
        page_size=1,
        page_token=page.next_page_token
    )
    assert len(page.notebook_engine_profiles) == 1
    assert page.notebook_engine_profiles[0].name == "workspaces/global/notebookEngineProfiles/p2"
    assert page.next_page_token != ""

    page = notebook_engine_profile_client_super_admin.list_notebook_engine_profiles(
        parent=GLOBAL_WORKSPACE,
        page_size=1,
        page_token=page.next_page_token
    )
    assert len(page.notebook_engine_profiles) == 1
    assert page.notebook_engine_profiles[0].name == "workspaces/global/notebookEngineProfiles/p1"
    assert page.next_page_token == ""
