import http
import time

import pytest

from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.login import Clients


# This test is a workaround for AuthZ race-condition issue where the default workspace resolution is not working
# in a parallel test case scenarios.
# The default workspace must be resolved sequentially before any actual parallel testing begins.
def test_default_workspace_resolution(clients: Clients, admin_clients: Clients, super_admin_clients: Clients):
    with pytest.raises(CustomApiException) as exc:
        clients.dai_engine_client.get_engine(workspace_id="default", engine_id="e")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND

    time.sleep(2)

    with pytest.raises(CustomApiException) as exc:
        admin_clients.dai_engine_client.get_engine(workspace_id="default", engine_id="e")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND

    time.sleep(2)

    with pytest.raises(CustomApiException) as exc:
        super_admin_clients.dai_engine_client.get_engine(workspace_id="default", engine_id="e")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
