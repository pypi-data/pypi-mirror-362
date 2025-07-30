import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from tests.integration.conftest import DAI_LIFECYCLE_WORKSPACE


@pytest.mark.timeout(180)
def test_dai_lifecycle(
    dai_client,
    websocket_base_url,
    dai_engine_profile_12,
    dai_engine_version_v1_11_5,
):
    """
    Main goal of this test is to make sure the real DAIEngine instance can
    walk through its whole life cycle using AIEM API.
    """

    workspace_id = DAI_LIFECYCLE_WORKSPACE
    engine_id = "engine-lifecycle"

    # Test Create
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
        config={"max_runtime_minutes": "120", "feature_engineering_effort": "5"},
        profile=dai_engine_profile_12.name,
        dai_engine_version=dai_engine_version_v1_11_5.name,
    )
    deleted = False

    try:
        assert engine.name == f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        assert engine.state.name == DAIEngineState.STATE_STARTING.name
        assert engine.gpu == 0

        # Test Pause during STARTING.
        engine.pause()
        assert engine.state.name == DAIEngineState.STATE_PAUSING.name

        # Test Pause noop. Engine can be already paused (current state is updated even for noop).
        engine.pause()
        assert engine.state.name in [
            DAIEngineState.STATE_PAUSING.name,
            DAIEngineState.STATE_PAUSED.name,
        ]

        # Test Wait for PAUSED.
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        # Test Resume
        engine.resume()
        assert engine.state.name == DAIEngineState.STATE_STARTING.name

        # Test Resume noop. Engine can be already running (current state is updated even for noop).
        engine.resume()
        assert engine.state.name in [
            DAIEngineState.STATE_STARTING.name,
            DAIEngineState.STATE_RUNNING.name,
        ]

        # Test Wait for RUNNING
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_RUNNING.name

        # Test Get
        engine = dai_client.get_engine(
            engine_id=engine.engine_id, workspace_id=engine.workspace_id
        )
        assert engine.state.name == DAIEngineState.STATE_RUNNING.name

        # Test List with default parameters.
        page = dai_client.list_engines(workspace_id=workspace_id)
        assert len(page.engines) == 1
        assert page.next_page_token == ""

        # Test List with additional parameters.
        page = dai_client.list_engines(
            workspace_id=workspace_id,
            page_size=2,
            order_by="cpu",
            filter="state = STATE_RUNNING",
        )
        assert len(page.engines) == 1
        assert page.next_page_token == ""

        # Test help function list_all.
        engines = dai_client.list_all_engines(workspace_id=workspace_id)
        assert len(engines) == 1

        # Test Pause
        engine.pause()
        assert engine.state.name == DAIEngineState.STATE_PAUSING.name

        # Test Wait for PAUSED
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        # Test Update
        engine.cpu = 2
        engine.update()
        assert engine.cpu == 2

        # Test Resume
        engine.resume()
        assert engine.state.name == DAIEngineState.STATE_STARTING.name

        # Test Wait for RUNNING
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_RUNNING.name

        # Test engine reports disk size
        assert engine.free_disk_size_bytes != ""
        assert engine.total_disk_size_bytes != ""

        # Test Delete
        engine.delete()

        # This test case is supposed to run in real test environment. Therefore, we expect the engine to
        # take some time to be deleted.
        # Check that the returned engine still exists and has fields set accordingly.
        assert engine is not None
        assert engine.state == DAIEngineState.STATE_DELETING

        # Check that the engine is not found after some time (is deleted).
        engine.wait(timeout_seconds=100)
        deleted = True
    finally:
        allow_missing = False
        if deleted:
            allow_missing = True

        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}",
            allow_missing=allow_missing,
        )
