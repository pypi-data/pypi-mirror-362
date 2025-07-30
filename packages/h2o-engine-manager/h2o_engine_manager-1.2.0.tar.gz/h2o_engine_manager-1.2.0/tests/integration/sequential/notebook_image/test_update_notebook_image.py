import http
import re
import time

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine_image.image import NotebookEngineImage
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_update_notebook_engine_images(
    notebook_engine_image_client_super_admin,
    notebook_engine_image_client_admin,
    notebook_engine_image_client,
    delete_all_notebook_engine_images_before_after,
):
    created: NotebookEngineImage = notebook_engine_image_client_super_admin.create_notebook_engine_image(
        parent=GLOBAL_WORKSPACE,
        notebook_engine_image=(NotebookEngineImage(
            image = "my-image",
            display_name = "display original",
            enabled = True,
            image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS,
            image_pull_secrets = ["secret1", "secret2"],
        )),
        notebook_engine_image_id="i1",
    )

    creator = created.creator
    re.match(r"^users/.+$", creator)
    create_time = created.create_time
    now_before = time.time()

    created.creator = "whatever"
    created.image = "my-image-2"
    created.display_name = "updated display name"

    # Regular user cannot update.
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_image_client.update_notebook_engine_image(notebook_engine_image=created)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # Only super-admin can update.
    updated: NotebookEngineImage = notebook_engine_image_client_super_admin.update_notebook_engine_image(notebook_engine_image=created, update_mask="image")

    assert updated.name == "workspaces/global/notebookEngineImages/i1"
    assert updated.display_name == "display original"
    assert updated.enabled is True
    assert updated.image == "my-image-2"
    assert updated.create_time == create_time
    assert updated.create_time != updated.update_time
    now_after = time.time()
    assert now_before <= updated.update_time.timestamp() <= now_after
    assert updated.creator == creator
    assert updated.creator == updated.updater
    assert updated.creator_display_name == "test-super-admin"
    assert updated.updater_display_name == "test-super-admin"

    # Update with default mask
    updated: NotebookEngineImage = notebook_engine_image_client_super_admin.update_notebook_engine_image(notebook_engine_image=created)
    assert updated.display_name == "updated display name"
