import os
import time
from typing import List

import pytest
from kubernetes import client
from kubernetes import config
from kubernetes.client.models.v1_pod import V1Pod

from h2o_engine_manager.clients.h2o_engine.client import H2OEngineClient
from h2o_engine_manager.clients.h2o_engine.h2o_engine import H2OEngine
from tests.integration.conftest import H2O_SETUP_WORKSPACE


@pytest.mark.timeout(180)
def test_pod_template_spec_gpu_toleration_applied(
    h2o_engine_client,
    h2o_engine_profile_p6,
    h2o_engine_version_v4,
):
    """
    Whitebox testing! (Pod spec is not accessible via API)
    Using workspace_id that has a related H2OSetup (h2o-setup.yaml).
    """
    config.load_config()

    workspace_id = H2O_SETUP_WORKSPACE
    engine_id = "pod-template-spec-gpu-toleration-applied"
    namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

    h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        node_count=1,
        cpu=1,
        gpu=1,
        memory_bytes="1Gi",
        max_idle_duration="15m",
        max_running_duration="2d",
        display_name="My engine 1",
        profile=h2o_engine_profile_p6.name,
        h2o_engine_version=h2o_engine_version_v4.name,
    )

    try:
        # We cannot wait until the H2OEngine is in RUNNING state:
        # - there may be no resources in the cluster for allocating pod's GPU
        # - the gpuToleration may never be fulfilled so no node can be used (we're setting nonsense toleration value)
        # For our testing we only need to get the created pods.
        pods = get_h2o_pods(
            namespace=namespace, workspace_id=workspace_id, engine_id=engine_id
        )

        # Test that each pod is created with the expected gpuTolerations.
        for pod in pods:
            # We expect in total 4 tolerations.
            # Custom tolerations:
            # - gpu toleration ("gpu") - added because engine has gpu > 0
            # and Kubernetes automatically adds 3 tolerations:
            # - node.kubernetes.io/not-ready
            # - node.kubernetes.io/unreachable
            # podTemplateSpec toleration ("dedicated") is ignored, it's overridden by gpu toleration
            assert len(pod.spec.tolerations) == 3

            # Test that all tolerations are present.
            gpu_idx = -1
            not_ready_idx = -1
            unreachable_idx = -1
            for idx, t in enumerate(pod.spec.tolerations):
                # match-case pattern is supported only in python 3.10+ -_-
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
            assert pod.spec.tolerations[gpu_idx].value == "foooooooo"
            assert pod.spec.tolerations[gpu_idx].effect == "NoSchedule"
    finally:
        h2o_engine_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
            name_4=f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
        )


def get_h2o_pods(namespace: str, workspace_id: str, engine_id: str) -> List[V1Pod]:
    # Kubernetes client is already setup in conftest.py, can be used here out-of-the-box.
    # Whitebox testing - we know how to fetch the H2O k8s object directly from cluster.
    h2o = client.CustomObjectsApi().get_namespaced_custom_object(
        group="engine.h2o.ai",
        version="v1",
        namespace=namespace,
        plural="h2os",
        name=f"{workspace_id}.{engine_id}",
    )
    node_count = h2o["spec"]["nodeCount"]

    h2o_pods = []

    # Internal knowledge:
    # - there's exactly as many pods as is nodeCount.
    # - each pod has name composed of H2OEngine.UID and node number (index)
    for i in range(node_count):
        pod = wait_until_get_h2o_pod(
            pod_namespace=namespace, pod_name=f"engine-{h2o['spec']['managedUID']}-{i}"
        )
        h2o_pods.append(pod)

    return h2o_pods


def wait_until_get_h2o_pod(pod_namespace: str, pod_name: str) -> V1Pod:
    while True:
        try:
            return client.CoreV1Api().read_namespaced_pod(
                namespace=pod_namespace, name=pod_name
            )
        except Exception:
            pass
        time.sleep(2)
