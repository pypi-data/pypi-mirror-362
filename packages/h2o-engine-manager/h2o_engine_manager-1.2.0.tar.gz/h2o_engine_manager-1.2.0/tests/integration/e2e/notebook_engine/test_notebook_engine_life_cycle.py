import http

import pytest

from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine.engine import NotebookEngine
from h2o_engine_manager.clients.notebook_engine.state import NotebookEngineState


@pytest.mark.timeout(180)
def test_notebook_engine_life_cycle(
    notebook_engine_client_super_admin,
    notebook_engine_profile_p1,
    notebook_engine_image_i1,
    notebook_engine_image_i3,
):
    workspace_id = "8cf6b17d-c018-48f0-8d05-cdd5fba22893"
    engine_id = "ntbk-e1"

    engine = notebook_engine_client_super_admin.create_notebook_engine(
        parent=f"workspaces/{workspace_id}",
        notebook_engine=NotebookEngine(
            profile=notebook_engine_profile_p1.name,
            notebook_image=notebook_engine_image_i1.name,
            display_name="Notebook E1",
        ),
        notebook_engine_id=engine_id,
    )

    assert engine.name == f"workspaces/{workspace_id}/notebookEngines/{engine_id}"
    assert engine.display_name == "Notebook E1"
    assert engine.cpu == 1
    assert engine.gpu == 0
    assert engine.memory_bytes == "20Mi"
    assert engine.storage_bytes == "20Mi"
    assert engine.max_idle_duration == "4h"
    assert engine.max_running_duration == "4h"
    assert engine.state == NotebookEngineState.STATE_STARTING
    assert engine.reconciling is True
    assert engine.profile_info.storage_class_name == "sc1"
    assert engine.profile_info.gpu_resource_name == "amd.com/gpu"
    assert engine.notebook_image == notebook_engine_image_i1.name
    assert engine.storage_class_name == notebook_engine_profile_p1.storage_class_name
    assert engine.create_time is not None
    assert engine.resume_time is None

    page = notebook_engine_client_super_admin.list_notebook_engines(parent=f"workspaces/{workspace_id}")
    assert len(page.notebook_engines) == 1
    assert page.notebook_engines[0].name == f"workspaces/{workspace_id}/notebookEngines/{engine_id}"
    assert page.next_page_token == ""

    all_engines = notebook_engine_client_super_admin.list_all_notebook_engines(parent=f"workspaces/{workspace_id}")
    assert len(all_engines) == 1
    assert all_engines[0].name == f"workspaces/{workspace_id}/notebookEngines/{engine_id}"

    engine = notebook_engine_client_super_admin.pause_notebook_engine(name=engine.name)
    assert engine.state == NotebookEngineState.STATE_PAUSING

    notebook_engine_client_super_admin.wait(name=engine.name, timeout_seconds=30)
    engine = notebook_engine_client_super_admin.get_notebook_engine(name=engine.name)
    assert engine.state == NotebookEngineState.STATE_PAUSED
    assert engine.reconciling is False

    engine.display_name = "updated display name"
    engine.cpu = 2
    engine.gpu = 1
    engine.memory_bytes = "40Mi"
    # storageBytes should be ignored during updated
    engine.storage_bytes = "40Mi"
    engine.max_idle_duration = "2h"
    engine.max_running_duration = "2h"
    engine.notebook_image = notebook_engine_image_i3.name

    updated_engine = notebook_engine_client_super_admin.update_notebook_engine(notebook_engine=engine)
    assert updated_engine.display_name == "updated display name"
    assert updated_engine.cpu == 2
    assert updated_engine.gpu == 1
    assert updated_engine.memory_bytes == "40Mi"
    assert updated_engine.storage_bytes == "20Mi"
    assert updated_engine.max_idle_duration == "2h"
    assert updated_engine.max_running_duration == "2h"
    assert updated_engine.notebook_image == notebook_engine_image_i3.name
    assert updated_engine.resume_time is None

    engine = notebook_engine_client_super_admin.resume_notebook_engine(name=updated_engine.name)
    assert engine.state == NotebookEngineState.STATE_STARTING
    assert engine.resume_time is not None
    assert engine.create_time < engine.resume_time

    # TODO wait until the notebookEngine is running
    # Create mocked notebook image for that purpose.

    notebook_engine_client_super_admin.delete_notebook_engine(name=engine.name)

    deleted_engine = notebook_engine_client_super_admin.get_notebook_engine(name=engine.name)
    assert deleted_engine.state == NotebookEngineState.STATE_DELETING

    notebook_engine_client_super_admin.wait(name=engine.name, timeout_seconds=30)

    with pytest.raises(CustomApiException) as exc:
        notebook_engine_client_super_admin.get_notebook_engine(name=engine.name)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
