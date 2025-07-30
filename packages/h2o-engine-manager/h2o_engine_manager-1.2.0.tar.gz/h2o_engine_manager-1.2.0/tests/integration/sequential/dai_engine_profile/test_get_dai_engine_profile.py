import http
import re

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


def test_get_dai_engine_profile(
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
            assigned_oidc_roles=["admin"]
        )),
        dai_engine_profile_id="p1",
    )

    profile_get = dai_engine_profile_client_super_admin.get_dai_engine_profile(
        name="workspaces/global/daiEngineProfiles/p1"
    )

    # User cannot GetDAIEngineProfile (does not have permission).
    with pytest.raises(CustomApiException) as exc:
        dai_engine_profile_client.get_dai_engine_profile(name="workspaces/global/daiEngineProfiles/p1")
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


    # Check that Get method returns correct data.
    assert profile_get.cpu_constraint == ProfileConstraintNumeric(minimum="1", default="1")
    assert profile_get.gpu_constraint == ProfileConstraintNumeric(
        minimum="0", default="0", maximum="10", cumulative_maximum="100"
    )
    assert profile_get.memory_bytes_constraint == ProfileConstraintNumeric(minimum="100", default="100")
    assert profile_get.storage_bytes_constraint == ProfileConstraintNumeric(minimum="100", default="100")
    assert profile_get.max_idle_duration_constraint == ProfileConstraintDuration(minimum="100s", default="200s")
    assert profile_get.max_running_duration_constraint == ProfileConstraintDuration(
        minimum="100s", default="200s", maximum="400s"
    )
    assert profile_get.config_editability == ConfigEditability.CONFIG_EDITABILITY_FULL
    assert profile_get.name == "workspaces/global/daiEngineProfiles/p1"
    assert profile_get.display_name == ""
    assert profile_get.priority == 0
    assert profile_get.enabled is True
    assert profile_get.assigned_oidc_roles_enabled is True
    assert profile_get.assigned_oidc_roles == ["admin"]
    assert profile_get.max_running_engines is None
    assert profile_get.max_non_interaction_duration is None
    assert profile_get.max_unused_duration is None
    assert profile_get.configuration_override == {}
    assert profile_get.base_configuration == {}
    assert profile_get.yaml_pod_template_spec == ""
    assert profile_get.yaml_gpu_tolerations == ""
    assert profile_get.triton_enabled is False
    assert profile_get.create_time is not None
    assert profile_get.update_time is None
    assert re.match(r"^users/.+$", profile_get.creator)
    assert profile_get.updater == ""
    assert profile_get.creator_display_name == "test-super-admin"
    assert profile_get.updater_display_name == ""
    assert profile_get.gpu_resource_name == "nvidia.com/gpu"
    assert profile_get.data_directory_storage_class == ""
