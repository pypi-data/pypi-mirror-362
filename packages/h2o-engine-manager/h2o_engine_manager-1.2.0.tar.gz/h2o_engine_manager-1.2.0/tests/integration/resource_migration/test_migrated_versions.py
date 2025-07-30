from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import FailedEngineException


def test_migrated_versions(
    dai_client,
    h2o_engine_client,
    dai_engine_profile_p28,
):
    """
    DAIEngine and H2OEngine are created manually via k8s with old versions.
    Check that after AIEM server is started and up (which is now), the old versions are migrated to new versions.
    """

    workspace_id = "829cee5d-a40e-48a5-879d-5bbe5d4fec93"
    dai_engine_id = "old-dai-engine"
    h2o_engine_id = "old-h2o-engine"

    dai_engine = dai_client.get_engine(workspace_id=workspace_id, engine_id=dai_engine_id)
    assert dai_engine.dai_engine_version == "workspaces/global/daiEngineVersions/1.10.6.1"

    h2o_engine = h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id=h2o_engine_id)
    assert h2o_engine.h2o_engine_version == "workspaces/global/h2oEngineVersions/3.40.0.4"

    # Extra test that DAIEngine without DAIEngineProfile can be set to that profile

    try:
        dai_engine.pause()
        dai_engine.wait()
    except FailedEngineException:
        # Engine may end up in failed state (direct creation via k8s may cause that, it's not reliable)
        pass
    finally:
        # Engine should end up either in PAUSED or FAILED state.
        assert dai_engine.state in [DAIEngineState.STATE_PAUSED, DAIEngineState.STATE_FAILED]

    dai_engine.profile = dai_engine_profile_p28.name
    dai_engine.update()
    assert dai_engine.profile == dai_engine_profile_p28.name

    # ExtraExtra check.
    dai_engine = dai_client.get_engine(workspace_id=workspace_id, engine_id=dai_engine_id)
    assert dai_engine.dai_engine_version == "workspaces/global/daiEngineVersions/1.10.6.1"
    assert dai_engine.profile == dai_engine_profile_p28.name
