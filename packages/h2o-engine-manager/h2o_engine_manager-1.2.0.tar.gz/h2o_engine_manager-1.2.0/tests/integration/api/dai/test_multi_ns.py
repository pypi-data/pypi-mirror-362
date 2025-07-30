from kubernetes import client

from tests.integration.conftest import AIEM_WORKSPACE_2_ID
from tests.integration.conftest import AIEM_WORKSPACE_2_NAMESPACE
from tests.integration.conftest import GLOBAL_WORKSPACE_ID
from tests.integration.conftest import GLOBAL_WORKSPACE_NAMESPACE


def test_create_dai_global_workspace(dai_client, delete_all_dais_before_after):
    # Use workspace that does not have any namespace assigned
    workspace_id = "3a991d92-b792-4094-8a34-dd975c8fde87"
    e = dai_client.create_engine(
        workspace_id=workspace_id,
    )

    # Verify default namespace is resolved from the global workspace
    get_dai_crd(namespace=GLOBAL_WORKSPACE_NAMESPACE, workspace_id=workspace_id, engine_id=e.engine_id)

def test_create_multiple_namespaces(dai_client, delete_all_dais_before_after):
    # When
    e1_id = "engine1"
    dai_client.create_engine(
        engine_id=e1_id,
        workspace_id=GLOBAL_WORKSPACE_ID,
    )
    e2_id = "engine2"
    dai_client.create_engine(
        engine_id=e2_id,
        workspace_id=AIEM_WORKSPACE_2_ID,
    )

    # Then both CRDs exists in a different namespaces
    get_dai_crd(namespace=GLOBAL_WORKSPACE_NAMESPACE, workspace_id=GLOBAL_WORKSPACE_ID, engine_id=e1_id)
    get_dai_crd(namespace=AIEM_WORKSPACE_2_NAMESPACE, workspace_id=AIEM_WORKSPACE_2_ID, engine_id=e2_id)


def test_lifecycle(dai_client, delete_all_dais_before_after):
    # When
    e = dai_client.create_engine(
        workspace_id=AIEM_WORKSPACE_2_ID,
    )

    # Then - can GET
    e = dai_client.get_engine(engine_id=e.engine_id, workspace_id=e.workspace_id)

    # Then - can LIST
    list = dai_client.list_all_engines(workspace_id=e.workspace_id)
    assert len(list) == 1

    # Then - can PAUSE
    e.pause()

    # Then - can DELETE
    e.delete()


def get_dai_crd(namespace: str, workspace_id: str, engine_id: str):
    # Kubernetes client is already setup in conftest.py, can be used here out-of-the-box.
    # Whitebox testing - we know how to fetch the DriverlessAI k8s object directly from cluster.
    return client.CustomObjectsApi().get_namespaced_custom_object(
        group="engine.h2o.ai",
        version="v1",
        namespace=namespace,
        plural="driverlessais",
        name=f"{workspace_id}.{engine_id}",
    )

