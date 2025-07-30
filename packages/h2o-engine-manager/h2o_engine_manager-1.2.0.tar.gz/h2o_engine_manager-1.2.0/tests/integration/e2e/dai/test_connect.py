import pytest
import websocket

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState


@pytest.mark.timeout(200)
def test_dai_logs(
    dai_client,
    websocket_base_url,
    dai_engine_version_v1_11_6,
    dai_engine_profile_13,
):
    workspace_id = "3a991d92-b792-4094-8a34-dd975c8fde87"
    engine_id = "whatever"

    # Create engine
    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        cpu=1,
        gpu=0,
        memory_bytes="8Gi",
        storage_bytes="16Gi",
        max_idle_duration="15m",
        max_running_duration="2d",
        display_name="Whatever",
        profile=dai_engine_profile_13.name,
        dai_engine_version=dai_engine_version_v1_11_6.name,
    )
    try:
        ws = websocket.WebSocket()
        ws.connect(
            url=f"{websocket_base_url}/v1/{engine.name}:stream_logs?follow=true",
            header=[
                f"Authorization: Bearer {dai_client.client_info.token_provider.token()}"
            ],
        )

        # Test not-available logs message.
        # Every 2 seconds the DAIEngine exists but the DAI container is not running yet, a not-available message is sent
        # to the websocket client from AIEM server (websocket server).
        # Mocked DAI server takes 5 seconds to startup -> there should be at least two not-available websocket messages.
        assert ws.recv() == "Driverless AI logs are not available yet\n"
        assert ws.recv() == "Driverless AI logs are not available yet\n"

        # Need to close the websocket connection to throw away all other not-available message.
        ws.close()

        # Wait for RUNNING DAIEngine.
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_RUNNING.name

        # Reconnect to the websocket server again (now only the log lines should be sent from server because the DAI
        # container is running).
        ws.connect(
            url=f"{websocket_base_url}/v1/{engine.name}:stream_logs?follow=true",
            header=[
                f"Authorization: Bearer {dai_client.client_info.token_provider.token()}"
            ],
        )

        # Test reading first 3 logs lines of running engine.
        read_lines = 3
        ws_lines = []
        for l in range(read_lines):
            ws_lines.append(ws.recv())
        ws.close()

        # We know exactly that mocked DAI server prints these 3 logs lines as first on startup.
        want_lines = [
            "DRIVERLESS AI 1.10.3\n",
            "Starting mock DAI server on port 12345\n",
            "health endpoint provided at /apis/health/v1\n",
        ]

        assert ws_lines == want_lines

        # Test downloading logs.
        downloaded_lines = engine.download_logs().splitlines(keepends=True)[0:read_lines]

        # Test that the first 3 downloaded lines are the same as the streamed lines.
        assert downloaded_lines == ws_lines
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )
