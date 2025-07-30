import http
import json

import pytest

from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine.engine import NotebookEngine
from h2o_engine_manager.clients.notebook_engine.state import NotebookEngineState


@pytest.mark.timeout(180)
def test_notebook_engine_update(
    notebook_engine_client_super_admin,
    notebook_engine_image_client_super_admin,
    notebook_engine_profile_p3,
    notebook_engine_profile_p4,
    notebook_engine_image_i4,
    notebook_engine_image_i5,
):
    workspace_id = "f07263f2-9a5b-4274-886a-9d5f7a2f2e95"
    engine_id = "ntb-eng-update"

    # Update non-existing engine.
    with pytest.raises(CustomApiException) as exc:
        notebook_engine_client_super_admin.update_notebook_engine(
            notebook_engine=NotebookEngine(
                name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}",
                profile=notebook_engine_profile_p3.name,
                notebook_image=notebook_engine_image_i4.name,
            )
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND

    try:
        eng = notebook_engine_client_super_admin.create_notebook_engine(
            parent=f"workspaces/{workspace_id}",
            notebook_engine=NotebookEngine(
                profile=notebook_engine_profile_p3.name,
                notebook_image=notebook_engine_image_i4.name,
            ),
            notebook_engine_id=engine_id,
        )

        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'engine must be paused or failed' in json.loads(exc.value.body)["message"]

        notebook_engine_client_super_admin.pause_notebook_engine(name=eng.name)
        notebook_engine_client_super_admin.wait(name=eng.name)
        eng = notebook_engine_client_super_admin.get_notebook_engine(name=eng.name)
        assert eng.state in {NotebookEngineState.STATE_PAUSED, NotebookEngineState.STATE_FAILED}

        eng.cpu = 20
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: max constraint violated: cpu (20) must be <= 3' \
               in json.loads(exc.value.body)["message"]

        eng.cpu = 2
        eng.gpu = 20
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: max constraint violated: gpu (20) must be <= 3' \
               in json.loads(exc.value.body)["message"]

        eng.gpu = 1
        eng.memory_bytes = "3Gi"
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: max constraint violated: memory_bytes (3221225472) must be <= 2147483648' \
               in json.loads(exc.value.body)["message"]

        eng.memory_bytes = "40Mi"
        eng.max_idle_duration = "10h"
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: max_idle_duration (10h0m0s) must be <= 8h0m0s' \
               in json.loads(exc.value.body)["message"]

        eng.max_idle_duration = "5h"
        eng.max_running_duration = "10h"
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: max_running_duration (10h0m0s) must be <= 8h0m0s' \
               in json.loads(exc.value.body)["message"]

        eng.max_running_duration = "5h"
        eng.notebook_image = "foooo"
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: invalid notebook_image: rpc error: code = InvalidArgument desc = validation error: NotebookImage name "foooo" is invalid' \
               in json.loads(exc.value.body)["message"]

        eng.notebook_image = "workspaces/global/notebookEngineImages/non-existing"
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: invalid notebook_image: rpc error: code = InvalidArgument desc = notebookImage workspaces/global/notebookEngineImages/non-existing not found' \
               in json.loads(exc.value.body)["message"]

        # Delete currently assigned notebookEngineImage.
        notebook_engine_image_client_super_admin.delete_notebook_engine_image(
            name=notebook_engine_image_i4.name,
        )

        # Double-check image can no longer be found.
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_image_client_super_admin.get_notebook_engine_image(name=notebook_engine_image_i4.name)
        assert exc.value.status == http.HTTPStatus.NOT_FOUND

        # Update all.
        eng = notebook_engine_client_super_admin.get_notebook_engine(name=eng.name)
        eng.cpu = 2
        eng.gpu = 1
        eng.memory_bytes = "40Mi"
        eng.storage_bytes = "40Mi"
        eng.max_idle_duration = "5h"
        eng.max_running_duration = "5h"
        eng.display_name = "Some display name"
        eng.storage_class_name = "massive low taper fade"

        updated_eng = notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert updated_eng.cpu == 2
        assert updated_eng.gpu == 1
        assert updated_eng.memory_bytes == "40Mi"
        # Storage bytes change is ignored (storage cannot be changed via Update method).
        assert updated_eng.storage_bytes == "20Mi"
        assert updated_eng.max_idle_duration == "5h"
        assert updated_eng.max_running_duration == "5h"
        assert updated_eng.display_name == "Some display name"
        # Non-existing image has no effect on update because it has not changed in terms of engine-update.
        assert updated_eng.notebook_image == notebook_engine_image_i4.name
        # storageClassName always remains unchanged after creation (immutable).
        assert updated_eng.storage_class_name == "sc3"

        # Partial update
        eng = notebook_engine_client_super_admin.get_notebook_engine(name=eng.name)
        eng.cpu = 3
        eng.display_name = "Changed display name"
        eng.notebook_image = "whatever"

        updated_eng = notebook_engine_client_super_admin.update_notebook_engine(
            notebook_engine=eng,
            update_mask="cpu,display_name",
        )
        assert updated_eng.cpu == 3
        assert updated_eng.gpu == 1
        assert updated_eng.memory_bytes == "40Mi"
        assert updated_eng.storage_bytes == "20Mi"
        assert updated_eng.max_idle_duration == "5h"
        assert updated_eng.max_running_duration == "5h"
        assert updated_eng.display_name == "Changed display name"
        assert updated_eng.notebook_image == notebook_engine_image_i4.name

        # Update image to existing one.
        eng = notebook_engine_client_super_admin.get_notebook_engine(name=eng.name)
        eng.notebook_image = notebook_engine_image_i5.name
        updated_eng = notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert updated_eng.cpu == 3
        assert updated_eng.gpu == 1
        assert updated_eng.memory_bytes == "40Mi"
        assert updated_eng.storage_bytes == "20Mi"
        assert updated_eng.max_idle_duration == "5h"
        assert updated_eng.max_running_duration == "5h"
        assert updated_eng.display_name == "Changed display name"
        assert updated_eng.notebook_image == notebook_engine_image_i5.name

        eng = notebook_engine_client_super_admin.get_notebook_engine(name=eng.name)
        eng.profile = ""
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'profile cannot be unset' in json.loads(exc.value.body)["message"]

        eng.profile = "whatever"
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: NotebookEngineProfile name "whatever" is invalid' \
               in json.loads(exc.value.body)["message"]

        eng.profile = "workspaces/global/notebookEngineProfiles/non-existing"
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'notebookEngineProfile workspaces/global/notebookEngineProfiles/non-existing not found' \
               in json.loads(exc.value.body)["message"]

        eng.profile = notebook_engine_profile_p4.name
        with pytest.raises(CustomApiException) as exc:
            notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'validation error: max constraint violated: cpu (3) must be <= 1' \
               in json.loads(exc.value.body)["message"]

        # Set engine params to fit the constraints of the new profile.
        eng.cpu = 1
        eng.gpu = 0
        eng.memory_bytes = "20Mi"
        eng.max_idle_duration = "4h"
        eng.max_running_duration = "4h"
        eng.display_name = "Some display name"

        updated_eng = notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=eng)
        assert updated_eng.cpu == 1
        assert updated_eng.gpu == 0
        assert updated_eng.memory_bytes == "20Mi"
        assert updated_eng.storage_bytes == "20Mi"
        assert updated_eng.max_idle_duration == "4h"
        assert updated_eng.max_running_duration == "4h"
        assert updated_eng.display_name == "Some display name"
        assert updated_eng.profile == notebook_engine_profile_p4.name
        assert updated_eng.notebook_image == notebook_engine_image_i5.name
        # storageClassName always remains unchanged after creation (immutable).
        assert updated_eng.storage_class_name == "sc3"
    finally:
        notebook_engine_client_super_admin.delete_notebook_engine(
            name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}",
        )
