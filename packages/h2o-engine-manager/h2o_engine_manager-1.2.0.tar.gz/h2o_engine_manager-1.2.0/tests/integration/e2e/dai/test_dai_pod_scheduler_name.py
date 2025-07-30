import os

import pytest
from kubernetes import config

from tests.integration.e2e.dai.test_dai_pod_template_spec import wait_until_get_dai_pod


@pytest.mark.timeout(180)
def test_dai_pod_scheduler(
        dai_client,
        dai_engine_profile_32,
        dai_engine_version_v2_0_1,
):
    """
    Whitebox testing! (Pod spec is not accessible via API)
    """
    config.load_config()

    workspace_id = "18ac0b86-26b9-428c-869a-209b3c8ef7f0"
    engine_id = "engine"
    namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

    try:
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            cpu=1,
            gpu=1,
            memory_bytes="1Gi",
            storage_bytes="1Gi",
            max_idle_duration="15m",
            max_running_duration="2d",
            display_name="My engine 1",
            profile=dai_engine_profile_32.name,
            dai_engine_version=dai_engine_version_v2_0_1.name,
        )

        # We cannot wait until the DAIEngine is in RUNNING state:
        # - custom scheduler not available
        # - gpu node not available
        # For our testing we only need to get the created pod (regardless its status) -> wait until the pod is created.
        pod = wait_until_get_dai_pod(
            namespace=namespace, workspace_id=workspace_id, engine_id=engine_id
        )

        assert pod.spec.scheduler_name == "gpu-scheduler"
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(180)
def test_dai_pod_scheduler_no_gpu(
        dai_client,
        dai_engine_profile_33,
        dai_engine_version_v2_0_2,
):
    """
    Whitebox testing! (Pod spec is not accessible via API)
    """
    config.load_config()

    workspace_id = "18ac0b86-26b9-428c-869a-209b3c8ef7f0"
    engine_id = "engine-no-gpu"
    namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

    try:
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            cpu=1,
            gpu=0,
            memory_bytes="1Gi",
            storage_bytes="1Gi",
            max_idle_duration="15m",
            max_running_duration="2d",
            display_name="My engine 1",
            profile=dai_engine_profile_33.name,
            dai_engine_version=dai_engine_version_v2_0_2.name,
        )

        # We cannot wait until the DAIEngine is in RUNNING state:
        # - custom scheduler not available
        # - gpu node not available
        # For our testing we only need to get the created pod (regardless its status) -> wait until the pod is created.
        pod = wait_until_get_dai_pod(
            namespace=namespace, workspace_id=workspace_id, engine_id=engine_id
        )

        assert pod.spec.scheduler_name == "default-scheduler"
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )