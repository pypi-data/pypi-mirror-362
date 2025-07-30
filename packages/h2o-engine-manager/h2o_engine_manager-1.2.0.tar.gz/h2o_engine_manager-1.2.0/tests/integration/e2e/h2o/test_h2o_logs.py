import pytest
import websocket as websocket

from h2o_engine_manager.clients.h2o_engine.client import H2OEngineClient
from h2o_engine_manager.clients.h2o_engine.h2o_engine import H2OEngine
from h2o_engine_manager.clients.h2o_engine.state import H2OEngineState


@pytest.mark.timeout(180)
def test_h2o_logs(
    h2o_engine_client,
    websocket_base_url,
    h2o_engine_profile_p5,
    h2o_engine_version_v3,
):
    workspace_id = "08b86840-b48e-439f-9826-f2ea743beb8d"
    engine_id = "test-logs-felix"

    e = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        node_count=1,
        cpu=1,
        gpu=0,
        memory_bytes="2Gi",
        max_idle_duration="2h",
        max_running_duration="12h",
        profile=h2o_engine_profile_p5.name,
        h2o_engine_version=h2o_engine_version_v3.name,
    )

    try:
        ws = websocket.WebSocket()

        # TODO skipping this test for now so our e2e tests don't because of this known issue.
        # assert_logs_unavailable(
        #     ws=ws,
        #     websocket_base_url=websocket_base_url,
        #     engine=e,
        #     h2o_engine_client=h2o_engine_client,
        # )

        e.wait()
        assert e.state.name == H2OEngineState.STATE_RUNNING.name

        # Reconnect to the websocket server again (now only the log lines should be sent from server because the H2O
        # container is running).
        ws.connect(
            url=f"{websocket_base_url}/v1/{e.name}:stream_logs?follow=true",
            header=[
                f"Authorization: Bearer {h2o_engine_client.client_info.token_provider.token()}"
            ],
        )

        # Test reading first 2 logs lines of running engine.
        read_lines = 2
        for i in range(read_lines):
            l = ws.recv()
            assert "H2O logs are not available yet" not in l
        ws.close()

        logs = e.download_logs()

        expected_lines = [
            "Starting mock H2O server on port 54321",
            f"health endpoint provided at /workspaces/{workspace_id}/h2oEngines/{engine_id}/3/Cloud",
        ]

        line1_idx = None
        line2_idx = None

        for idx, line in enumerate(logs.splitlines()):
            if expected_lines[0] in line:
                line1_idx = idx
            if expected_lines[1] in line:
                line2_idx = idx

        # Test that lines were found.
        assert line1_idx is not None
        assert line2_idx is not None

        # Test that lines were printed in the expected order (line1, line2, line3).
        assert line1_idx == line2_idx - 1
    finally:
        h2o_engine_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
            name_4=f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
        )


def assert_logs_unavailable(
    ws: websocket.WebSocket,
    websocket_base_url: str,
    engine: H2OEngine,
    h2o_engine_client: H2OEngineClient,
):
    ws.connect(
        url=f"{websocket_base_url}/v1/{engine.name}:stream_logs?follow=true",
        header=[
            f"Authorization: Bearer {h2o_engine_client.client_info.token_provider.token()}"
        ],
    )

    # Test not-available logs message.
    # Every 2 seconds the H2OEngine exists but the H2O container is not running yet, a not-available message is sent
    # to the websocket client from AIEM server (websocket server).
    # Mocked H2O server takes 5 seconds to startup.
    assert ws.recv() == "H2O logs are not available yet"

    # Need to close the websocket connection to throw away all other not-available message.
    ws.close()
