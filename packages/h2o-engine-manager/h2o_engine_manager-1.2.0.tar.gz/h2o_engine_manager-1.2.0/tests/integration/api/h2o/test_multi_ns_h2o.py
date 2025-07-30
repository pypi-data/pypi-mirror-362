from kubernetes import client

from tests.integration.conftest import AIEM_WORKSPACE_2_ID
from tests.integration.conftest import AIEM_WORKSPACE_2_NAMESPACE
from tests.integration.conftest import GLOBAL_WORKSPACE_ID
from tests.integration.conftest import GLOBAL_WORKSPACE_NAMESPACE


def test_create_h2o_global_workspace(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    # Use workspace that does not have any namespace assigned
    workspace_id = "3a991d92-b792-4094-8a34-dd975c8fde87"
    e = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    # Verify default namespace is resolved from the global workspace
    get_h2o_crd(namespace=GLOBAL_WORKSPACE_NAMESPACE, workspace_id=workspace_id, engine_id=e.engine_id)


def test_create_multiple_namespaces(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    # When
    e1_id = "engine1"
    h2o_engine_client.create_engine(
        engine_id=e1_id,
        workspace_id=GLOBAL_WORKSPACE_ID,
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )
    e2_id = "engine2"
    h2o_engine_client.create_engine(
        engine_id=e2_id,
        workspace_id=AIEM_WORKSPACE_2_ID,
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    # Then both CRDs exists in a different namespaces
    get_h2o_crd(namespace=GLOBAL_WORKSPACE_NAMESPACE, workspace_id=GLOBAL_WORKSPACE_ID, engine_id=e1_id)
    get_h2o_crd(namespace=AIEM_WORKSPACE_2_NAMESPACE, workspace_id=AIEM_WORKSPACE_2_ID, engine_id=e2_id)


def test_lifecycle(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    # When
    e = h2o_engine_client.create_engine(
        workspace_id=AIEM_WORKSPACE_2_ID,
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    # Then - can GET
    e = h2o_engine_client.get_engine(engine_id=e.engine_id, workspace_id=e.workspace_id)

    # Then - can LIST
    list = h2o_engine_client.list_all_engines(workspace_id=e.workspace_id)
    assert len(list) == 1

    # Then - can TERMINATE
    e.terminate()

    # Then - can DELETE
    e.delete()


def get_h2o_crd(namespace: str, workspace_id: str, engine_id: str):
    # Kubernetes client is already setup in conftest.py, can be used here out-of-the-box.
    # Whitebox testing - we know how to fetch the H2O k8s object directly from cluster.
    return client.CustomObjectsApi().get_namespaced_custom_object(
        group="engine.h2o.ai",
        version="v1",
        namespace=namespace,
        plural="h2os",
        name=f"{workspace_id}.{engine_id}",
    )
