import os
import time

import jwt

# Fixtures should be only in conftest.py, so they are automatically resolved during pytest.
# However, we want to have fixtures in multiple files (don't want to have one huge file)
# and still want them to be automatically resolved during pytest.
# Therefore, using ugly "import *" to include the extra fixtures in this conftest.py.
from fixtures.dai_engine_profile_fixtures import *
from fixtures.dai_engine_version_fixtures import *
from fixtures.h2o_engine_profile_fixtures import *
from fixtures.h2o_engine_version_fixtures import *
from fixtures.notebook_engine_image_fixtures import *
from fixtures.notebook_engine_profile_fixtures import *
from kubernetes import config

import h2o_engine_manager
from h2o_engine_manager.clients.engine.client import EngineClient
from testing.kubectl import kubectl_apply
from testing.kubectl import kubectl_delete_resource_all

# Kubernetes cache needs to take some time to detect changes in k8s server.
CACHE_SYNC_SECONDS = 0.2

# To have control over the provisioned test resources, a workspace with related DAISetup is used.
DAI_SETUP_WORKSPACE = "b4f21769-03f1-4ffe-aa88-39a165e9765c"
DAI_LIFECYCLE_WORKSPACE = "271b22c9-f4d8-4459-acd6-b0dbff849729"

H2O_SETUP_WORKSPACE = "1b04dfac-c0df-4022-91b7-23d1add51e1f"

GLOBAL_WORKSPACE_NAMESPACE = "aiem-workloads"
GLOBAL_WORKSPACE_ID = "global"
GLOBAL_WORKSPACE = f"workspaces/{GLOBAL_WORKSPACE_ID}"
AIEM_WORKSPACE_2_NAMESPACE = "aiem-workloads-2"
AIEM_WORKSPACE_2_ID = "57d851c8-d328-419e-a72f-747b7975f11e"


@pytest.fixture(scope="session")
def system_namespace():
    return os.getenv("TEST_K8S_SYSTEM_NAMESPACE")


@pytest.fixture(scope="session")
def workloads_namespace():
    return os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")


@pytest.fixture(scope="session")
def load_kube_config():
    config.load_config()


@pytest.fixture(scope="function")
def sync_cache():
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="function")
def create_default_dai_setup(load_kube_config, system_namespace):
    """Create DefaultDAISetup"""
    kubectl_apply(
        path=(os.path.join(os.path.dirname(__file__), "test_data", "dai_setups", "system.default.yaml")),
        namespace=system_namespace,
    )

    # Created default DAISetup is almost always used in tests via API
    # that uses cache. Wait a short while so the cache is synced in tests
    # to avoid race conditions.
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="function")
def create_dai_setup_workspace_dai_setup(load_kube_config, system_namespace):
    """Create DAISetup for workspace dai-setup"""
    kubectl_apply(
        path=(os.path.join(os.path.dirname(__file__), "test_data", "dai_setups", "dai-setup.yaml")),
        namespace=system_namespace,
    )

    # To avoid race conditions.
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="function")
def create_dai_setup_workspace_adjusted_dai_profiles(load_kube_config, system_namespace):
    """Create DAISetup for workspace adjusted-dai-profiles"""
    kubectl_apply(
        path=(os.path.join(os.path.dirname(__file__), "test_data", "dai_setups", "adjusted-dai-profiles.yaml")),
        namespace=system_namespace,
    )

    # To avoid race conditions.
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="function")
def delete_all_dai_setups_after(load_kube_config, system_namespace):
    """Delete all kube DAISetups after test."""
    yield

    kubectl_delete_resource_all(
        resource="daistp",
        namespace=system_namespace,
    )

    # To avoid race conditions.
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="function")
def create_default_h2o_setup(load_kube_config, system_namespace):
    """Create DefaultH2OSetup"""
    kubectl_apply(
        path=(os.path.join(os.path.dirname(__file__), "test_data", "h2o_setups", "system.default.yaml")),
        namespace=system_namespace,
    )

    # To avoid race conditions.
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="function")
def create_h2o_setup_workspace_h2o_setup(load_kube_config, system_namespace):
    """Create DAISetup for workspace dai-setup"""
    kubectl_apply(
        path=(os.path.join(os.path.dirname(__file__), "test_data", "h2o_setups", "h2o-setup.yaml")),
        namespace=system_namespace,
    )

    # To avoid race conditions.
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="function")
def delete_all_h2o_setups_after(load_kube_config, system_namespace):
    """Delete all kube H2OSetups after test."""
    yield

    delete_all_h2o_setups(system_namespace=system_namespace)


@pytest.fixture(scope="function")
def delete_all_h2o_setups_before_after(load_kube_config, system_namespace):
    delete_all_h2o_setups(system_namespace=system_namespace)
    yield
    delete_all_h2o_setups(system_namespace=system_namespace)


def delete_all_h2o_setups(system_namespace: str):
    """Delete all kube H2OSetups."""
    kubectl_delete_resource_all(
        resource="h2ostp",
        namespace=system_namespace,
    )

    # To avoid race conditions.
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="function")
def delete_all_dais_before_after(load_kube_config):
    """Delete all kube DAIs before and after test."""
    kubectl_delete_resource_all(
        resource="dai",
        namespace=GLOBAL_WORKSPACE_NAMESPACE,
    )
    kubectl_delete_resource_all(
        resource="dai",
        namespace=AIEM_WORKSPACE_2_NAMESPACE,
    )
    time.sleep(CACHE_SYNC_SECONDS)

    yield

    kubectl_delete_resource_all(
        resource="dai",
        namespace=GLOBAL_WORKSPACE_NAMESPACE,
    )
    kubectl_delete_resource_all(
        resource="dai",
        namespace=AIEM_WORKSPACE_2_NAMESPACE,
    )
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="function")
def delete_all_h2os_before_after(load_kube_config):
    """Delete all kube H2Os before and after test."""
    kubectl_delete_resource_all(
        resource="h2o",
        namespace=GLOBAL_WORKSPACE_NAMESPACE,
    )
    kubectl_delete_resource_all(
        resource="h2o",
        namespace=AIEM_WORKSPACE_2_NAMESPACE,
    )
    time.sleep(CACHE_SYNC_SECONDS)

    yield

    kubectl_delete_resource_all(
        resource="h2o",
        namespace=GLOBAL_WORKSPACE_NAMESPACE,
    )
    kubectl_delete_resource_all(
        resource="h2o",
        namespace=AIEM_WORKSPACE_2_NAMESPACE,
    )
    time.sleep(CACHE_SYNC_SECONDS)


@pytest.fixture(scope="session")
def clients():
    return h2o_engine_manager.login_custom(
        endpoint=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def admin_clients():
    return h2o_engine_manager.login_custom(
        endpoint=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        refresh_token=os.getenv("PLATFORM_TOKEN_ADMIN"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def super_admin_clients():
    return h2o_engine_manager.login_custom(
        endpoint=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        refresh_token=os.getenv("PLATFORM_TOKEN_SUPER_ADMIN"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )

@pytest.fixture(scope="session")
def deny_user_clients():
    return h2o_engine_manager.login_custom(
        endpoint=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        refresh_token=os.getenv("PLATFORM_TOKEN_DENY_USER"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def dai_client(clients):
    return clients.dai_engine_client


@pytest.fixture(scope="session")
def dai_admin_client(admin_clients):
    return admin_clients.dai_engine_client


@pytest.fixture(scope="session")
def dai_super_admin_client(super_admin_clients):
    return super_admin_clients.dai_engine_client


@pytest.fixture(scope="session")
def h2o_engine_client(clients):
    return clients.h2o_engine_client


@pytest.fixture(scope="session")
def h2o_engine_admin_client(admin_clients):
    return admin_clients.h2o_engine_client


@pytest.fixture(scope="session")
def engine_client():
    return EngineClient(
        url=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        platform_token=os.getenv("PLATFORM_TOKEN_USER"),
        platform_oidc_url=os.getenv("PLATFORM_OIDC_URL"),
        platform_oidc_client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )

@pytest.fixture(scope="session")
def engine_client_super_admin():
    return EngineClient(
        url=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        platform_token=os.getenv("PLATFORM_TOKEN_SUPER_ADMIN"),
        platform_oidc_url=os.getenv("PLATFORM_OIDC_URL"),
        platform_oidc_client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )

@pytest.fixture(scope="session")
def engine_client_deny_user():
    return EngineClient(
        url=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        platform_token=os.getenv("PLATFORM_TOKEN_DENY_USER"),
        platform_oidc_url=os.getenv("PLATFORM_OIDC_URL"),
        platform_oidc_client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )

@pytest.fixture(scope="session")
def dai_engine_profile_client_super_admin(super_admin_clients):
    return super_admin_clients.dai_engine_profile_client


@pytest.fixture(scope="session")
def dai_engine_profile_client_admin(admin_clients):
    return admin_clients.dai_engine_profile_client


@pytest.fixture(scope="session")
def dai_engine_profile_client(clients):
    return clients.dai_engine_profile_client


@pytest.fixture(scope="function")
def delete_all_dai_engine_profiles_before_after(dai_engine_profile_client_super_admin):
    profiles = dai_engine_profile_client_super_admin.list_all_dai_engine_profiles(parent=GLOBAL_WORKSPACE)
    for p in profiles:
        dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=p.name)

    yield

    profiles = dai_engine_profile_client_super_admin.list_all_dai_engine_profiles(parent=GLOBAL_WORKSPACE)
    for p in profiles:
        dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=p.name)


@pytest.fixture(scope="session")
def h2o_engine_profile_client_super_admin(super_admin_clients):
    return super_admin_clients.h2o_engine_profile_client


@pytest.fixture(scope="session")
def h2o_engine_profile_client_admin(admin_clients):
    return admin_clients.h2o_engine_profile_client


@pytest.fixture(scope="session")
def h2o_engine_profile_client(clients):
    return clients.h2o_engine_profile_client


@pytest.fixture(scope="function")
def delete_all_h2o_engine_profiles_before_after(h2o_engine_profile_client_super_admin):
    profiles = h2o_engine_profile_client_super_admin.list_all_h2o_engine_profiles(parent=GLOBAL_WORKSPACE)
    for p in profiles:
        h2o_engine_profile_client_super_admin.delete_h2o_engine_profile(name=p.name)

    yield

    profiles = h2o_engine_profile_client_super_admin.list_all_h2o_engine_profiles(parent=GLOBAL_WORKSPACE)
    for p in profiles:
        h2o_engine_profile_client_super_admin.delete_h2o_engine_profile(name=p.name)


@pytest.fixture(scope="session")
def notebook_engine_profile_client_super_admin(super_admin_clients):
    return super_admin_clients.notebook_engine_profile_client


@pytest.fixture(scope="session")
def notebook_engine_profile_client_admin(admin_clients):
    return admin_clients.notebook_engine_profile_client


@pytest.fixture(scope="session")
def notebook_engine_profile_client(clients):
    return clients.notebook_engine_profile_client


@pytest.fixture(scope="function")
def delete_all_notebook_engine_profiles_before_after(notebook_engine_profile_client_super_admin):
    profiles = notebook_engine_profile_client_super_admin.list_all_notebook_engine_profiles(parent=GLOBAL_WORKSPACE)
    for p in profiles:
        notebook_engine_profile_client_super_admin.delete_notebook_engine_profile(name=p.name)

    yield

    profiles = notebook_engine_profile_client_super_admin.list_all_notebook_engine_profiles(parent=GLOBAL_WORKSPACE)
    for p in profiles:
        notebook_engine_profile_client_super_admin.delete_notebook_engine_profile(name=p.name)


@pytest.fixture(scope="session")
def notebook_engine_image_client_super_admin(super_admin_clients):
    return super_admin_clients.notebook_engine_image_client


@pytest.fixture(scope="session")
def notebook_engine_image_client_admin(admin_clients):
    return admin_clients.notebook_engine_image_client


@pytest.fixture(scope="session")
def notebook_engine_image_client(clients):
    return clients.notebook_engine_image_client


@pytest.fixture(scope="function")
def delete_all_notebook_engine_images_before_after(notebook_engine_image_client_super_admin):
    profiles = notebook_engine_image_client_super_admin.list_all_notebook_engine_images(parent=GLOBAL_WORKSPACE)
    for p in profiles:
        notebook_engine_image_client_super_admin.delete_notebook_engine_image(name=p.name)

    yield

    profiles = notebook_engine_image_client_super_admin.list_all_notebook_engine_images(parent=GLOBAL_WORKSPACE)
    for p in profiles:
        notebook_engine_image_client_super_admin.delete_notebook_engine_image(name=p.name)


@pytest.fixture(scope="session")
def notebook_engine_client(clients):
    return clients.notebook_engine_client


@pytest.fixture(scope="session")
def notebook_engine_client_super_admin(super_admin_clients):
    return super_admin_clients.notebook_engine_client

@pytest.fixture(scope="function")
def dai_profile_cleanup_after(dai_profile_client):
    yield

    time.sleep(CACHE_SYNC_SECONDS)
    profiles = dai_profile_client.list_all_profiles()
    for p in profiles:
        dai_profile_client.delete_profile(profile_id=p.dai_profile_id)


@pytest.fixture(scope="session")
def websocket_base_url() -> str:
    scheme = os.getenv("AIEM_SCHEME")
    host = os.getenv("AIEM_HOST")

    if scheme == "http":
        return f"ws://{host}"
    elif scheme == "https":
        return f"wss://{host}"

    raise ValueError(f"AIEM_SCHEME must be either http or https, got scheme: {scheme}")


@pytest.fixture(scope="function")
def dai_profile(dai_profile_client):
    dai_profile = dai_profile_client.create_profile(
        profile_id="profile1",
        cpu=1,
        gpu=0,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        display_name="Smokerinho",
    )
    dai_profile_id = dai_profile.dai_profile_id

    time.sleep(CACHE_SYNC_SECONDS)

    yield dai_profile

    dai_profile_client.delete_profile(profile_id=dai_profile_id)


@pytest.fixture(scope="session")
def valid_ca_bundle(tmp_path_factory):
    cert = """
-----BEGIN CERTIFICATE-----
MIIB+jCCAWMCAgGjMA0GCSqGSIb3DQEBBAUAMEUxCzAJBgNVBAYTAlVTMRgwFgYD
VQQKEw9HVEUgQ29ycG9yYXRpb24xHDAaBgNVBAMTE0dURSBDeWJlclRydXN0IFJv
b3QwHhcNOTYwMjIzMjMwMTAwWhcNMDYwMjIzMjM1OTAwWjBFMQswCQYDVQQGEwJV
UzEYMBYGA1UEChMPR1RFIENvcnBvcmF0aW9uMRwwGgYDVQQDExNHVEUgQ3liZXJU
cnVzdCBSb290MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC45k+625h8cXyv
RLfTD0bZZOWTwUKOx7pJjTUteueLveUFMVnGsS8KDPufpz+iCWaEVh43KRuH6X4M
ypqfpX/1FZSj1aJGgthoTNE3FQZor734sLPwKfWVWgkWYXcKIiXUT0Wqx73llt/5
1KiOQswkwB6RJ0q1bQaAYznEol44AwIDAQABMA0GCSqGSIb3DQEBBAUAA4GBABKz
dcZfHeFhVYAA1IFLezEPI2PnPfMD+fQ2qLvZ46WXTeorKeDWanOB5sCJo9Px4KWl
IjeaY8JIILTbcuPI9tl8vrGvU9oUtCG41tWW4/5ODFlitppK+ULdjG+BqXH/9Apy
bW1EDp3zdHSo1TRJ6V6e6bR64eVaH4QwnNOfpSXY
-----END CERTIFICATE-----
    """
    fn = tmp_path_factory.mktemp("data") / "valid-cert.crt"
    fn.write_text(cert)
    return fn


@pytest.fixture(scope="session")
def invalid_ca_bundle(tmp_path_factory):
    cert = """
-----BEGIN CERTIFICATE-----
MIICjzCCAfigAwIBAgIJAJ5g4w0PvT34MA0GCSqGSIb3DQEBCwUAMBwxGjAYBgNV
BAMMEVRlc3QgSW52YWxpZCBDQTAeFw0yNDA3MjUxNzQ1NDFaFw0yNDA3MjQxNzQ1
NDFaMBwxGjAYBgNVBAMMEVRlc3QgSW52YWxpZCBDQTCBnzANBgkqhkiG9w0BAQEF
AAOBjQAwgYkCgYEA4mE6eq9mMNR5HDrFhjlmJ5aS+Z7QVVvF+32Lb+U5rP3m+vYP
5L8/X8IBT8MIv5gyA5/8X6ZgKJzkV7Zq4SWTlbnOx0Hp8T+lY43S+OErzZRxr12A
A0n97B2qdbbG5tbDt2dh1gnmKZDPbYk2pDh45fZryNabDwW9jxyXMO4pp6UCAwEA
AaM+MDwwDwYDVR0TBAgwBgEB/wIBADAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQW
BBTSt2RZ9DywA3YriGsoM0BxB8wM4TANBgkqhkiG9w0BAQsFAAOBgQBofPxtcI39
HqMNJxRgGfO23c8kF/8BYg0Khg0SPZBebgx+hNEKohZqOx+OjG/d+B5TZZy1djuy
dFRBBP7b5TZJx9FzVot0Y0CTN2trm8+Px9eZ4RpD+6RZID+bH5HeXRRB0seMPSOt
leQO3aZmR3kp1aVGcBf7W6dZ6hYlWROt5g==
-----END CERTIFICATE-----
    """
    fn = tmp_path_factory.mktemp("data") / "invalid-cert.crt"
    fn.write_text(cert)
    return fn


@pytest.fixture(scope="session")
def dai_engine_version_client_super_admin(super_admin_clients):
    return super_admin_clients.dai_engine_version_client


@pytest.fixture(scope="function")
def delete_all_dai_engine_versions_before_after(dai_engine_version_client_super_admin):
    dai_engine_version_client_super_admin.delete_all_dai_engine_versions(parent="workspaces/global")
    yield
    dai_engine_version_client_super_admin.delete_all_dai_engine_versions(parent="workspaces/global")


@pytest.fixture(scope="session")
def h2o_engine_version_client_super_admin(super_admin_clients):
    return super_admin_clients.h2o_engine_version_client


@pytest.fixture(scope="function")
def delete_all_h2o_engine_versions_before_after(h2o_engine_version_client_super_admin):
    h2o_engine_version_client_super_admin.delete_all_h2o_engine_versions(parent="workspaces/global")
    yield
    h2o_engine_version_client_super_admin.delete_all_h2o_engine_versions(parent="workspaces/global")


@pytest.fixture(scope="session")
def admin_user_name():
    token = os.getenv("PLATFORM_TOKEN_ADMIN")
    decoded = jwt.decode(jwt=token, options={"verify_signature": False})
    sub = decoded.get("sub")
    return f"users/{sub}"


@pytest.fixture(scope="session")
def regular_user_user_name():
    token = os.getenv("PLATFORM_TOKEN_USER")
    decoded = jwt.decode(jwt=token, options={"verify_signature": False})
    sub = decoded.get("sub")
    return f"users/{sub}"


@pytest.fixture(scope="function")
def create_dai_engine_in_k8s(load_kube_config, workloads_namespace):
    kubectl_apply(
        path=(os.path.join(os.path.dirname(__file__), "test_data", "dai", "dai_engine.yaml")),
        namespace=workloads_namespace,
    )
    time.sleep(CACHE_SYNC_SECONDS)
