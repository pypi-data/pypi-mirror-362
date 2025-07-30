import http
import re

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine_image.image import NotebookEngineImage
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_list_notebook_engine_images(
    notebook_engine_image_client_super_admin,
    notebook_engine_image_client_admin,
    notebook_engine_image_client,
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
    notebook_engine_image_client_super_admin.create_notebook_engine_image(
        parent=GLOBAL_WORKSPACE,
        notebook_engine_image=NotebookEngineImage(
            image = "my-image-3",
            image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT,
        ),
        notebook_engine_image_id="img3",
    )

    profiles: list[NotebookEngineImage] = notebook_engine_image_client.list_all_notebook_engine_images(parent=GLOBAL_WORKSPACE)
    assert len(profiles) == 3
    assert profiles[0].name == "workspaces/global/notebookEngineImages/img3"
    assert profiles[1].name == "workspaces/global/notebookEngineImages/img2"
    assert profiles[2].name == "workspaces/global/notebookEngineImages/img1"

    # test pagination
    page = notebook_engine_image_client_super_admin.list_notebook_engine_images(parent=GLOBAL_WORKSPACE, page_size=1)
    assert len(page.notebook_engine_images) == 1
    assert page.notebook_engine_images[0].name == "workspaces/global/notebookEngineImages/img3"
    assert page.next_page_token != ""

    page = notebook_engine_image_client_super_admin.list_notebook_engine_images(
        parent=GLOBAL_WORKSPACE,
        page_size=1,
        page_token=page.next_page_token
    )
    assert len(page.notebook_engine_images) == 1
    assert page.notebook_engine_images[0].name == "workspaces/global/notebookEngineImages/img2"
    assert page.next_page_token != ""

    page = notebook_engine_image_client_super_admin.list_notebook_engine_images(
        parent=GLOBAL_WORKSPACE,
        page_size=1,
        page_token=page.next_page_token
    )
    assert len(page.notebook_engine_images) == 1
    assert page.notebook_engine_images[0].name == "workspaces/global/notebookEngineImages/img1"
    assert page.next_page_token == ""
