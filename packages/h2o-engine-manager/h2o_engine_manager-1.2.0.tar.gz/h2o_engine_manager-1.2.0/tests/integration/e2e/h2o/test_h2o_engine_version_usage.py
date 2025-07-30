import http
import json
import os

import pytest
from kubernetes import config

from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.h2o_engine.h2o_engine_version_info import (
    H2OEngineVersionInfo,
)
from h2o_engine_manager.clients.h2o_engine_version.version import H2OEngineVersion
from tests.integration.e2e.dai.test_dai_engine_profile_usage import (
    assert_equal_datetimes_up_to_seconds,
)
from tests.integration.e2e.h2o.test_h2o_engine_profile_usage import (
    assert_profile_equal_profile_info,
)
from tests.integration.e2e.h2o.test_h2o_engine_profile_usage import get_kube_h2o


@pytest.mark.timeout(180)
def test_h2o_engine_version_usage(
    h2o_engine_client,
    h2o_engine_admin_client,
    h2o_engine_profile_p2,
    h2o_engine_version_v0_0_0_1,
):
    """
    White-box testing using k8s client to check that H2OEngineVersion is persisted correctly in kubeH2OEngine Spec.
    (These fields are not available via API, need to access directly via k8s).
    """
    config.load_config()

    workspace_id = "035a4779-2b49-445a-bb0b-b9d03df7a3e5"
    engine_id = "h2o-engine-version-usage"
    namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

    try:
        with pytest.raises(CustomApiException) as exc:
            h2o_engine_client.create_engine(
                workspace_id=workspace_id,
                engine_id=engine_id,
                profile=h2o_engine_profile_p2.name,
                h2o_engine_version="workspaces/global/h2oEngineVersions/0.0.0.1-non-existing"
            )
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert f'h2o_engine_version workspaces/global/h2oEngineVersions/0.0.0.1-non-existing not found' \
               in json.loads(exc.value.body)["message"]

        engine = h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=h2o_engine_profile_p2.name,
            h2o_engine_version=h2o_engine_version_v0_0_0_1.name,
        )

        assert engine.name == f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
        assert engine.profile == h2o_engine_profile_p2.name
        assert_profile_equal_profile_info(profile=h2o_engine_profile_p2, profile_info=engine.profile_info)
        assert engine.h2o_engine_version == h2o_engine_version_v0_0_0_1.name
        assert_version_equal_version_info(version=h2o_engine_version_v0_0_0_1, version_info=engine.h2o_engine_version_info)

        # Test H2OEngineVersion is correctly persisted in kubeH2OEngine Spec.
        kube_eng = get_kube_h2o(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        img = "353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest"
        assert kube_eng["metadata"]["annotations"]["engine.h2o.ai/gpu-resource-name"] == "amd.com/gpu"
        # The old version is not set.
        assert "engine.h2o.ai/version" not in kube_eng["metadata"]["annotations"]
        assert kube_eng["spec"]["image"] == img
        assert kube_eng["spec"]["imagePullPolicy"] == "IfNotPresent"
        assert kube_eng["spec"]["imagePullSecrets"] == [{"name": "regcred"}]

        # Test GetH2OEngine
        engine_get = h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
        assert engine_get.name == f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
        assert engine_get.h2o_engine_version == h2o_engine_version_v0_0_0_1.name
        assert_version_equal_version_info(
            version=h2o_engine_version_v0_0_0_1,
            version_info=engine_get.h2o_engine_version_info
        )

        # Test ListH2OEngines
        engines = h2o_engine_client.list_all_engines(workspace_id=workspace_id)
        assert len(engines) == 1
        assert engines[0].name == f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
        assert engines[0].h2o_engine_version == h2o_engine_version_v0_0_0_1.name
        assert_version_equal_version_info(
            version=h2o_engine_version_v0_0_0_1,
            version_info=engines[0].h2o_engine_version_info,
        )
    finally:
        h2o_engine_admin_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
            name_4=f"workspaces/{workspace_id}/h2oEngines/{engine_id}", allow_missing=True
        )


def assert_version_equal_version_info(version: H2OEngineVersion, version_info: H2OEngineVersionInfo):
    assert version.name == version_info.name
    assert version.deprecated == version_info.deprecated
    assert version.aliases == version_info.aliases
    assert version.image == version_info.image
    assert version.image_pull_policy == version_info.image_pull_policy
    assert version.image_pull_secrets == version_info.image_pull_secrets
    assert_equal_datetimes_up_to_seconds(version.create_time, version_info.create_time)
    assert_equal_datetimes_up_to_seconds(version.update_time, version_info.update_time)
    assert version.creator == version_info.creator
    assert version.updater == version_info.updater
    assert version.creator_display_name == version_info.creator_display_name
    assert version.updater_display_name == version_info.updater_display_name
