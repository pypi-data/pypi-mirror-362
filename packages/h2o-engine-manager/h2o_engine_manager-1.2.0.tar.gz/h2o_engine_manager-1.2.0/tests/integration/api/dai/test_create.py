import http
import os
import time

import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.api.dai.create_dai_request import *
from tests.integration.conftest import CACHE_SYNC_SECONDS
from tests.integration.sequential.adjusted_dai_profiles.test_adjusted_profile_get import (
    create_test_profile,
)


def incorrect_workspace_id(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.workspace_id = "no space in id allowed"
    return req


def incorrect_engine_id(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.engine_id = ""
    return req


def cpu_below_min(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.cpu = 0
    return req


def gpu_below_min(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.gpu = -5
    return req


def memory_below_min(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.memory_bytes = "1000"
    return req


def incorrect_storage(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.storage_bytes = "-2"
    return req


def incorrect_max_idle_duration(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.max_idle_duration = "-5s"
    return req


def incorrect_display_name(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.display_name = "I am definitely longer than 63 characters, there's no way I can pass validation"
    return req


def incorrect_version(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.version = "non-existing-version"
    return req


def deprecated_version(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.version = "1.10.4.1"
    return req


def incorrect_config(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.config = {"base_url": "whatever"}
    return req


def test_create_dai(dai_client):
    # When
    workspace_id = "bb4e89d6-fdc1-4e01-a046-9ea43669976b"
    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id="engine1",
        version="1.10.5-mock",
        cpu=1,
        gpu=0,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        max_idle_duration="2h",
        max_running_duration="12h",
        display_name="Proboscis monkey",
        config={"key1": "val1"},
    )

    # Then
    assert engine.name == f"workspaces/{workspace_id}/daiEngines/engine1"
    assert engine.state == DAIEngineState.STATE_STARTING
    assert engine.reconciling is True
    assert engine.cpu == 1
    assert engine.gpu == 0
    assert engine.max_idle_duration == "2h"
    assert engine.max_running_duration == "12h"
    assert engine.display_name == "Proboscis monkey"
    assert engine.annotations == {}
    assert engine.config == {"key1": "val1"}
    assert engine.create_time is not None
    assert engine.delete_time is None
    assert engine.resume_time is not None
    external_scheme = os.getenv("MANAGER_EXTERNAL_SCHEME")
    external_host = os.getenv("MANAGER_EXTERNAL_HOST")
    assert (
        engine.api_url
        == f"{external_scheme}://{external_host}/workspaces/{workspace_id}/daiEngines/engine1"
    )
    assert (
        engine.login_url
        == f"{external_scheme}://{external_host}/workspaces/{workspace_id}/daiEngines/engine1/oidc/login"
    )
    assert engine.creator.startswith("users/") and len(engine.creator) > len("users/")
    assert engine.creator_display_name == "test-user"
    assert engine.memory_bytes == "1Gi"
    assert engine.storage_bytes == "1Gi"


@pytest.mark.parametrize(
    "modify_func",
    [
        incorrect_workspace_id,
        incorrect_engine_id,
        cpu_below_min,
        gpu_below_min,
        memory_below_min,
        incorrect_display_name,
        incorrect_version,
        deprecated_version,
        incorrect_config,
    ],
)
def test_create_dai_server_validation(dai_client, modify_func):
    # When
    workspace_id = "a2533922-9794-486b-b494-d40700d47a1c"
    req = modify_func(CreateDAIEngineRequest(workspace_id=workspace_id))

    # Then
    with pytest.raises(CustomApiException) as exc:
        create_dai_from_request(dai_client, req)
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "modify_func", [incorrect_storage, incorrect_max_idle_duration]
)
def test_create_dai_client_validation(dai_client, modify_func):
    # When
    workspace_id = "a2533922-9794-486b-b494-d40700d47a1c"
    req = modify_func(CreateDAIEngineRequest(workspace_id=workspace_id))

    # Then
    with pytest.raises(ValueError) as exc:
        create_dai_from_request(dai_client, req)


def test_create_already_exists(dai_client):
    # When an engine is created
    workspace_id = "7919f397-d59c-4a9b-99f3-b914aa29349d"
    req = CreateDAIEngineRequest(workspace_id=workspace_id)
    create_dai_from_request(dai_client, req)

    # Then engine with the same IDs cannot be created again.
    with pytest.raises(CustomApiException) as exc:
        create_dai_from_request(dai_client, req)
    assert exc.value.status == http.HTTPStatus.CONFLICT

    # Check that validate only also returns Conflict.
    req.validate_only = True
    with pytest.raises(CustomApiException) as exc:
        create_dai_from_request(dai_client, req)
    assert exc.value.status == http.HTTPStatus.CONFLICT


def test_create_validate_only(dai_client):
    # When engine is not really created
    workspace_id = "359ad2c5-7709-4e64-97db-a6218ccabe8d"
    req = CreateDAIEngineRequest(
        workspace_id=workspace_id, validate_only=True
    )
    create_dai_from_request(dai_client, req)

    # Then it cannot be found
    with pytest.raises(CustomApiException) as exc:
        dai_client.get_engine(
            workspace_id=workspace_id, engine_id="engine1"
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_create_optional_values(dai_client):
    # Default values should be applied.
    workspace_id = "59bcc361-d392-4aae-8144-c66cda3e425f"
    e = dai_client.create_engine(
        workspace_id=workspace_id, engine_id="e1"
    )
    assert e.cpu == 1
    assert e.gpu == 0
    assert e.memory_bytes == "1Gi"
    assert e.storage_bytes == "1Gi"
    assert e.max_idle_duration == "4h"
    assert e.max_running_duration == "4h"


def test_create_engine_id_generator(dai_client):
    # Engine ID should be uniquely generated if not provided
    workspace_id = "c14e49ab-cfd7-4ad2-9130-5848258584d8"
    no_param_1 = dai_client.create_engine(workspace_id=workspace_id)
    time.sleep(CACHE_SYNC_SECONDS)
    no_param_2 = dai_client.create_engine(workspace_id=workspace_id)
    assert no_param_1.name != no_param_2.name

    # Engine ID should be uniquely generated from display name
    display_name_1 = dai_client.create_engine(workspace_id=workspace_id, display_name="Smoker@2023")
    time.sleep(CACHE_SYNC_SECONDS)
    display_name_2 = dai_client.create_engine(workspace_id=workspace_id, display_name="Smoker@2023")
    assert display_name_1.name != display_name_2.name


def test_create_dai_with_profile(dai_profile_client, dai_client):
    # Setup
    profile = create_test_profile(dai_profile_client)

    try:
        # When
        req = CreateDAIEngineRequest(
            workspace_id="b684f009-7c06-43df-a9df-2d39018630a5",
            profile_id="my-profile",
            cpu=None,
            gpu=None,
            memory_bytes=None,
            storage_bytes=None,
            version="1.10.5-mock",
        )
        eng = create_dai_from_request(dai_client, req)

        # Then
        assert eng.cpu == 20
        assert eng.gpu == 30
        assert eng.memory_bytes == "1000Gi"
        assert eng.storage_bytes == "1000Gi"
    finally:
        dai_profile_client.delete_profile(profile_id=profile.dai_profile_id)
