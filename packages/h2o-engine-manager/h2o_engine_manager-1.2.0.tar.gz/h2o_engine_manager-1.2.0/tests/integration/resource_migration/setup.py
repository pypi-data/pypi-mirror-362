import os

from kubernetes import config

from testing.kubectl import kubectl_apply
from testing.kubectl import kubectl_delete_resource_all

config.load_config()
workloads_namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

kubectl_delete_resource_all(resource="dai", namespace=workloads_namespace)
kubectl_apply(
    path=(os.path.join(os.path.dirname(__file__), "test_data", "dai")),
    namespace=workloads_namespace,
)
kubectl_delete_resource_all(resource="h2o", namespace=workloads_namespace)
kubectl_apply(
    path=(os.path.join(os.path.dirname(__file__), "test_data", "h2o")),
    namespace=workloads_namespace,
)
