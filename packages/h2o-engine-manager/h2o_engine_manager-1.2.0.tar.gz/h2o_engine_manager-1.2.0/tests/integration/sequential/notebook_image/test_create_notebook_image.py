import http
import re
import time

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.constraint.profile_constraint_duration import (
    ProfileConstraintDuration,
)
from h2o_engine_manager.clients.constraint.profile_constraint_numeric import (
    ProfileConstraintNumeric,
)
from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine_image.image import NotebookEngineImage
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_create_notebook_engine_image(
    notebook_engine_image_client_super_admin,
    notebook_engine_image_client,
    delete_all_notebook_engine_images_before_after,
):
    to_create = NotebookEngineImage(
        image = "my-image",
        display_name = "display my image",
        enabled = True,
        image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS,
        image_pull_secrets = ["secret1", "secret2"],
    )
    to_create_id = "i1"
    now_before = time.time()

    # regular user cannot create profile
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_image_client.create_notebook_engine_image(
            parent=GLOBAL_WORKSPACE,
            notebook_engine_image=to_create,
            notebook_engine_image_id=to_create_id,
        )
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # super-admin can create profile
    created: NotebookEngineImage = notebook_engine_image_client_super_admin.create_notebook_engine_image(
        parent=GLOBAL_WORKSPACE,
        notebook_engine_image=to_create,
        notebook_engine_image_id=to_create_id,
    )

    assert created.name == "workspaces/global/notebookEngineImages/i1"
    assert created.display_name == "display my image"
    assert created.enabled is True
    assert created.image_pull_policy == ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS
    assert created.image_pull_secrets == ["secret1", "secret2"]
    now_after = time.time()
    assert now_before <= created.create_time.timestamp() <= now_after
    assert created.update_time is None
    assert re.match(r"^users/.+$", created.creator)
    assert created.updater == ""
    assert created.creator_display_name == "test-super-admin"
    assert created.updater_display_name == ""

    # Already exists error
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_image_client_super_admin.create_notebook_engine_image(
            parent=GLOBAL_WORKSPACE,
            notebook_engine_image=to_create,
            notebook_engine_image_id=to_create_id,
        )
    assert exc.value.status == http.HTTPStatus.CONFLICT
