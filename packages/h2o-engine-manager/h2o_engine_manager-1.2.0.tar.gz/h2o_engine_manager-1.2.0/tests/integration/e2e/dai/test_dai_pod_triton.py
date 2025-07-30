import os

import pytest
from kubernetes import config

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from tests.integration.e2e.dai.test_dai_pod_template_spec import create_dai_engine
from tests.integration.e2e.dai.test_dai_pod_template_spec import get_dai_pod


@pytest.mark.timeout(180)
def test_triton_enabled(
    dai_client,
    dai_engine_profile_18,
    dai_engine_version_v1_11_13,
):
    """
    Whitebox testing! (Pod spec is not accessible via API)
    """
    config.load_config()

    workspace_id = "225fb6ba-ed48-4534-a861-3ea3f51bc67a"
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
            profile=dai_engine_profile_18.name,
            dai_engine_version=dai_engine_version_v1_11_13.name,
        )

        # Wait until engine is running - we need to wait until the pod is created.
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_RUNNING.name

        pod = get_dai_pod(
            namespace=namespace, workspace_id=workspace_id, engine_id=engine_id
        )

        dai_container = next(
            (c for c in pod.spec.containers if c.name == "driverless-ai"), None
        )

        # Related triton DAI env var should not exist (because default value is true).
        triton_env_var = next(
            (e for e in dai_container.env if e.name == "DRIVERLESS_AI_ENABLE_TRITON_SERVER_LOCAL"), None
        )
        assert triton_env_var is None

        # SYS_NICE security capability must be present.
        assert 'SYS_NICE' in dai_container.security_context.capabilities.add
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(100)
def test_triton_disabled(
    dai_client,
    dai_engine_profile_19,
    dai_engine_version_v1_11_14,
):
    """
    Whitebox testing! (Pod spec is not accessible via API)
    Using workspace_id that has a related DriverlessAISetup.
    """
    config.load_config()

    workspace_id = "208d39bb-5407-4441-aa14-a79c7ce8ead1"
    engine_id = "engine2"
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
            profile=dai_engine_profile_19.name,
            dai_engine_version=dai_engine_version_v1_11_14.name,
        )

        # Wait until engine is running - we need to wait until the pod is created.
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_RUNNING.name

        pod = get_dai_pod(
            namespace=namespace, workspace_id=workspace_id, engine_id=engine_id
        )

        dai_container = next(
            (c for c in pod.spec.containers if c.name == "driverless-ai"), None
        )

        # Related triton DAI env var must be set to false.
        triton_env_var = next(
            (e for e in dai_container.env if e.name == "DRIVERLESS_AI_ENABLE_TRITON_SERVER_LOCAL"), None
        )
        assert triton_env_var is not None
        assert triton_env_var.value == "false"

        # SYS_NICE security capability must not be present in security capabilities.
        assert 'ALL' in dai_container.security_context.capabilities.drop
        add_capabilities = dai_container.security_context.capabilities.add
        if add_capabilities:
            assert 'SYS_NICE' not in add_capabilities
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )
