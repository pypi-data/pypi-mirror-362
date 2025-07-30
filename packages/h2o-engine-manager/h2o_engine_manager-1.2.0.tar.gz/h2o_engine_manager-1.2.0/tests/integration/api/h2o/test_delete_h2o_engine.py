import http
import time

import pytest

from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.h2o_engine.state import H2OEngineState
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_delete_validate_only(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    workspace_id = "764326fa-cfbf-4ecb-87a5-3061de18e379"
    engine_id = "delete-h2o-validate"

    e = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        node_count=1,
        cpu=1,
        gpu=0,
        max_idle_duration="5h",
        max_running_duration="10h",
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    e.delete(validate_only=True)

    # Although not deleted, the response should behave as if it was deleted.
    # Double-check that engine still exists (no exception is thrown) and it's not in DELETING state.
    time.sleep(CACHE_SYNC_SECONDS)
    e = h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
    assert e.state != H2OEngineState.STATE_DELETING


@pytest.mark.timeout(180)
def test_delete(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    workspace_id = "764326fa-cfbf-4ecb-87a5-3061de18e379"
    engine_id = "delete-h2o"

    e = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        node_count=1,
        cpu=1,
        gpu=0,
        max_idle_duration="5h",
        max_running_duration="10h",
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    e.delete()

    # This test case is supposed to run in simplified test environment. Therefore, it can happen
    # that the engine was deleted so quickly, that AIEM had nothing to return.
    # Check delete-related fields only if the engine was returned by AIEM.
    if e is not None:
        assert e.delete_time is not None
        assert e.state == H2OEngineState.STATE_DELETING

    # Check that the engine is not found after some time (is deleted).
    e.wait(timeout_seconds=60)

    with pytest.raises(CustomApiException) as exc:
        h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
