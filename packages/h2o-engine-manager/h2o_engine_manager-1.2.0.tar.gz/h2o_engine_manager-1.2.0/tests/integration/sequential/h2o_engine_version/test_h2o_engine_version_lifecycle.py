from typing import List

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.h2o_engine_version.h2o_engine_version_config import (
    H2OEngineVersionConfig,
)
from h2o_engine_manager.clients.h2o_engine_version.version import H2OEngineVersion


def test_h2o_engine_version_lifecycle(
    h2o_engine_version_client_super_admin,
    delete_all_h2o_engine_versions_before_after,
):
    """
    Basic functionality walkthrough.
    """
    client = h2o_engine_version_client_super_admin

    client.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="img1",
            aliases=["foo"],
        ),
        h2o_engine_version_id="3.36.1.5",
    )
    client.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="img2",
            aliases=["bar"],
        ),
        h2o_engine_version_id="3.38.0.4",
    )
    client.create_h2o_engine_version(
        parent="workspaces/global",
        h2o_engine_version=H2OEngineVersion(
            image="img3",
            aliases=["latest"],
        ),
        h2o_engine_version_id="3.40.0.4",
    )

    latest_version = client.get_h2o_engine_version(name="workspaces/global/h2oEngineVersions/latest")
    assert latest_version.name == "workspaces/global/h2oEngineVersions/3.40.0.4"
    assert latest_version.deprecated is False
    assert latest_version.image == "img3"
    assert latest_version.aliases == ["latest"]
    assert latest_version.image_pull_policy == ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT
    assert latest_version.image_pull_secrets == []
    assert latest_version.create_time is not None
    assert latest_version.update_time is None
    assert latest_version.creator != ""
    assert latest_version.updater == ""
    assert latest_version.creator_display_name != ""
    assert latest_version.updater_display_name == ""

    versions = client.list_all_h2o_engine_versions(parent="workspaces/global")
    assert len(versions) == 3
    assert versions[0].name == "workspaces/global/h2oEngineVersions/3.40.0.4"
    assert versions[1].name == "workspaces/global/h2oEngineVersions/3.38.0.4"
    assert versions[2].name == "workspaces/global/h2oEngineVersions/3.36.1.5"

    page1 = client.list_h2o_engine_versions(parent="workspaces/global", page_size=1)
    assert len(page1.h2o_engine_versions) == 1
    assert page1.h2o_engine_versions[0].name == "workspaces/global/h2oEngineVersions/3.40.0.4"
    assert page1.next_page_token != ""

    client.delete_h2o_engine_version(name="workspaces/global/h2oEngineVersions/3.38.0.4")

    page2 = client.list_h2o_engine_versions(
        parent="workspaces/global",
        page_size=2,
        page_token=page1.next_page_token
    )
    assert len(page2.h2o_engine_versions) == 1
    assert page2.h2o_engine_versions[0].name == "workspaces/global/h2oEngineVersions/3.36.1.5"
    assert page2.next_page_token == ""

    v1 = client.get_h2o_engine_version(name="workspaces/global/h2oEngineVersions/3.36.1.5")
    v1.deprecated = True
    v1.image = "updated_img1"
    v1.image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_NEVER
    v1.image_pull_secrets = ["secret1", "secret2"]
    updated_v1 = client.update_h2o_engine_version(h2o_engine_version=v1)
    assert updated_v1.name == "workspaces/global/h2oEngineVersions/3.36.1.5"
    assert updated_v1.deprecated is True
    assert updated_v1.image == "updated_img1"
    assert updated_v1.aliases == ["foo"]
    assert updated_v1.image_pull_policy == ImagePullPolicy.IMAGE_PULL_POLICY_NEVER
    assert updated_v1.image_pull_secrets == ["secret1", "secret2"]
    assert updated_v1.create_time is not None
    assert updated_v1.update_time is not None
    assert updated_v1.creator != ""
    assert updated_v1.updater != ""
    assert updated_v1.creator_display_name != ""
    assert updated_v1.updater_display_name != ""

    all_versions = client.assign_h2o_engine_version_aliases(
        name="workspaces/global/h2oEngineVersions/3.40.0.4",
        aliases=["latest", "foo", "bam"]
    )
    assert len(all_versions) == 2
    assert all_versions[0].name == "workspaces/global/h2oEngineVersions/3.40.0.4"
    assert all_versions[0].aliases == ["bam", "foo", "latest"]
    assert all_versions[1].name == "workspaces/global/h2oEngineVersions/3.36.1.5"
    assert all_versions[1].aliases == []

    configs: List[H2OEngineVersionConfig] = [
        H2OEngineVersionConfig(h2o_engine_version_id="3.1.11.4", image="img3.1.11.4", aliases=["foo"]),
        H2OEngineVersionConfig(h2o_engine_version_id="3.1.11.4.1", image="img3.1.11.4.1", aliases=["bam"]),
        H2OEngineVersionConfig(h2o_engine_version_id="3.1.11.10", image="img3.1.11.10", aliases=["baz"]),
    ]
    client.apply_h2o_engine_version_configs(configs=configs)
    all_versions = client.list_all_h2o_engine_versions(parent="workspaces/global")
    assert len(all_versions) == 3
    assert all_versions[0].name == "workspaces/global/h2oEngineVersions/3.1.11.10"
    assert all_versions[1].name == "workspaces/global/h2oEngineVersions/3.1.11.4.1"
    assert all_versions[2].name == "workspaces/global/h2oEngineVersions/3.1.11.4"
