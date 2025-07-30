import pytest

from h2o_engine_manager.clients.h2o_engine.state import H2OEngineState


@pytest.mark.timeout(180)
def test_terminate_h2o_engine_immediately(
    h2o_engine_client,
    h2o_engine_profile_p7,
    h2o_engine_version_v5,
):
    workspace_id = "default"
    engine_id = "test-terminate-h2o-engine"

    e = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=h2o_engine_profile_p7.name,
        h2o_engine_version=h2o_engine_version_v5.name,
    )
    deleted = False

    try:
        assert e.state.name == H2OEngineState.STATE_STARTING.name

        # Do not wait until engine is running, terminate it during starting.
        e.terminate()
        assert e.state.name == H2OEngineState.STATE_TERMINATING.name

        e.wait()
        assert e.state.name == H2OEngineState.STATE_TERMINATED.name

        e.delete()
        e.wait()
        deleted = True
    finally:
        allow_missing = False
        if deleted:
            allow_missing = True

        h2o_engine_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
            name_4=f"workspaces/{workspace_id}/h2oEngines/{engine_id}",
            allow_missing=allow_missing,
        )
