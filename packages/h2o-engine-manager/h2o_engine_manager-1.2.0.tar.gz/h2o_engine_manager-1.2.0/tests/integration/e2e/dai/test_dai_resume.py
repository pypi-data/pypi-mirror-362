import http
import json
import os

import pytest
from kubernetes import client
from kubernetes import config

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import CustomApiException


@pytest.mark.timeout(180)
def test_dai_resume_update_config(
    dai_client,
    websocket_base_url,
    dai_engine_profile_20,
    dai_engine_version_v1_11_15,
):
    """
    White-box testing using k8s client to check that baseConfig in CRD object is updated
    during resume action (we cannot verify it directly via AIEM API as it is internal logic).
    """
    config.load_config()

    workspace_id = "b6f087a7-eb1a-4f0b-96f4-0c3a9aba8586"
    engine_id = "e1"
    namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

    try:
        engine = dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            cpu=1,
            gpu=0,
            memory_bytes="1Gi",
            storage_bytes="1Gi",
            max_idle_duration="15m",
            max_running_duration="2d",
            display_name="My engine 1",
            config={"key1": "val1"},
            profile=dai_engine_profile_20.name,
            dai_engine_version=dai_engine_version_v1_11_15.name,
        )

        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        # Check that coreConfig (picked parts) and engineConfig of the created engine is set correctly.
        kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        orig_core_config = kube_eng["spec"]["coreConfig"]
        assert orig_core_config["override_virtual_cores"] == "1"
        assert orig_core_config["base_url"] == "/workspaces/b6f087a7-eb1a-4f0b-96f4-0c3a9aba8586/daiEngines/e1/"

        orig_engine_config = kube_eng["spec"]["engineConfig"]
        assert orig_engine_config["key1"] == "val1"

        # Manually update engine's coreConfig (need to access directly via k8s API).
        # Python k8s client supports only strategicMergePatch
        # (it doesn't support jsonPatch: https://github.com/kubernetes-client/python/issues/1216).
        client.CustomObjectsApi().patch_namespaced_custom_object(
            group="engine.h2o.ai",
            version="v1",
            namespace=namespace,
            plural="driverlessais",
            name=f"{workspace_id}.{engine_id}",
            body=(
                json.loads(
                    '{"spec": {"coreConfig":{"override_virtual_cores": "2", "base_url": "/woah/what/a/change/"}}}'
                )
            ),
        )
        # Check that baseConfig has been changed, custom config remains unchanged.
        changed_kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        changed_core_config = changed_kube_eng["spec"]["coreConfig"]
        assert orig_core_config != changed_core_config
        assert changed_core_config["override_virtual_cores"] == "2"
        assert changed_core_config["base_url"] == "/woah/what/a/change/"

        changed_engine_config = kube_eng["spec"]["engineConfig"]
        assert changed_engine_config["key1"] == "val1"

        # Resume engine.
        engine.resume()

        # Check that baseConfig (picked parts) and custom config of the created engine is set back correctly.
        resumed_kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )

        resumed_core_config = resumed_kube_eng["spec"]["coreConfig"]
        assert orig_core_config == resumed_core_config
        assert resumed_core_config["override_virtual_cores"] == "1"
        assert resumed_core_config["base_url"] == "/workspaces/b6f087a7-eb1a-4f0b-96f4-0c3a9aba8586/daiEngines/e1/"

        resumed_engine_config = resumed_kube_eng["spec"]["engineConfig"]
        assert resumed_engine_config["key1"] == "val1"
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


PATCH_DAIVERSION__JSON = """
{
    "spec": {
        "image": "some-nonsense",
        "imagePullPolicy": "IfNotPresent",
        "imagePullSecrets": [
            {"name": "another-pull-secret-name"}
        ],
        "gpuResourceName": "amd.com/gpu",
        "dataDirectoryStorageClass": "foo"
    }
}
"""


def get_kube_dai(workspace_id: str, engine_id: str, namespace: str):
    return client.CustomObjectsApi().get_namespaced_custom_object(
        group="engine.h2o.ai",
        version="v1",
        namespace=namespace,
        plural="driverlessais",
        name=f"{workspace_id}.{engine_id}",
    )
