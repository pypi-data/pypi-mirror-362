import http
import time

import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.api.dai.create_dai_request import *
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_delete_validate_only(dai_client):
    workspace_id = "default"
    engine_id = "test-delete-validate-only"

    req = CreateDAIEngineRequest(workspace_id=workspace_id, engine_id=engine_id)
    e = create_dai_from_request(dai_client, req)

    e.delete(validate_only=True)

    # Although not deleted, the response should behave as if it was deleted.
    # Double-check that engine still exists. (No exception is thrown)
    time.sleep(CACHE_SYNC_SECONDS)
    e = dai_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)


def test_delete(dai_client):
    workspace_id = "default"
    engine_id = "test-delete"

    req = CreateDAIEngineRequest(workspace_id=workspace_id, engine_id=engine_id)
    e = create_dai_from_request(dai_client, req)

    e.delete()

    # This test case is supposed to run in simplified test environment. Therefore, it can happen
    # that the engine was deleted so quickly, that AIEM had nothing to return.
    # Check delete-related fields only if the engine was returned by AIEM.
    if e is not None:
        assert e.delete_time is not None
        assert e.state == DAIEngineState.STATE_DELETING

    # Check that the engine is not found after some time (is deleted).
    e.wait(timeout_seconds=10)
    with pytest.raises(CustomApiException) as exc:
        dai_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
