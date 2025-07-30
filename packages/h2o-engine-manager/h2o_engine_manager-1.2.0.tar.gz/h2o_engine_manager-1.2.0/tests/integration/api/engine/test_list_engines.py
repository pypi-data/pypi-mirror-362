import os
import time

import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine_client import DAIEngineClient
from h2o_engine_manager.clients.dai_engine_profile.dai_engine_profile import (
    DAIEngineProfile,
)
from h2o_engine_manager.clients.dai_engine_version.version import DAIEngineVersion
from h2o_engine_manager.clients.engine.client import EngineClient
from h2o_engine_manager.clients.engine.state import EngineState
from h2o_engine_manager.clients.engine.type import EngineType
from h2o_engine_manager.clients.h2o_engine.client import H2OEngineClient
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile import (
    H2OEngineProfile,
)
from h2o_engine_manager.clients.h2o_engine_version.version import H2OEngineVersion
from h2o_engine_manager.clients.notebook_engine.engine import NotebookEngine
from tests.integration.conftest import CACHE_SYNC_SECONDS


@pytest.mark.timeout(180)
def test_list(
    engine_client,
    dai_client,
    dai_admin_client,
    h2o_engine_client,
    h2o_engine_admin_client,
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
    workspace_id = "10a4df10-2fea-47aa-a5a5-cbf7d476bbcc"

    try:
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="engine1",
            display_name="My engine 1",
            cpu=1,
            memory_bytes="1Mi",
            storage_bytes="1Ki",
            annotations={"e1": "v1"},
            profile=dai_engine_profile_p27.name,
            dai_engine_version=dai_engine_version_v1_10_4_1.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="engine2",
            display_name="My engine 2",
            cpu=4,
            memory_bytes="1Ki",
            storage_bytes="1Ki",
            annotations={"e2": "v2"},
            profile=dai_engine_profile_p27.name,
            dai_engine_version=dai_engine_version_v1_10_5.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="engine3",
            display_name="My engine 3",
            cpu=1,
            memory_bytes="1Ki",
            storage_bytes="1Ki",
            annotations={"e3": "v3"},
            profile=dai_engine_profile_p27.name,
            dai_engine_version=dai_engine_version_v1_10_4_1.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="engine4",
            display_name="My engine 4",
            cpu=5,
            memory_bytes="1Ki",
            storage_bytes="1Ki",
            profile=dai_engine_profile_p27.name,
            dai_engine_version=dai_engine_version_v1_10_4_9.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="engine5",
            profile=dai_engine_profile_p10.name,
            dai_engine_version=dai_engine_version_v1_11_4.name,
        )

        # We cannot create engine with deprecated version.
        # Set daiEngine1's and daiEngine3's assigned version 1.10.4.1 to deprecated.
        dai_engine_version_v1_10_4_1.deprecated = True
        updated_v1_10_4_1 = dai_engine_version_client_super_admin.update_dai_engine_version(
            dai_engine_version=dai_engine_version_v1_10_4_1,
        )
        assert updated_v1_10_4_1.deprecated is True

        # We cannot create engine with non-existent version.
        # Delete daiEngine4's version 1.10.4.9.
        dai_engine_version_client_super_admin.delete_dai_engine_version(
            name=dai_engine_version_v1_10_4_9.name,
        )

        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="engine1",
            node_count=1,
            cpu=2,
            gpu=0,
            memory_bytes="1Mi",
            max_idle_duration="2h",
            max_running_duration="12h",
            profile=h2o_engine_profile_p3.name,
            h2o_engine_version=h2o_engine_version_v3_36_1_5.name,
        )
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="engine2",
            node_count=1,
            cpu=2,
            gpu=0,
            memory_bytes="1Ki",
            max_idle_duration="2h",
            max_running_duration="12h",
            profile=h2o_engine_profile_p3.name,
            h2o_engine_version=h2o_engine_version_v3_38_0_4.name,
        )
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="engine3",
            node_count=1,
            cpu=3,
            gpu=1,
            memory_bytes="1Mi",
            max_idle_duration="2h",
            max_running_duration="12h",
            profile=h2o_engine_profile_p3.name,
            h2o_engine_version=h2o_engine_version_v3_40_0_3.name,
        )

        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="engine4",
            profile=h2o_engine_profile_p3.name,
            h2o_engine_version=h2o_engine_version_v0_0_0_2.name,
        )

        time.sleep(CACHE_SYNC_SECONDS)

        # Deprecate version (To test 'deprecate_version' field later).
        dai_engine_version_v1_11_4.deprecated = True
        dai_engine_version_client_super_admin.update_dai_engine_version(
            dai_engine_version=dai_engine_version_v1_11_4,
        )

        # Delete version (To test 'deleted_version' field later).
        h2o_engine_version_client_super_admin.delete_h2o_engine_version(
            name=h2o_engine_version_v0_0_0_2.name,
        )

        notebook_engine_client_super_admin.create_notebook_engine(
            parent=f"workspaces/{workspace_id}",
            notebook_engine_id="engine1",
            notebook_engine=NotebookEngine(
                profile=notebook_engine_profile_p2.name,
                notebook_image=notebook_engine_image_i2.name,
            ),
        )

        notebook_engine_client_super_admin.create_notebook_engine(
            parent=f"workspaces/{workspace_id}",
            notebook_engine_id="engine2",
            notebook_engine=NotebookEngine(
                profile=notebook_engine_profile_p2.name,
                notebook_image=notebook_engine_image_i2.name,
            ),
        )

        # When list first page
        page = engine_client.list_engines(workspace_id=workspace_id, page_size=2)

        # Then
        assert len(page.engines) == 2
        assert page.total_size == 11
        assert page.next_page_token != ""

        # When list second page
        page = engine_client.list_engines(
            workspace_id=workspace_id, page_size=2, page_token=page.next_page_token
        )

        # Then
        assert len(page.engines) == 2
        assert page.total_size == 11
        assert page.next_page_token != ""

        # When list third page
        page = engine_client.list_engines(
            workspace_id=workspace_id, page_size=1, page_token=page.next_page_token
        )

        # Then
        assert len(page.engines) == 1
        assert page.total_size == 11
        assert page.next_page_token != ""

        # When list fourth page
        page = engine_client.list_engines(
            workspace_id=workspace_id, page_size=2, page_token=page.next_page_token
        )

        # Then
        assert len(page.engines) == 2
        assert page.total_size == 11
        assert page.next_page_token != ""

        # When list fifth page
        page = engine_client.list_engines(
            workspace_id=workspace_id, page_size=2, page_token=page.next_page_token
        )

        # Then
        assert len(page.engines) == 2
        assert page.total_size == 11
        assert page.next_page_token != ""

        # When list sixth page
        page = engine_client.list_engines(
            workspace_id=workspace_id, page_size=1, page_token=page.next_page_token
        )

        # Then
        assert len(page.engines) == 1
        assert page.total_size == 11
        assert page.next_page_token != ""

        # When list seventh (last) page
        page = engine_client.list_engines(
            workspace_id=workspace_id, page_size=1, page_token=page.next_page_token
        )

        # Then
        assert len(page.engines) == 1
        assert page.total_size == 11
        assert page.next_page_token == ""

        # When order_by
        page = engine_client.list_engines(
            workspace_id=workspace_id,
            order_by="cpu desc, version desc, memory_bytes desc, storage_bytes asc",
        )

        # Then
        assert len(page.engines) == 11
        assert page.total_size == 11
        assert page.next_page_token == ""

        # highest cpu (5)
        assert page.engines[0].name == f"workspaces/{workspace_id}/daiEngines/engine4"
        # second-highest cpu (4)
        assert page.engines[1].name == f"workspaces/{workspace_id}/daiEngines/engine2"
        # third-highest cpu (3)
        assert page.engines[2].name == f"workspaces/{workspace_id}/h2oEngines/engine3"
        # highest version (3.40.0.3)
        assert page.engines[3].name == f"workspaces/{workspace_id}/h2oEngines/engine2"
        # second-highest version (3.38.0.4)
        assert page.engines[4].name == f"workspaces/{workspace_id}/h2oEngines/engine1"
        assert page.engines[4].profile == "workspaces/global/h2oEngineProfiles/p3"

        assert page.engines[5].name == f"workspaces/{workspace_id}/daiEngines/engine5"
        assert page.engines[5].version == "1.11.4"
        assert page.engines[5].deprecated_version is True
        assert page.engines[5].deleted_version is False
        assert page.engines[5].profile == "workspaces/global/daiEngineProfiles/p10"

        assert page.engines[6].name == f"workspaces/{workspace_id}/daiEngines/engine1"
        assert page.engines[6].profile == "workspaces/global/daiEngineProfiles/p27"

        assert page.engines[7].name == f"workspaces/{workspace_id}/daiEngines/engine3"
        assert page.engines[7].profile == "workspaces/global/daiEngineProfiles/p27"

        assert page.engines[8].name == f"workspaces/{workspace_id}/h2oEngines/engine4"
        assert page.engines[8].version == "0.0.0.2"
        assert page.engines[8].deprecated_version is False
        assert page.engines[8].deleted_version is True
        assert page.engines[8].profile == "workspaces/global/h2oEngineProfiles/p3"

        assert page.engines[9].name == f"workspaces/{workspace_id}/notebookEngines/engine1"
        assert page.engines[9].profile == "workspaces/global/notebookEngineProfiles/p2"

        assert page.engines[10].name == f"workspaces/{workspace_id}/notebookEngines/engine2"
        assert page.engines[10].profile == "workspaces/global/notebookEngineProfiles/p2"

        # When filter non-existing
        page = engine_client.list_engines(
            workspace_id=workspace_id,
            filter_expr="type != TYPE_DRIVERLESS_AI AND type != TYPE_H2O AND type != TYPE_NOTEBOOK",
        )

        # Then
        assert len(page.engines) == 0
        assert page.total_size == 0
        assert page.next_page_token == ""

        # When list only notebookEngines
        page = engine_client.list_engines(
            workspace_id=workspace_id,
            filter_expr="type = TYPE_NOTEBOOK",
            page_size=1,
        )
        assert len(page.engines) == 1
        assert page.total_size == 2
        assert page.engines[0].name == f"workspaces/{workspace_id}/notebookEngines/engine2"
        assert page.next_page_token != ""

        page = engine_client.list_engines(
            workspace_id=workspace_id,
            filter_expr="type = TYPE_NOTEBOOK",
            page_size=1,
            page_token=page.next_page_token,
        )
        assert len(page.engines) == 1
        assert page.total_size == 2
        assert page.engines[0].name == f"workspaces/{workspace_id}/notebookEngines/engine1"
        assert page.next_page_token == ""

        # When filter engines with deprecated version
        page = engine_client.list_engines(
            workspace_id=workspace_id,
            filter_expr="deprecated_version = true",
            order_by="name desc",
        )

        # Then
        assert len(page.engines) == 3
        assert page.total_size == 3
        assert page.next_page_token == ""

        assert page.engines[0].name == f"workspaces/{workspace_id}/daiEngines/engine5"
        assert page.engines[0].version == "1.11.4"
        assert page.engines[0].deprecated_version is True
        assert page.engines[0].deleted_version is False

        # Newly created engine is listed first.
        assert page.engines[1].name == f"workspaces/{workspace_id}/daiEngines/engine3"
        assert page.engines[1].version == "1.10.4.1"
        assert page.engines[1].deprecated_version is True

        assert page.engines[2].name == f"workspaces/{workspace_id}/daiEngines/engine1"
        assert page.engines[2].version == "1.10.4.1"
        assert page.engines[2].deprecated_version is True

        # When filter engines with deleted version
        page = engine_client.list_engines(
            workspace_id=workspace_id,
            filter_expr="deleted_version = true",
            order_by="name desc",
        )

        # Then
        assert len(page.engines) == 2
        assert page.total_size == 2
        assert page.next_page_token == ""
        assert page.engines[0].name == f"workspaces/{workspace_id}/h2oEngines/engine4"
        assert page.engines[0].version == "0.0.0.2"
        assert page.engines[0].deprecated_version is False
        assert page.engines[0].deleted_version is True
        assert page.engines[1].name == f"workspaces/{workspace_id}/daiEngines/engine4"
        assert page.engines[1].version == "1.10.4.9"
        assert page.engines[1].deleted_version is True

        # When filter
        expr = "type = TYPE_DRIVERLESS_AI AND version < \"1.10.5\" AND memory_bytes > 1024"
        page = engine_client.list_engines(workspace_id=workspace_id, filter_expr=expr)

        # Then
        assert len(page.engines) == 1
        assert page.total_size == 1
        assert page.next_page_token == ""
        assert page.engines[0].name == f"workspaces/{workspace_id}/daiEngines/engine1"

        # Extra check for correct mapping (Since we don't have GetEngine endpoint)
        eng = page.engines[0]
        assert eng.version == "1.10.4.1"
        assert eng.deprecated_version is True
        assert eng.engine_type == EngineType.TYPE_DRIVERLESS_AI
        assert eng.cpu == 1
        assert eng.gpu == 0
        assert eng.create_time is not None
        assert eng.update_time is None
        assert eng.delete_time is None
        assert eng.annotations["e1"] == "v1"
        assert eng.display_name == "My engine 1"
        assert eng.memory_bytes == "1Mi"
        assert eng.storage_bytes == "1Ki"
        assert eng.reconciling is True
        assert eng.creator.startswith("users/") and len(eng.creator) > len("users/")
        assert eng.creator_display_name == "test-user"
        assert eng.state == EngineState.STATE_STARTING
        external_scheme = os.getenv("MANAGER_EXTERNAL_SCHEME")
        external_host = os.getenv("MANAGER_EXTERNAL_HOST")
        assert (
            eng.login_url
            == f"{external_scheme}://{external_host}/workspaces/{workspace_id}/daiEngines/engine1/oidc/login"
        )
        assert eng.profile == "workspaces/global/daiEngineProfiles/p27"

        # List all
        engines = engine_client.list_all_engines(workspace_id=workspace_id)
        assert len(engines) == 11

        assert_dynamically_changing_dataset(
            engine_client=engine_client,
            dai_client=dai_client,
            workspace_id=workspace_id,
            dai_engine_profile=dai_engine_profile_p27,
            dai_engine_version=dai_engine_version_v1_10_5,
        )

    finally:
        # Clean up.
        for i in range(1, 8):
            dai_admin_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
                name_1=f"workspaces/{workspace_id}/daiEngines/engine{i}", allow_missing=True
            )
        for i in range(1, 5):
            h2o_engine_admin_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
                name_4=f"workspaces/{workspace_id}/h2oEngines/engine{i}", allow_missing=True
            )
        for i in range(1, 3):
            # This will not immediately delete notebookEngine but only trigger its deletion.
            notebook_engine_client_super_admin.delete_notebook_engine(
                name=f"workspaces/{workspace_id}/notebookEngines/engine{i}"
            )


def assert_dynamically_changing_dataset(
    engine_client: EngineClient,
    dai_client: DAIEngineClient,
    workspace_id: str,
    dai_engine_profile: DAIEngineProfile,
    dai_engine_version: DAIEngineVersion,
):
    # Create new 'last' DAIEngine
    dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id="engine7",
        profile=dai_engine_profile.name,
        dai_engine_version=dai_engine_version.name,
    )

    # List n-1 engines (so one more is left in the next page).
    page = engine_client.list_engines(
        workspace_id=workspace_id,
        page_size=5,
        filter_expr="type = TYPE_DRIVERLESS_AI",
        order_by="name asc"
    )
    assert len(page.engines) == 5
    assert page.engines[0].name == f"workspaces/{workspace_id}/daiEngines/engine1"
    assert page.engines[1].name == f"workspaces/{workspace_id}/daiEngines/engine2"
    assert page.engines[2].name == f"workspaces/{workspace_id}/daiEngines/engine3"
    assert page.engines[3].name == f"workspaces/{workspace_id}/daiEngines/engine4"
    assert page.engines[4].name == f"workspaces/{workspace_id}/daiEngines/engine5"
    assert page.total_size == 6
    assert page.next_page_token != ""

    # In the meanwhile create a new DAIEngine.

    # Create second last engine.
    dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id="engine6",
        profile=dai_engine_profile.name,
        dai_engine_version=dai_engine_version.name,
    )
    time.sleep(CACHE_SYNC_SECONDS)

    page = engine_client.list_engines(
        workspace_id=workspace_id,
        page_size=5,
        filter_expr="type = TYPE_DRIVERLESS_AI",
        order_by="name asc",
        page_token=page.next_page_token,
    )
    assert len(page.engines) == 2
    assert page.engines[0].name == f"workspaces/{workspace_id}/daiEngines/engine6"
    assert page.engines[1].name == f"workspaces/{workspace_id}/daiEngines/engine7"
    assert page.total_size == 7
    assert page.next_page_token == ""
