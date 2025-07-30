import os
import time

from h2o_engine_manager.clients.h2o_engine.state import H2OEngineState
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_get(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    workspace_id = "6f32a0fc-2745-42e9-9314-a1e5dc151e00"
    engine_id = "get-h2o-engine"

    # Given
    h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        node_count=1,
        cpu=1,
        gpu=0,
        memory_bytes="2Gi",
        max_idle_duration="2h",
        max_running_duration="12h",
        display_name="Proboscis monkey",
        annotations={"foo": "bar"},
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    time.sleep(CACHE_SYNC_SECONDS)

    # When
    e = h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)

    # Then
    assert e.name == f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
    assert e.state == H2OEngineState.STATE_STARTING
    assert e.reconciling is True
    assert e.node_count == 1
    assert e.cpu == 1
    assert e.gpu == 0
    assert e.max_idle_duration == "2h"
    assert e.max_running_duration == "12h"
    assert e.display_name == "Proboscis monkey"
    assert e.annotations == {"foo": "bar"}
    assert e.create_time is not None
    assert e.delete_time is None
    external_host = os.getenv("MANAGER_EXTERNAL_HOST")
    external_scheme = os.getenv("MANAGER_EXTERNAL_SCHEME")
    assert (
        e.api_url
        == f"{external_scheme}://{external_host}/workspaces/{workspace_id}/h2oEngines/{engine_id}"
    )
    assert (
        e.login_url
        == f"{external_scheme}://{external_host}/workspaces/{workspace_id}/h2oEngines/{engine_id}/flow/index.html"
    )
    assert e.creator.startswith("users/") and len(e.creator) > len("users/")
    assert e.creator_display_name == "test-user"
    assert e.memory_bytes == "2Gi"
