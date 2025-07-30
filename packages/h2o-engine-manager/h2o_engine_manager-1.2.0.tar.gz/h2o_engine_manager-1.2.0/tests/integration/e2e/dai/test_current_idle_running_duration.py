import time

import pytest


@pytest.mark.timeout(180)
def test_current_idle_running_duration(
    dai_client,
    dai_engine_profile_14,
    dai_engine_version_v1_11_7,
):
    """
    Main goal of this is to verify the current idle and runtime duration is properly detected.
    """
    workspace_id = "d6082dfa-8143-4064-8b15-a9a11afb7284"
    engine_id = "e1"

    # Create engine
    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=dai_engine_profile_14.name,
        dai_engine_version=dai_engine_version_v1_11_7.name,
    )
    try:
        # Wait for RUNNING
        engine.wait()
        # Wait a few seconds
        time.sleep(10)
        e = dai_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
        # Verify the current idle and runtime duration.
        initial_idle = int(e.current_idle_duration.rstrip("s"))
        initial_runtime = int(e.current_running_duration.rstrip("s"))

        assert initial_idle > 5
        assert initial_runtime > 5

        e.pause()
        e.wait()
        e.resume()
        e.wait()

        # Verify the current idle and runtime resets with the engine resume (is lower than on the initial run)
        #  assert int(e.current_idle_duration.rstrip("s")) < initial_idle
        assert int(e.current_running_duration.rstrip("s")) < initial_runtime

    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}", allow_missing=True
        )
