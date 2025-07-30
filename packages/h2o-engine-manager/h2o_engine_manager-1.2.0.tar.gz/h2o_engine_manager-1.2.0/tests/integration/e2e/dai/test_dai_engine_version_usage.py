import http
import json
import os

import pytest
from kubernetes import config

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.dai_engine.dai_engine_version_info import (
    DAIEngineVersionInfo,
)
from h2o_engine_manager.clients.dai_engine_version.version import DAIEngineVersion
from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.e2e.dai.test_dai_engine_profile_usage import (
    assert_equal_datetimes_up_to_seconds,
)
from tests.integration.e2e.dai.test_dai_resume import get_kube_dai


@pytest.mark.timeout(180)
def test_dai_engine_version_usage(
    dai_client,
    dai_admin_client,
    dai_engine_version_client_super_admin,
    dai_engine_profile_p8_for_all,
    dai_engine_version_v1_11_0,
    dai_engine_version_v1_11_1,
    dai_engine_version_v1_11_2,
    dai_engine_version_v1_11_3,
    dai_engine_version_v2_0_0,
):
    """
    White-box testing using k8s client to check that DAIEngineVersion is persisted correctly in kubeDAIEngine Spec.
    (These fields are not available via API, need to access directly via k8s).
    """
    config.load_config()

    workspace_id = "a6ff0166-e3df-4a48-9e73-27df75ac19bb"
    engine_id = "dai-engine-version-usage"
    namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=dai_engine_profile_p8_for_all.name,
        dai_engine_version=dai_engine_version_v1_11_1.name,
    )

    try:
        assert engine.name == f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        assert engine.dai_engine_version == dai_engine_version_v1_11_1.name
        assert_version_equal_version_info(
            version=dai_engine_version_v1_11_1,
            version_info=engine.dai_engine_version_info,
        )
        # Engine has version v1. version v3 is newer => upgrade available.
        assert engine.upgrade_available is True

        # Test DAIEngineVersion is correctly persisted in kubeDAIEngine Spec.
        kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        img = "353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest"
        assert kube_eng["spec"]["image"] == img
        assert kube_eng["spec"]["imagePullPolicy"] == "IfNotPresent"
        assert kube_eng["spec"]["imagePullSecrets"] == [{"name": "regcred"}]
        assert kube_eng["spec"]["daiEngineVersion"] == dai_engine_version_v1_11_1.name

        # Test GetDAIEngine
        engine_get = dai_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
        assert engine_get.name == f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        assert engine_get.dai_engine_version == dai_engine_version_v1_11_1.name
        assert_version_equal_version_info(version=dai_engine_version_v1_11_1,
                                          version_info=engine_get.dai_engine_version_info)
        assert engine_get.upgrade_available is True

        # Test ListDAIEngines
        engines = dai_client.list_all_engines(workspace_id=workspace_id)
        assert len(engines) == 1
        assert engines[0].name == f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        assert engines[0].dai_engine_version == dai_engine_version_v1_11_1.name
        assert_version_equal_version_info(
            version=dai_engine_version_v1_11_1,
            version_info=engines[0].dai_engine_version_info,
        )
        assert engines[0].upgrade_available is True

        engine.pause()
        engine.wait()

        # Update assigned daiEngineVersion
        dai_engine_version_v1_11_1.image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS
        dai_engine_version_v1_11_1.image_pull_secrets = ["regcred", "regcred2"]
        updated_v1 = dai_engine_version_client_super_admin.update_dai_engine_version(
            dai_engine_version=dai_engine_version_v1_11_1
        )

        orig_version_info = engine.dai_engine_version_info

        # Resume engine with DAIEngineVersion that was recently updated.
        engine.resume()

        # Check that DAIEngine has correctly updated its DAIEngineVersion fields.
        assert engine.name == f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        assert engine.dai_engine_version == dai_engine_version_v1_11_1.name
        assert_version_equal_version_info(version=updated_v1, version_info=engine.dai_engine_version_info)
        assert engine.upgrade_available is True
        # Explicitly check that versionInfo has changed correctly when compared to the last one.
        assert orig_version_info.create_time == engine.dai_engine_version_info.create_time
        assert orig_version_info.update_time != engine.dai_engine_version_info.update_time
        # Check kubeDAIEngine persisted fields.
        kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        img = "353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest"
        assert kube_eng["spec"]["image"] == img
        assert kube_eng["spec"]["imagePullPolicy"] == "Always"
        assert kube_eng["spec"]["imagePullSecrets"] == [{"name": "regcred"}, {"name": "regcred2"}]
        assert kube_eng["spec"]["daiEngineVersion"] == dai_engine_version_v1_11_1.name

        # Test UpgradeDAIEngineVersion validation.
        with pytest.raises(CustomApiException) as exc:
            engine.upgrade_dai_engine_version(new_dai_engine_version=dai_engine_version_v2_0_0.name)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'engine must be paused or failed' in json.loads(exc.value.body)["message"]

        engine.pause()
        engine.wait()

        # Test UpgradeDAIEngineVersion validation.
        with pytest.raises(CustomApiException) as exc:
            engine.upgrade_dai_engine_version(new_dai_engine_version=dai_engine_version_v1_11_0.name)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert f'new version (1.11.0) must be greater than or equal to the current version (1.11.1)' \
               in json.loads(exc.value.body)["message"]

        # Test UpgradeDAIEngineVersion validation.
        with pytest.raises(CustomApiException) as exc:
            engine.upgrade_dai_engine_version(new_dai_engine_version="workspaces/global/daiEngineVersions/non-existing")
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert f'DAIEngineVersion "workspaces/global/daiEngineVersions/non-existing" not found' \
               in json.loads(exc.value.body)["message"]

        # Test UpgradeDAIEngineVersion validation.
        with pytest.raises(CustomApiException) as exc:
            engine.upgrade_dai_engine_version(new_dai_engine_version=dai_engine_version_v1_11_2.name)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert f'DAIEngineVersion "{dai_engine_version_v1_11_2.name}" is deprecated' \
               in json.loads(exc.value.body)["message"]

        # Test UpgradeDAIEngineVersion validation (using alias).
        with pytest.raises(CustomApiException) as exc:
            engine.upgrade_dai_engine_version(
                new_dai_engine_version="workspaces/global/daiEngineVersions/v2-deprecated"
            )
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert f'DAIEngineVersion "{dai_engine_version_v1_11_2.name}" is deprecated' \
               in json.loads(exc.value.body)["message"]

        # Test UpgradeDAIEngineVersion validation.
        with pytest.raises(CustomApiException) as exc:
            engine.upgrade_dai_engine_version(
                new_dai_engine_version=dai_engine_version_v1_11_3.name,
            )
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert (f'prohibited new version (1.11.3): '
                f'cannot upgrade to version that is greater than or equal 1.11.1 and less than 2.0.0'
                ) in json.loads(exc.value.body)["message"]

        # Test UpgradeDAIEngineVersion completed (successful, finally)
        engine.upgrade_dai_engine_version(new_dai_engine_version=dai_engine_version_v2_0_0.name)
        assert engine.dai_engine_version == dai_engine_version_v2_0_0.name
        # VersionInfo should is not changed!
        assert engine.dai_engine_version_info.name != dai_engine_version_v2_0_0.name

        # TODO we cannot reliably check that 'upgrade_available is False' because other tests
        # are running concurrently and they may be creating newer versions (it's not properly isolated).
        # assert engine.upgrade_available is False

        # Check kubeDAIEngine Spec persisted fields (upgrade method rewrites only daiEngineVersion field, other fields
        # remain unchanged until Resume).
        kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        img = "353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest"
        assert kube_eng["spec"]["image"] == img
        assert kube_eng["spec"]["imagePullPolicy"] == "Always"
        assert kube_eng["spec"]["imagePullSecrets"] == [{"name": "regcred"}, {"name": "regcred2"}]
        assert kube_eng["spec"]["daiEngineVersion"] == dai_engine_version_v2_0_0.name

        # Test Resume with the upgraded version.
        engine.resume()
        assert engine.dai_engine_version == dai_engine_version_v2_0_0.name
        # VersionInfo should be updated now.
        assert_version_equal_version_info(
            version=dai_engine_version_v2_0_0,
            version_info=engine.dai_engine_version_info,
        )

        # TODO we cannot reliably check that 'upgrade_available is False' because other tests
        # are running concurrently and they may be creating newer versions (it's not properly isolated).
        # assert engine.upgrade_available is False

        # Check kubeDAIEngine Spec persisted fields. Image, ImagePullPolicy and ImagePullSecrets should be updated.
        kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        img = "353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest"
        assert kube_eng["spec"]["image"] == img
        assert kube_eng["spec"]["imagePullPolicy"] == "IfNotPresent"
        assert kube_eng["spec"]["imagePullSecrets"] == [{"name": "regcred"}]
        assert kube_eng["spec"]["daiEngineVersion"] == dai_engine_version_v2_0_0.name
    finally:
        dai_admin_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}", allow_missing=True
        )


def assert_version_equal_version_info(version: DAIEngineVersion, version_info: DAIEngineVersionInfo):
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
