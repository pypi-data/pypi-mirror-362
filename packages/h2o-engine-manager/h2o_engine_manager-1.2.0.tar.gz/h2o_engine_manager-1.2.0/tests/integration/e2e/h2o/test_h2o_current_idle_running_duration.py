import time

import pytest


# Overwriting default pytest timeout for this long-running test method.
@pytest.mark.timeout(180)
def test_current_idle_running_duration(
    h2o_engine_client,
    h2o_engine_profile_p8,
    h2o_engine_version_v6,
):
    """
    Main goal of this is to verify the current idle and runtime duration is properly detected.
    """

    workspace_id = "default"
    engine_id = "e1"

    # Create engine
    engine = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=h2o_engine_profile_p8.name,
        h2o_engine_version=h2o_engine_version_v6.name,
    )
    try:
        # Wait for RUNNING
        engine.wait()
        # Wait a few seconds
        time.sleep(5)
        e = h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
        # Verify the current idle and runtime duration.
        assert int(e.current_idle_duration.rstrip("s")) > 0
        assert int(e.current_running_duration.rstrip("s")) > 5

    finally:
        h2o_engine_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
            name_4=f"workspaces/{workspace_id}/h2oEngines/{engine_id}",
            allow_missing=True,
        )
