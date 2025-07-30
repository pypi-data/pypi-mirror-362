import http

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.dai_engine_version.version import DAIEngineVersion
from h2o_engine_manager.clients.exception import CustomApiException


@pytest.fixture(scope="function")
def dai_engine_version_v1_10_4_1(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.10.4.1",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_10_4_9(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.10.4.9",
    )
    name = created_version.name

    yield created_version

    # Version should be deleted during its usage in test case.
    # Check that version no longer exists.
    try:
        dai_engine_version_client_super_admin.get_dai_engine_version(name=name)
    except CustomApiException as exc:
        if exc.status == http.HTTPStatus.NOT_FOUND:
            return
        else:
            # Unexpected exception, re-raise.
            raise

    # In case version was found (test failed before it was deleted), delete it.
    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_10_5(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.10.5",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_10_6_1(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.10.6.1",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_10_7_2(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-driverlessai-console:1.10.7.2-cuda11.2.2",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.10.7.2",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_0(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.0",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_1(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.1",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_2(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
            deprecated=True,
            aliases=["v2-deprecated"]
        ),
        dai_engine_version_id="1.11.2",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_3(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
            aliases=["latest"]
        ),
        dai_engine_version_id="1.11.3",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_4(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.4",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_5(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.5",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_6(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.6",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_7(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.7",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_8(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.8",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_9(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.9",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_10(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.10",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_11(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.11",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_12(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.12",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_13(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.13",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_14(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.14",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_15(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.15",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_16(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.16",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_17(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.17",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_18(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.18",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_19(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.19",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_20(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.20",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_21(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.21",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_22(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.22",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_23(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-driverlessai-console:1.10.7.2-cuda11.2.2",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.23",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_24(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.24",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_25(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.25",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v1_11_26(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="1.11.26",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v2_0_0(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="2.0.0",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v2_0_1(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="2.0.1",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)


@pytest.fixture(scope="function")
def dai_engine_version_v2_0_2(dai_engine_version_client_super_admin):
    created_version = dai_engine_version_client_super_admin.create_dai_engine_version(
        parent="workspaces/global",
        dai_engine_version=DAIEngineVersion(
            image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-enginemanager-mockdai:latest",
            image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
            image_pull_secrets=["regcred"],
        ),
        dai_engine_version_id="2.0.2",
    )
    name = created_version.name

    yield created_version

    dai_engine_version_client_super_admin.delete_dai_engine_version(name=name)