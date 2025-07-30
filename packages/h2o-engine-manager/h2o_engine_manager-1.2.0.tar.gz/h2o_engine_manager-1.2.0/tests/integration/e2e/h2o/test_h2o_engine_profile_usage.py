import datetime
import http
import os

import pytest
from kubernetes import client
from kubernetes import config

from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.h2o_engine.profile_info import H2OEngineProfileInfo
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile import (
    H2OEngineProfile,
)


@pytest.mark.timeout(180)
def test_h2o_engine_profile_usage(
    clients,
    admin_clients,
    h2o_engine_profile_p1,
    h2o_engine_version_v2,
):
    """
    White-box testing using k8s client for checking fields that are not available via API.
    (need to access directly via k8s)
    """
    config.load_config()

    workspace_id = "687cc72b-8061-4e59-a866-5bcad26aa4b7"
    engine_id = "e1"
    namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

    # Regular user does not have matching OIDC roles -> cannot create engine with this profile.
    with pytest.raises(CustomApiException) as exc:
        clients.h2o_engine_client.create_engine(
            h2o_engine_version=h2o_engine_version_v2.name,
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=h2o_engine_profile_p1.name,
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST

    # Admin client has matching OIDC role -> can create engine with this profile.
    eng = admin_clients.h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=h2o_engine_profile_p1.name,
        h2o_engine_version=h2o_engine_version_v2.name,
    )

    try:
        assert eng.name == f"workspaces/{workspace_id}/h2oEngines/e1"
        assert eng.profile == "workspaces/global/h2oEngineProfiles/p1"
        original_profile = h2o_engine_profile_p1
        assert_profile_equal_profile_info(profile=original_profile, profile_info=eng.profile_info)
        assert eng.profile_info.gpu_resource_name == "amd.com/gpu"
        # Double check that gpu resource name is correctly set in kubeEng.
        kube_eng = get_kube_h2o(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        assert kube_eng["metadata"]["annotations"]["engine.h2o.ai/gpu-resource-name"] == "amd.com/gpu"
    finally:
        admin_clients.h2o_engine_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
            name_4=f"workspaces/{workspace_id}/h2oEngines/{engine_id}", allow_missing=True
        )


def assert_profile_equal_profile_info(profile: H2OEngineProfile, profile_info: H2OEngineProfileInfo):
    assert profile.node_count_constraint == profile_info.node_count_constraint
    assert profile.cpu_constraint == profile_info.cpu_constraint
    assert profile.gpu_constraint == profile_info.gpu_constraint
    assert profile.memory_bytes_constraint == profile_info.memory_bytes_constraint
    assert profile.max_idle_duration_constraint == profile_info.max_idle_duration_constraint
    assert profile.max_running_duration_constraint == profile_info.max_running_duration_constraint
    assert profile.name == profile_info.name
    assert profile.display_name == profile_info.display_name
    assert profile.priority == profile_info.priority
    assert profile.enabled == profile_info.enabled
    assert profile.assigned_oidc_roles_enabled == profile_info.assigned_oidc_roles_enabled
    assert profile.assigned_oidc_roles == profile_info.assigned_oidc_roles
    assert profile.max_running_engines == profile_info.max_running_engines
    assert profile.yaml_pod_template_spec == profile_info.yaml_pod_template_spec
    assert profile.yaml_gpu_tolerations == profile_info.yaml_gpu_tolerations
    assert_equal_datetimes_up_to_seconds(profile.create_time, profile_info.create_time)
    assert_equal_datetimes_up_to_seconds(profile.update_time, profile_info.update_time)
    assert profile.creator == profile_info.creator
    assert profile.updater == profile_info.updater
    assert profile.creator_display_name == profile_info.creator_display_name
    assert profile.updater_display_name == profile_info.updater_display_name
    assert profile.gpu_resource_name == profile_info.gpu_resource_name


def assert_equal_datetimes_up_to_seconds(dt1: datetime.datetime, dt2: datetime.datetime):
    dt1_trimmed = None
    dt2_trimmed = None

    if dt1 is not None:
        dt1_trimmed = dt1.replace(microsecond=0)

    if dt2 is not None:
        dt2_trimmed = dt2.replace(microsecond=0)

    assert dt1_trimmed == dt2_trimmed


def get_kube_h2o(workspace_id: str, engine_id: str, namespace: str):
    return client.CustomObjectsApi().get_namespaced_custom_object(
        group="engine.h2o.ai",
        version="v1",
        namespace=namespace,
        plural="h2os",
        name=f"{workspace_id}.{engine_id}",
    )
