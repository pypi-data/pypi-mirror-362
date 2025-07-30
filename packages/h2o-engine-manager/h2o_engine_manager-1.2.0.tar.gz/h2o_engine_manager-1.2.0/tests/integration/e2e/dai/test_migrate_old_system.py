import http
import json
import os

import pytest
from kubernetes import config

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.exception import FailedEngineException
from tests.integration.e2e.dai.test_dai_engine_profile_usage import (
    assert_profile_equal_profile_info,
)
from tests.integration.e2e.dai.test_dai_engine_version_usage import (
    assert_version_equal_version_info,
)
from tests.integration.e2e.dai.test_dai_resume import get_kube_dai


@pytest.mark.timeout(180)
def test_migrate_from_old_system_to_new_system(
    dai_client,
    dai_admin_client,
    dai_engine_profile_p9,
    dai_engine_version_v1_10_6_1,
    create_dai_engine_in_k8s,
):
    """
    Test migrating DAIEngine from old {DAISetup} to new {DAIEngineProfile}.
    """
    # White-box testing using k8s client.
    config.load_config()

    workspace_id = "80c41cc0-e269-4f32-a702-c0dd75484ff8"
    engine_id = "old-engine"
    namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

    try:
        engine = dai_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)

        try:
            engine.pause()
            engine.wait()
        except FailedEngineException:
            # Engine may end up in failed state (direct creation via k8s may cause that, it's not reliable)
            pass
        finally:
            # Engine should end up either in PAUSED or FAILED state.
            assert engine.state in [DAIEngineState.STATE_PAUSED, DAIEngineState.STATE_FAILED]

        # Set new DAIEngineProfile.
        engine.profile = dai_engine_profile_p9.name
        engine.update()
        assert engine.profile == dai_engine_profile_p9.name
        assert engine.profile_info is None

        # Check that after Resume everything is set as expected.
        engine.resume()
        assert engine.profile == dai_engine_profile_p9.name
        assert engine.profile_info is not None
        assert_profile_equal_profile_info(profile=dai_engine_profile_p9, profile_info=engine.profile_info)
        assert engine.dai_engine_version == dai_engine_version_v1_10_6_1.name
        assert engine.dai_engine_version_info is not None
        assert_version_equal_version_info(
            version=dai_engine_version_v1_10_6_1,
            version_info=engine.dai_engine_version_info
        )
        # Check kubeDAIEngine.
        kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        assert kube_eng["spec"]["profile"] == "workspaces/global/daiEngineProfiles/p9"
        img = "353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest"
        assert kube_eng["spec"]["image"] == img
        assert kube_eng["spec"]["imagePullPolicy"] == "IfNotPresent"
        assert kube_eng["spec"]["imagePullSecrets"] == [{"name": "regcred"}]

        # Check that engine gets into RUNNING state.
        engine.wait()
        assert engine.state == DAIEngineState.STATE_RUNNING

    finally:
        dai_admin_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}", allow_missing=True
        )
