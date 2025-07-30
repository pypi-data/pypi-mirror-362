import http

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine_image.image import NotebookEngineImage
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_delete_notebook_engine_images(
    notebook_engine_image_client_super_admin,
    notebook_engine_image_client,
    delete_all_notebook_engine_images_before_after,
):
    created = notebook_engine_image_client_super_admin.create_notebook_engine_image(
        parent=GLOBAL_WORKSPACE,
        notebook_engine_image=(NotebookEngineImage(
            image = "my-image",
            display_name = "display my image",
            enabled = True,
            image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS,
            image_pull_secrets = ["secret1", "secret2"],
        )),
        notebook_engine_image_id="i1",
    )

    # Regular user cannot delete.
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_image_client.delete_notebook_engine_image(name=created.name)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # Only super-admin can delete.
    notebook_engine_image_client_super_admin.delete_notebook_engine_image(name=created.name)

    # Check that profile no longer exists.
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_image_client_super_admin.get_notebook_engine_image(name=created.name)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
