import http

import pytest

from h2o_engine_manager.clients.exception import CustomApiException
from h2o_engine_manager.clients.notebook_engine.engine import NotebookEngine
from h2o_engine_manager.gen.exceptions import ForbiddenException


@pytest.mark.timeout(180)
def test_list_all_workspaces(
        engine_client_super_admin,
        dai_client,
        dai_super_admin_client,
        h2o_engine_client,
        h2o_engine_admin_client,
        notebook_engine_client,
        notebook_engine_client_super_admin,
        dai_engine_version_client_super_admin,
        h2o_engine_version_client_super_admin,
        dai_engine_profile_p10,
        dai_engine_profile_p27,
        dai_engine_version_v1_10_4_1,
        dai_engine_version_v1_10_4_9,
        dai_engine_version_v1_10_5,
        dai_engine_version_v1_11_4,
        h2o_engine_profile_p3,
        h2o_engine_version_v0_0_0_2,
        h2o_engine_version_v3_36_1_5,
        h2o_engine_version_v3_38_0_4,
        h2o_engine_version_v3_40_0_3,
        notebook_engine_profile_p2,
        notebook_engine_image_i2,
):
    workspace_id_1 = "c832d5d3-4fc7-4f05-bca0-fe08b77eaed5"
    workspace_id_2 = "95f9925c-033f-4093-8b48-2fe786c01598"

    list_workspace_id = "-"

    # Create two engines of each type, one in each workspace, and each by a different user
    try:
        dai1 = dai_client.create_engine(
            workspace_id=workspace_id_1,
            engine_id="dai1",
            display_name="My engine 1",
            cpu=1,
            memory_bytes="1Mi",
            storage_bytes="1Ki",
            annotations={"e1": "v1"},
            profile=dai_engine_profile_p27.name,
            dai_engine_version=dai_engine_version_v1_10_4_1.name,
        )
        dai2 = dai_super_admin_client.create_engine(
            workspace_id=workspace_id_2,
            engine_id="dai2",
            display_name="My engine 2",
            cpu=4,
            memory_bytes="1Ki",
            storage_bytes="1Ki",
            annotations={"e2": "v2"},
            profile=dai_engine_profile_p27.name,
            dai_engine_version=dai_engine_version_v1_10_5.name,
        )

        h2o1 = h2o_engine_client.create_engine(
            workspace_id=workspace_id_1,
            engine_id="h2o1",
            node_count=1,
            cpu=2,
            gpu=0,
            memory_bytes="1Mi",
            max_idle_duration="2h",
            max_running_duration="12h",
            profile=h2o_engine_profile_p3.name,
            h2o_engine_version=h2o_engine_version_v3_36_1_5.name,
        )
        h2o2 = h2o_engine_admin_client.create_engine(
            workspace_id=workspace_id_2,
            engine_id="h2o2",
            node_count=1,
            cpu=2,
            gpu=0,
            memory_bytes="1Ki",
            max_idle_duration="2h",
            max_running_duration="12h",
            profile=h2o_engine_profile_p3.name,
            h2o_engine_version=h2o_engine_version_v3_38_0_4.name,
        )


        ntb1 = notebook_engine_client.create_notebook_engine(
            parent=f"workspaces/{workspace_id_1}",
            notebook_engine_id="ntb1",
            notebook_engine=NotebookEngine(
                profile=notebook_engine_profile_p2.name,
                notebook_image=notebook_engine_image_i2.name,
            ),
        )
        ntb2 = notebook_engine_client_super_admin.create_notebook_engine(
            parent=f"workspaces/{workspace_id_2}",
            notebook_engine_id="ntb2",
            notebook_engine=NotebookEngine(
                profile=notebook_engine_profile_p2.name,
                notebook_image=notebook_engine_image_i2.name,
            ),
        )

        # All engines are present when listing
        page = engine_client_super_admin.list_engines(workspace_id=list_workspace_id)

        # Build a dictionary with engine name as the key and engine as the value
        engine_map = {engine.name: engine for engine in page.engines}
        # Check if all engines are present and visitable field is set correctly
        assert dai1.name in engine_map
        assert engine_map[dai1.name].visitable == False

        assert dai2.name in engine_map
        assert engine_map[dai2.name].visitable == True

        assert h2o1.name in engine_map
        assert engine_map[h2o1.name].visitable == True

        assert h2o2.name in engine_map
        assert engine_map[h2o2.name].visitable == True

        assert ntb1.name in engine_map
        assert engine_map[ntb1.name].visitable == False

        assert ntb2.name in engine_map
        assert engine_map[ntb2.name].visitable == True

    finally:
        dai_super_admin_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id_1}/daiEngines/dai1", allow_missing=True
        )
        dai_super_admin_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id_2}/daiEngines/dai2", allow_missing=True
        )
        h2o_engine_admin_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
            name_4=f"workspaces/{workspace_id_1}/h2oEngines/h2o1", allow_missing=True
        )
        h2o_engine_admin_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
            name_4=f"workspaces/{workspace_id_2}/h2oEngines/h2o2", allow_missing=True
        )
        # This will not immediately delete notebookEngine but only trigger its deletion.
        notebook_engine_client_super_admin.delete_notebook_engine(
            name=f"workspaces/{workspace_id_1}/notebookEngines/ntb1"
        )
        notebook_engine_client_super_admin.delete_notebook_engine(
            name=f"workspaces/{workspace_id_2}/notebookEngines/ntb2"
        )


def test_list_all_forbidden(
        engine_client_deny_user
):
    workspace_id = "c832d5d3-4fc7-4f05-bca0-fe08b77eaed5"
    with pytest.raises(ForbiddenException) as exc:
        engine_client_deny_user.list_engines(workspace_id=workspace_id)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN