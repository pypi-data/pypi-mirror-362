import os
import time

import pytest
from kubernetes import client
from kubernetes import config
from kubernetes.client.models.v1_pod import V1Pod

from h2o_engine_manager.clients.dai_engine.dai_engine import DAIEngine
from h2o_engine_manager.clients.dai_engine.dai_engine_client import DAIEngineClient
from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from tests.integration.conftest import DAI_SETUP_WORKSPACE


@pytest.mark.timeout(180)
def test_pod_template_spec_applied(
    dai_client,
    dai_engine_profile_15,
    dai_engine_version_v1_11_10,
):
    """
    Whitebox testing! (Pod spec is not accessible via API)
    """
    config.load_config()

    workspace_id = DAI_SETUP_WORKSPACE
    engine_id = "engine1"
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
            profile=dai_engine_profile_15.name,
            dai_engine_version=dai_engine_version_v1_11_10.name,
        )

        # Wait until engine is running - we need to wait until the pod is created.
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_RUNNING.name

        pod = get_dai_pod(
            namespace=namespace, workspace_id=workspace_id, engine_id=engine_id
        )

        # Then custom setup was applied on top of default spec.

        assert pod.metadata.annotations["custom-key"] == "custom-value"

        assert len(pod.spec.containers) == 3

        dai_container = next(
            (c for c in pod.spec.containers if c.name == "driverless-ai"), None
        )
        custom_env_var = next(
            (e for e in dai_container.env if e.name == "CUSTOM_VAR"), None
        )
        assert custom_env_var.value == "CUSTOM_VAL"
        existing_env_var = next(
            (
                e
                for e in dai_container.env
                if e.name == "DRIVERLESS_AI_OVERRIDE_VIRTUAL_CORES"
            ),
            None,
        )
        assert existing_env_var.value == "20"

        custom_container = next(
            (c for c in pod.spec.containers if c.name == "custom-container"), None
        )
        assert custom_container.image == "353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai"
        assert custom_container.ports[0].container_port == 21212

        # We expect in total 3 tolerations.
        # Our configured tolerations:
        # - podTemplateSpec toleration ("dedicated")
        # and Kubernetes automatically adds 2 tolerations:
        # - node.kubernetes.io/not-ready
        # - node.kubernetes.io/unreachable
        #
        # gpuToleration is ignored because the engine has gpu == 0
        assert len(pod.spec.tolerations) == 3

        # Test that all tolerations are present.
        dedicated_idx = -1
        not_ready_idx = -1
        unreachable_idx = -1
        for idx, t in enumerate(pod.spec.tolerations):
            # match-case pattern is supported in python 3.10+ -_-
            if t.key == "dedicated":
                dedicated_idx = idx
            elif t.key == "gpu":
                pass
            elif t.key == "node.kubernetes.io/not-ready":
                not_ready_idx = idx
            elif t.key == "node.kubernetes.io/unreachable":
                unreachable_idx = idx

        assert dedicated_idx != -1
        assert not_ready_idx != -1
        assert unreachable_idx != -1

        assert pod.spec.tolerations[dedicated_idx].operator == "Equal"
        assert pod.spec.tolerations[dedicated_idx].value == "steam"
        assert pod.spec.tolerations[dedicated_idx].effect == "NoSchedule"

        override_env_var1 = next(
            (e for e in dai_container.env if e.name == "DRIVERLESS_AI_DISK_LIMIT_GB"),
            None,
        )
        assert override_env_var1.value == "10"

        override_env_var2 = next(
            (e for e in dai_container.env if e.name == "DRIVERLESS_AI_MY_NEW_CONFIG"),
            None,
        )
        assert override_env_var2.value == "my-new-value"
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(180)
def test_pod_template_spec_gpu_toleration_applied(
    dai_client,
    dai_engine_profile_16,
    dai_engine_version_v1_11_11,
):
    """
    Whitebox testing! (Pod spec is not accessible via API)
    """
    config.load_config()

    workspace_id = DAI_SETUP_WORKSPACE
    engine_id = "engine2"
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
            profile=dai_engine_profile_16.name,
            dai_engine_version=dai_engine_version_v1_11_11.name,
        )

        # We cannot wait until the DAIEngine is in RUNNING state:
        # - there may be no resources in the cluster for allocating pod's GPU
        # - the gpuToleration may never be fulfilled so no node can be used (we're setting nonsense toleration value)
        # For our testing we only need to get the created pod (regardless its status) -> wait until the pod is created.
        pod = wait_until_get_dai_pod(
            namespace=namespace, workspace_id=workspace_id, engine_id=engine_id
        )

        # We expect in total 4 tolerations.
        # Custom tolerations:
        # - gpu toleration ("gpu") - added because engine has gpu > 0
        # and Kubernetes automatically adds 2 tolerations:
        # - node.kubernetes.io/not-ready
        # - node.kubernetes.io/unreachable
        # podTemplateSpec toleration ("dedicated") is ignored, it's overridden by gpu toleration
        assert len(pod.spec.tolerations) == 3

        # Test that all tolerations are present.
        gpu_idx = -1
        not_ready_idx = -1
        unreachable_idx = -1
        for idx, t in enumerate(pod.spec.tolerations):
            # match-case pattern is supported in python 3.10+ -_-
            if t.key == "gpu":
                gpu_idx = idx
            elif t.key == "node.kubernetes.io/not-ready":
                not_ready_idx = idx
            elif t.key == "node.kubernetes.io/unreachable":
                unreachable_idx = idx

        assert gpu_idx != -1
        assert not_ready_idx != -1
        assert unreachable_idx != -1

        assert pod.spec.tolerations[gpu_idx].operator == "Equal"
        assert pod.spec.tolerations[gpu_idx].value == "value1"
        assert pod.spec.tolerations[gpu_idx].effect == "NoSchedule"
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(180)
def test_pod_template_spec_not_applied(
    dai_client,
    dai_engine_profile_17,
    dai_engine_version_v1_11_12,
):
    """
    Whitebox testing! (Pod spec is not accessible via API)
    """
    config.load_config()

    workspace_id = "6763564f-f843-489d-80de-a4dd15340ed9"
    engine_id = "engine1"
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
            profile=dai_engine_profile_17.name,
            dai_engine_version=dai_engine_version_v1_11_12.name,
        )

        # Wait until engine is running - we need to wait until the pod is created.
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_RUNNING.name

        pod = get_dai_pod(
            namespace=namespace, workspace_id=workspace_id, engine_id=engine_id
        )

        assert "custom-key" not in pod.metadata.annotations

        assert len(pod.spec.containers) == 2

        dai_container = next(
            (c for c in pod.spec.containers if c.name == "driverless-ai"), None
        )
        custom_env_var = next(
            (e for e in dai_container.env if e.name == "CUSTOM_VAR"), None
        )
        assert custom_env_var is None
        existing_env_var = next(
            (
                e
                for e in dai_container.env
                if e.name == "DRIVERLESS_AI_OVERRIDE_VIRTUAL_CORES"
            ),
            None,
        )
        assert existing_env_var.value == "1"

        custom_container = next(
            (c for c in pod.spec.containers if c.name == "custom-container"), None
        )
        assert custom_container is None

        override_env_var1 = next(
            (e for e in dai_container.env if e.name == "DRIVERLESS_AI_DISK_LIMIT_GB"),
            None,
        )
        assert override_env_var1.value == "0"

        override_env_var2 = next(
            (e for e in dai_container.env if e.name == "DRIVERLESS_AI_MY_NEW_CONFIG"),
            None,
        )
        assert override_env_var2 is None

        # We expect in total 3 tolerations. One is set by us, Kubernetes automatically adds 2 tolerations:
        # - dedicated (steam)
        # - node.kubernetes.io/not-ready
        # - node.kubernetes.io/unreachable
        assert len(pod.spec.tolerations) == 3

        # Test that all tolerations are present.
        dedicated_idx = -1
        not_ready_idx = -1
        unreachable_idx = -1
        for idx, t in enumerate(pod.spec.tolerations):
            if t.key == "dedicated":
                dedicated_idx = idx
            elif t.key == "node.kubernetes.io/not-ready":
                not_ready_idx = idx
            elif t.key == "node.kubernetes.io/unreachable":
                unreachable_idx = idx

        assert dedicated_idx != -1
        assert not_ready_idx != -1
        assert unreachable_idx != -1
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}", allow_missing=True,
        )


def create_dai_engine(
    dai_engine_client: DAIEngineClient, workspace_id: str, engine_id: str, gpu: int = 0
) -> DAIEngine:
    # Mocked version is good enough for our test.
    want_version = "mock"

    # Create DAIEngine (which internally creates DriverlessAI k8s object).
    return dai_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        version=want_version,
        cpu=1,
        gpu=gpu,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        max_idle_duration="15m",
        max_running_duration="2d",
        display_name="My engine 1",
    )


def wait_until_get_dai_pod(namespace: str, workspace_id: str, engine_id: str) -> V1Pod:
    while True:
        try:
            return get_dai_pod(
                namespace=namespace, workspace_id=workspace_id, engine_id=engine_id
            )
        except Exception:
            pass
        time.sleep(2)


def get_dai_pod(namespace: str, workspace_id: str, engine_id: str) -> V1Pod:
    # Kubernetes client is already setup in conftest.py, can be used here out-of-the-box.
    # Whitebox testing - we know how to fetch the DriverlessAI k8s object directly from cluster.
    dai = client.CustomObjectsApi().get_namespaced_custom_object(
        group="engine.h2o.ai",
        version="v1",
        namespace=namespace,
        plural="driverlessais",
        name=f"{workspace_id}.{engine_id}",
    )

    return client.CoreV1Api().read_namespaced_pod(
        namespace=namespace, name=f"engine-{dai['spec']['managedUID']}"
    )
