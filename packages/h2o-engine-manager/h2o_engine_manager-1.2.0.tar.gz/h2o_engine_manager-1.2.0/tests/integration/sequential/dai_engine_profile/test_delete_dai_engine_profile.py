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


def test_delete_dai_engine_profiles(
    dai_engine_profile_client_super_admin,
    dai_engine_profile_client_admin,
    dai_engine_profile_client,
    delete_all_dai_engine_profiles_before_after,
):
    created = dai_engine_profile_client_super_admin.create_dai_engine_profile(
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
            assigned_oidc_roles=["admin"],
            priority=1,
        )),
        dai_engine_profile_id="p1",
    )

    # Regular user cannot delete.
    with pytest.raises(CustomApiException) as exc:
        dai_engine_profile_client.delete_dai_engine_profile(name=created.name)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # Non-super-admin cannot delete.
    # Even if the user has matching assigned OIDC roles.
    with pytest.raises(CustomApiException) as exc:
        dai_engine_profile_client_admin.delete_dai_engine_profile(name=created.name)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # Only super-admin can delete.
    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=created.name)

    # Check that profile no longer exists.
    with pytest.raises(CustomApiException) as exc:
        dai_engine_profile_client_super_admin.get_dai_engine_profile(name=created.name)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
