import os

from kubernetes import config

from testing.kubectl import create_dai_license

config.load_config()
system_namespace = os.getenv("TEST_K8S_SYSTEM_NAMESPACE")

create_dai_license(namespace=system_namespace)
