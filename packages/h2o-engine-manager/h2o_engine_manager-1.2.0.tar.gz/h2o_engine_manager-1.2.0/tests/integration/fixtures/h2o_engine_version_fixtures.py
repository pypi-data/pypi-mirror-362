import http

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.h2o_engine_version.version import H2OEngineVersion


@pytest.fixture(scope="function")
def h2o_engine_version_v0_0_0_1(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
            aliases=["mock"]
        ),
        h2o_engine_version_id="0.0.0.1",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v3_36_1_5(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="3.36.1.5",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v3_38_0_4(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="3.38.0.4",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v3_40_0_3(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="3.40.0.3",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v0_0_0_2(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="0.0.0.2",
    )
    name = created_version.name

    yield created_version

    # Version should be deleted during its usage in test case.
    # Check that version no longer exists.
    try:
        h2o_engine_version_client_super_admin.get_h2o_engine_version(name=name)
    except CustomApiException as exc:
        if exc.status == http.HTTPStatus.NOT_FOUND:
            return
        else:
            # Unexpected exception, re-raise.
            raise

    # In case version was found (test failed before it was deleted), delete it.
    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v1(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="1",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v2(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="2",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v3(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="3",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v4(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="4",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v5(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="5",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v6(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="6",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)


@pytest.fixture(scope="function")
def h2o_engine_version_v7(h2o_engine_version_client_super_admin):
    created_version = h2o_engine_version_client_super_admin.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockh2o:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        h2o_engine_version_id="7",
    )
    name = created_version.name

    yield created_version

    h2o_engine_version_client_super_admin.delete_h2o_engine_version(name=name)
