import http
import json
import os
import time

import pytest
from kubernetes import client
from kubernetes import config

from h2o_engine_manager.clients.dai_engine.dai_engine import DAIEngine
from h2o_engine_manager.clients.dai_engine.dai_engine_client import DAIEngineClient
from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS
from tests.integration.e2e.dai.test_dai_engine_profile_usage import (
    assert_profile_equal_profile_info,
)


@pytest.mark.timeout(180)
def test_update(
    dai_client,
    dai_engine_profile_22,
    dai_engine_version_v1_11_17,
):
    workspace_id = "669fb616-e5e6-4d88-9fe4-59c4a8de2931"
    engine_id = "e2e-tests"

    try:
        engine = dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=dai_engine_profile_22.name,
            dai_engine_version=dai_engine_version_v1_11_17.name,
        )
        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        # No DAI engine spec has been changed but the update_time should be
        # non-empty.
        engine.update()
        first_update_time = engine.update_time
        assert first_update_time is not None

        # The precision of update_time is only seconds. Need to wait at least one
        # second to check that next Update operation will update update_time.
        time.sleep(1)

        # Update one field (cpu) using wildcard.
        engine.cpu = 5
        engine.update()

        assert engine.cpu == 5
        second_update_time = engine.update_time
        assert second_update_time > first_update_time

        # Update multiple fields (cpu, annotations and display name).
        # Ignore update of fields that are not in update mask (gpu).
        engine.cpu = 1
        engine.gpu = 50
        engine.annotations = {
            "customKey1": "custom value 1",
            "customKey2": "custom value 2",
        }
        engine.display_name = "New display name"

        engine.update(update_mask="cpu,annotations,display_name")

        assert engine.cpu == 1
        assert engine.gpu == 0
        assert engine.annotations == {
            "customKey1": "custom value 1",
            "customKey2": "custom value 2",
        }
        assert engine.display_name == "New display name"

        # Remove display_name and check that custom annotations remained unchanged.
        # (sort of white-box testing - display_name is stored together with
        # annotations in kubeObject Annotations - want to make sure the update
        # does not interfere)
        engine.display_name = ""
        engine.update()

        assert engine.display_name == ""
        assert engine.annotations == {
            "customKey1": "custom value 1",
            "customKey2": "custom value 2",
        }

        # Update durations.
        engine.max_idle_duration = "361s"
        engine.max_running_duration = "360s"
        engine.update()

        assert engine.max_idle_duration == "361s"
        assert engine.max_running_duration == "6m"
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(180)
def test_update_validate_only(
    dai_client,
    dai_engine_profile_23,
    dai_engine_version_v1_11_18,
):
    workspace_id = "669fb616-e5e6-4d88-9fe4-59c4a8de2931"
    engine_id = "update-validate"

    try:
        engine = dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=dai_engine_profile_23.name,
            dai_engine_version=dai_engine_version_v1_11_18.name,
        )

        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        original_cpu = engine.cpu
        assert original_cpu != 4
        engine.cpu = 4

        engine.update(update_mask="cpu", validate_only=True)

        # Response should contain the updated field
        # (as if the update was truly performed).
        assert engine.cpu == 4

        # Double check that engine is still unchanged.
        time.sleep(CACHE_SYNC_SECONDS)
        engine = dai_client.get_engine(
            engine_id=engine.engine_id, workspace_id=engine.workspace_id
        )

        assert engine.cpu == original_cpu
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(180)
def test_update_config(
    dai_client,
    dai_engine_profile_24,
    dai_engine_version_v1_11_19,
):
    workspace_id = "669fb616-e5e6-4d88-9fe4-59c4a8de2931"
    engine_id = "update-config"
    config.load_config()

    try:
        engine = dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=dai_engine_profile_24.name,
            dai_engine_version=dai_engine_version_v1_11_19.name,
            config={"key1": "val1", "key2": "val2"},
        )

        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        assert engine.config == {"key1": "val1", "key2": "val2"}

        engine.config = {
            "key1": "newVal1",
            "key3": "val3",
        }
        engine.update(update_mask="config")

        assert engine.config == {"key1": "newVal1", "key3": "val3"}

        # Extra white-box testing using k8s client to check that coreConfig in CRD object is not
        # affected by this update action (we cannot verify directly via AIEM API as its hidden).
        api_instance = client.CustomObjectsApi()
        kube_eng = api_instance.get_namespaced_custom_object(
            group="engine.h2o.ai",
            version="v1",
            namespace=os.getenv("TEST_K8S_WORKLOADS_NAMESPACE"),
            plural="driverlessais",
            name=f"{engine.workspace_id}.{engine.engine_id}",
        )

        # Check some base config fields.
        kube_core_config = kube_eng["spec"]["coreConfig"]
        assert kube_core_config["authentication_method"] == "oidc"
        assert (
            kube_core_config["base_url"]
            == f"/workspaces/{engine.workspace_id}/daiEngines/{engine.engine_id}/"
        )
        assert kube_core_config["enable_startup_checks"] == "false"
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(180)
def test_update_precondition(
    dai_client,
    dai_engine_profile_25,
    dai_engine_version_v1_11_20,
):
    workspace_id = "669fb616-e5e6-4d88-9fe4-59c4a8de2931"
    engine_id = "test-update"

    try:
        engine = dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=dai_engine_profile_25.name,
            dai_engine_version=dai_engine_version_v1_11_20.name,
        )

        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        engine.resume()
        with pytest.raises(CustomApiException) as exc:
            engine.update()
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(180)
def test_update_dai_engine_with_unchanged_profile(
    dai_client,
    dai_engine_profile_p4,
    dai_engine_version_v1_11_21,
):
    workspace_id = "default"
    engine_id = "update-dai-engine-with-unchanged-profile"

    # Create engine with profile.
    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=dai_engine_profile_p4.name,
        dai_engine_version=dai_engine_version_v1_11_21.name,
    )
    try:
        assert engine.profile == "workspaces/global/daiEngineProfiles/p4"
        assert engine.profile_info is not None
        assert engine.cpu == 1

        engine.pause()
        engine.wait()

        # Try to unset profile.
        engine.profile = ""
        with pytest.raises(CustomApiException) as exc:
            engine.update()
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert "profile cannot be unset" in json.loads(exc.value.body)["message"]

        # Try to update with invalid format.
        engine.profile = "workspaces/global/foo/p1"
        with pytest.raises(CustomApiException) as exc:
            engine.update()
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: DAIEngineProfile name "workspaces/global/foo/p1" is invalid' \
               in json.loads(exc.value.body)["message"]

        # Update some fields using the existing profile (update with unchanged profile).
        engine.profile = dai_engine_profile_p4.name
        engine.cpu = 2
        engine.update()

        assert engine.profile == "workspaces/global/daiEngineProfiles/p4"  # unchanged
        assert engine.profile_info is not None  # unchanged
        assert engine.cpu == 2  # changed
        assert engine.data_directory_storage_class == dai_engine_profile_p4.data_directory_storage_class

    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(180)
def test_update_dai_engine_with_changed_profile(
    dai_client,
    dai_engine_profile_p5,
    dai_engine_profile_p6,
    dai_engine_version_v1_11_22,
):
    workspace_id = "default"
    engine_id = "update-dai-engine-with-changed-profile"

    # Create engine with profile.
    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=dai_engine_profile_p5.name,
        dai_engine_version=dai_engine_version_v1_11_22.name,
    )
    try:
        assert engine.profile == "workspaces/global/daiEngineProfiles/p5"
        assert engine.profile_info is not None
        assert engine.cpu == 1
        assert_profile_equal_profile_info(profile=dai_engine_profile_p5, profile_info=engine.profile_info)
        assert engine.profile_info.gpu_resource_name == "nvidia.com/gpu"
        assert engine.data_directory_storage_class == "storage-class-5"

        engine.pause()
        engine.wait()

        # Update profile and also update CPU (update with changed profile).
        # New CPU value will violate the new profile constraints (maxCPU=1).
        engine.profile = dai_engine_profile_p6.name
        engine.cpu = 2

        with pytest.raises(CustomApiException) as exc:
            engine.update()
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: max constraint violated: cpu (2) must be <= 1' \
               in json.loads(exc.value.body)["message"]

        engine = dai_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
        assert engine.profile == "workspaces/global/daiEngineProfiles/p5"  # unchanged
        assert engine.profile_info is not None  # unchanged
        assert engine.cpu == 1  # unchanged
        assert engine.gpu == 0  # unchanged
        assert_profile_equal_profile_info(profile=dai_engine_profile_p5, profile_info=engine.profile_info)  # unchanged
        assert engine.profile_info.gpu_resource_name == "nvidia.com/gpu"  # unchanged
        assert engine.data_directory_storage_class == "storage-class-5"  # unchanged

        # Update profile and also update GPU (update with changed profile).
        # New values will match all new profile constraints.
        engine.profile = dai_engine_profile_p6.name
        engine.gpu = 2
        engine.update()

        assert engine.profile == "workspaces/global/daiEngineProfiles/p6"  # changed
        assert engine.profile_info is not None  # unchanged
        # profileInfo is unchanged (until engine is resumed with the new profile)
        assert_profile_equal_profile_info(profile=dai_engine_profile_p5, profile_info=engine.profile_info)
        assert engine.cpu == 1  # unchanged
        assert engine.gpu == 2  # changed

        engine.resume()
        # profileInfo is changed after resume
        assert_profile_equal_profile_info(profile=dai_engine_profile_p6, profile_info=engine.profile_info)
        assert engine.profile_info.gpu_resource_name == "amd.com/gpu"  # changed
        # storage class cannot be changed after creation, even if the profile is changed and engine resumed.
        assert engine.data_directory_storage_class == "storage-class-5"  # unchanged
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )
