import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState


def test_dai_connect(
    dai_client,
    dai_engine_profile_26,
    dai_engine_version_v1_11_23,
):
    workspace_id = "1b829a5a-7b6e-44f0-853e-926dfb5095ec"
    engine_id = "dai-connect"

    # Create engine
    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        cpu=1,
        gpu=0,
        memory_bytes="8Gi",
        storage_bytes="16Gi",
        max_idle_duration="15m",
        max_running_duration="2d",
        display_name="My DAIEngine connect",
        profile=dai_engine_profile_26.name,
        dai_engine_version=dai_engine_version_v1_11_23.name,
    )
    try:
        #  Unable to connect before the engine is running.
        with pytest.raises(RuntimeError):
            engine.connect()

        # Wait for RUNNING
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_RUNNING.name

        # Test Connect to DAI.
        engine.connect()
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}",
            allow_missing=True,
        )
