import http

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


def test_delete_notebook_engine_profiles(
    notebook_engine_profile_client_super_admin,
    notebook_engine_profile_client_admin,
    notebook_engine_profile_client,
    delete_all_notebook_engine_profiles_before_after,
):
    created = notebook_engine_profile_client_super_admin.create_notebook_engine_profile(
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
            priority=1,
        )),
        notebook_engine_profile_id="p1",
    )

    # Regular user cannot delete.
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_profile_client.delete_notebook_engine_profile(name=created.name)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # Non-super-admin cannot delete.
    # Even if the user has matching assigned OIDC roles.
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_profile_client_admin.delete_notebook_engine_profile(name=created.name)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # Only super-admin can delete.
    notebook_engine_profile_client_super_admin.delete_notebook_engine_profile(name=created.name)

    # Check that profile no longer exists.
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_profile_client_super_admin.get_notebook_engine_profile(name=created.name)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
