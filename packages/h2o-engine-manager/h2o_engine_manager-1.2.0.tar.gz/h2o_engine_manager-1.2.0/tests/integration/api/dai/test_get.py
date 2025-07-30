import http
import time

import pytest

from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.api.dai.create_dai_request import *
from tests.integration.conftest import CACHE_SYNC_SECONDS


@pytest.mark.parametrize(
    ["workspace_id", "engine_id"],
    [
        ("non-existing-workspace", "engine1"),
        ("default", "get-dai-validation-non-existing-engine"),
    ],
)
def test_get_validation(dai_client, workspace_id, engine_id):
    with pytest.raises(CustomApiException) as exc:
        dai_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_get(dai_client):
    # When
    req = CreateDAIEngineRequest(workspace_id="default", engine_id="test-get-engine1")
    create_dai_from_request(dai_client, req)
    time.sleep(CACHE_SYNC_SECONDS)

    # Then
    dai_client.set_default_workspace_id(default_workspace_id="default")
    dai_client.get_engine(engine_id="test-get-engine1")
