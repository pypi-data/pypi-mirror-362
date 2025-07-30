import time
from typing import List

import pytest

from h2o_engine_manager.clients.h2o_engine.client import H2OEngineClient
from h2o_engine_manager.clients.h2o_engine.h2o_engine import H2OEngine
from tests.integration.conftest import CACHE_SYNC_SECONDS


# Need to set higher timeout because engine deletion during test may take some time.
@pytest.mark.timeout(50)
def test_list_h2o_engines_dynamic_dataset(
    h2o_engine_client,
    h2o_engine_profile_p9,
    h2o_engine_version_v7,
):
    workspace_id = "b3d7749d-5973-4f0a-a828-8146f162cb7f"

    try:
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e1",
            cpu=5,
            profile=h2o_engine_profile_p9.name,
            h2o_engine_version=h2o_engine_version_v7.name,
        )
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e3",
            cpu=5,
            profile=h2o_engine_profile_p9.name,
            h2o_engine_version=h2o_engine_version_v7.name,
        )
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e5",
            cpu=4,
            profile=h2o_engine_profile_p9.name,
            h2o_engine_version=h2o_engine_version_v7.name,
        )
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e6",
            cpu=6,
            profile=h2o_engine_profile_p9.name,
            h2o_engine_version=h2o_engine_version_v7.name,
        )
        time.sleep(CACHE_SYNC_SECONDS)

        # Check total order.
        engines = h2o_engine_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc")
        assert_engines_order(engines=engines, ids=["e5", "e1", "e3", "e6"])

        page = h2o_engine_client.list_engines(workspace_id=workspace_id, page_size=1, order_by="cpu asc, name asc")
        assert len(page.engines) == 1
        assert page.engines[0].engine_id == "e5"
        assert page.next_page_token != ""
        assert page.total_size == 4

        # Create new resource during pagination.
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e2",
            cpu=4,
            profile=h2o_engine_profile_p9.name,
            h2o_engine_version=h2o_engine_version_v7.name,
        )
        # Create new resource during pagination.
        h2o_engine_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e7",
            cpu=4,
            profile=h2o_engine_profile_p9.name,
            h2o_engine_version=h2o_engine_version_v7.name,
        )
        time.sleep(CACHE_SYNC_SECONDS)

        # Check total order.
        engines = h2o_engine_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc")
        assert_engines_order(engines=engines, ids=["e2", "e5", "e7", "e1", "e3", "e6"])

        # List next page using token. Token is based of e5, so the next should be the new e7.
        # Engine e2 will be skipped.
        page = h2o_engine_client.list_engines(
            workspace_id=workspace_id,
            page_size=1,
            page_token=page.next_page_token,
            order_by="cpu asc, name asc",
        )
        assert len(page.engines) == 1
        assert page.engines[0].engine_id == "e7"
        assert page.next_page_token != ""
        assert page.total_size == 6

        # Delete resource during pagination.
        e1 = h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id="e1")
        e1.delete()
        e1.wait()

        # Check total order.
        engines = h2o_engine_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc")
        assert_engines_order(engines=engines, ids=["e2", "e5", "e7", "e3", "e6"])

        # Using page token based of e7. Next engine is e3.
        page = h2o_engine_client.list_engines(
            workspace_id=workspace_id,
            page_size=1,
            page_token=page.next_page_token,
            order_by="cpu asc, name asc",
        )
        assert len(page.engines) == 1
        assert page.engines[0].engine_id == "e3"
        assert page.next_page_token != ""
        assert page.total_size == 5

        # Delete last engine during pagination.
        e6 = h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id="e6")
        e6.delete()
        e6.wait()

        # Check total order.
        engines = h2o_engine_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc")
        assert_engines_order(engines=engines, ids=["e2", "e5", "e7", "e3"])

        # Use next page token based of e3. There's nothing left.
        page = h2o_engine_client.list_engines(
            workspace_id=workspace_id,
            page_size=1,
            page_token=page.next_page_token,
            order_by="cpu asc, name asc",
        )
        assert len(page.engines) == 0
        assert page.next_page_token == ""
        assert page.total_size == 4
    finally:
        for engine_id in ["e1", "e2", "e3", "e5", "e6", "e7"]:
            h2o_engine_client.client_info.api_instance.h2_o_engine_service_delete_h2_o_engine(
                name_4=f"workspaces/{workspace_id}/h2oEngines/{engine_id}", allow_missing=True,
            )


def assert_engines_order(engines: List[H2OEngine], ids: List[str]):
    assert len(engines) == len(ids)

    for i in range(0, len(engines)):
        assert engines[i].engine_id == ids[i]
