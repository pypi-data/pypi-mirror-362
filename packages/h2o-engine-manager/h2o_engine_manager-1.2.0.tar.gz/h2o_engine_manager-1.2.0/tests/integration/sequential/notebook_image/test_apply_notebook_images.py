import http
import re
from typing import List

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine_image.image import NotebookEngineImage
from h2o_engine_manager.clients.notebook_engine_image.image_config import (
    NotebookEngineImageConfig,
)
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_apply_notebook_engine_images_super_admin(
    notebook_engine_image_client_super_admin,
    delete_all_notebook_engine_images_before_after,
):
    notebook_engine_image_client_super_admin.create_notebook_engine_image(
        parent=GLOBAL_WORKSPACE,
        notebook_engine_image=NotebookEngineImage(
            image = "my-image-1",
            display_name = "display my image",
            image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS,
        ),
        notebook_engine_image_id="img1",
    )
    notebook_engine_image_client_super_admin.create_notebook_engine_image(
        parent=GLOBAL_WORKSPACE,
        notebook_engine_image=NotebookEngineImage(
            image = "my-image-2",
            image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_NEVER,
        ),
        notebook_engine_image_id="img2",
    )
    profiles = notebook_engine_image_client_super_admin.list_all_notebook_engine_images(parent=GLOBAL_WORKSPACE)
    assert len(profiles) == 2
    assert profiles[0].name == "workspaces/global/notebookEngineImages/img2"
    assert profiles[1].name == "workspaces/global/notebookEngineImages/img1"
    assert profiles[1].display_name == "display my image"

    configs: List[NotebookEngineImageConfig] = [
        NotebookEngineImageConfig(
            notebook_engine_image_id="i1",
            image = "my-image-1",
            image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
        ),
        NotebookEngineImageConfig(
            notebook_engine_image_id="i2",
            image = "my-image-2",
            image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
        ),
        NotebookEngineImageConfig(
            notebook_engine_image_id="i3",
            image = "my-image-3",
            image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
        )
    ]

    # When applying NotebookEngineImage configs.
    applied_profiles: list[NotebookEngineImage] = notebook_engine_image_client_super_admin.apply_notebook_engine_image_configs(configs=configs)

    # Then only applied images exist with specified params.
    assert len(applied_profiles) == 3
    assert applied_profiles[0].name == "workspaces/global/notebookEngineImages/i3"
    assert applied_profiles[1].name == "workspaces/global/notebookEngineImages/i2"
    assert applied_profiles[2].name == "workspaces/global/notebookEngineImages/i1"
