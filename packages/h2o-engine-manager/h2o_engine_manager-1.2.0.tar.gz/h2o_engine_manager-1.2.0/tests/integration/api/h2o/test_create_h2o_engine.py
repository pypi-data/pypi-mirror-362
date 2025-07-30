import http
import json
import os
import time

import pytest

from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.h2o_engine.state import H2OEngineState
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_create(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    # When
    workspace_id = "77e0c306-6113-4db1-bd39-a90a019f9187"
    engine_id = "create-h2o-engine-engine1"

    engine = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        node_count=2,
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

    # Then
    assert engine.name == f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
    assert engine.state == H2OEngineState.STATE_STARTING
    assert engine.reconciling is True
    assert engine.node_count == 2
    assert engine.cpu == 1
    assert engine.gpu == 0
    assert engine.max_idle_duration == "2h"
    assert engine.max_running_duration == "12h"
    assert engine.display_name == "Proboscis monkey"
    assert engine.annotations == {"foo": "bar"}
    assert engine.create_time is not None
    assert engine.delete_time is None
    external_scheme = os.getenv("MANAGER_EXTERNAL_SCHEME")
    external_host = os.getenv("MANAGER_EXTERNAL_HOST")
    assert (
        engine.api_url
        == f"{external_scheme}://{external_host}/workspaces/{workspace_id}/h2oEngines/{engine_id}"
    )
    assert (
        engine.login_url
        == f"{external_scheme}://{external_host}/workspaces/{workspace_id}/h2oEngines/{engine_id}/flow/index.html"
    )
    assert engine.creator.startswith("users/") and len(engine.creator) > len("users/")
    assert engine.creator_display_name == "test-user"
    assert engine.memory_bytes == "2Gi"
    assert engine.profile == h2o_engine_profile_p4.name
    assert engine.profile_info is not None
    assert engine.h2o_engine_version == h2o_engine_version_v1.name
    assert engine.h2o_engine_version_info is not None


def test_create_default_values(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    workspace_id = "77e0c306-6113-4db1-bd39-a90a019f9187"
    engine_id = "create-h2o-engine-engine-default-values"

    engine = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    # Then default values are filled from workspace constraints (see system.default H2OSetup)
    assert engine.node_count == 1
    assert engine.cpu == 1
    assert engine.gpu == 0
    assert engine.memory_bytes == "20Mi"
    assert engine.max_idle_duration == "4h"
    assert engine.max_running_duration == "4h"

    # Other fields are set according to API
    assert (
        engine.name == f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
    )
    assert engine.state == H2OEngineState.STATE_STARTING
    assert engine.reconciling is True
    assert engine.display_name == ""
    assert engine.annotations == {}
    assert engine.create_time is not None
    assert engine.delete_time is None
    external_scheme = os.getenv("MANAGER_EXTERNAL_SCHEME")
    external_host = os.getenv("MANAGER_EXTERNAL_HOST")
    assert (
        engine.api_url
        == f"{external_scheme}://{external_host}/workspaces/{workspace_id}/h2oEngines/{engine_id}"
    )
    assert (
        engine.login_url
        == f"{external_scheme}://{external_host}/workspaces/{workspace_id}/h2oEngines/{engine_id}/flow/index.html"
    )
    assert engine.creator.startswith("users/") and len(engine.creator) > len("users/")
    assert engine.creator_display_name == "test-user"
    assert engine.profile == h2o_engine_profile_p4.name
    assert engine.profile_info is not None
    assert engine.h2o_engine_version == h2o_engine_version_v1.name
    assert engine.h2o_engine_version_info is not None


def test_create_validation(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    workspace_id = "77e0c306-6113-4db1-bd39-a90a019f9187"
    engine_id = "create-h2o-engine-validation"

    with pytest.raises(CustomApiException) as exc:
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            memory_bytes="1Mi",  # violates constraint for minimal memory bytes
            profile=h2o_engine_profile_p4.name,
            h2o_engine_version=h2o_engine_version_v1.name,
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_create_validation_unavailable_version(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
):
    workspace_id = "77e0c306-6113-4db1-bd39-a90a019f9187"
    engine_id = "create-h2o-engine-validation-unavailable-version"
    with pytest.raises(CustomApiException) as exc:
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=h2o_engine_profile_p4.name,
            h2o_engine_version="workspaces/global/h2oEngineVersions/foo",
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST
    assert 'h2o_engine_version workspaces/global/h2oEngineVersions/foo not found' == json.loads(exc.value.body)[
        "message"]


def test_create_engine_id_generator_and_default_profile_version(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    workspace_id = "77e0c306-6113-4db1-bd39-a90a019f9187"

    # Engine ID should be uniquely generated if not provided
    no_param_1 = h2o_engine_client.create_engine(
        workspace_id=workspace_id
    )
    time.sleep(CACHE_SYNC_SECONDS)
    no_param_2 = h2o_engine_client.create_engine(workspace_id=workspace_id)
    assert no_param_1.name != no_param_2.name

    # Engine ID should be uniquely generated from display name
    display_name_1 = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        display_name="Smoker@2023",
    )
    time.sleep(CACHE_SYNC_SECONDS)
    display_name_2 = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        display_name="Smoker@2023",
    )
    assert display_name_1.name != display_name_2.name
