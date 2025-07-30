import time
from typing import List

import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine import DAIEngine
from tests.integration.conftest import CACHE_SYNC_SECONDS


# Need to set higher timeout because engine deletion during test may take some time.
@pytest.mark.timeout(50)
def test_list_dai_engines_dynamic_dataset(
    dai_client,
    dai_engine_profile_30,
    dai_engine_version_v1_11_25,
):
    workspace_id = "69b6d745-f1c2-4d01-9ad8-514b81f620d0"

    try:
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e1",
            cpu=5,
            profile=dai_engine_profile_30.name,
            dai_engine_version=dai_engine_version_v1_11_25.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e3",
            cpu=5,
            profile=dai_engine_profile_30.name,
            dai_engine_version=dai_engine_version_v1_11_25.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e5",
            cpu=4,
            profile=dai_engine_profile_30.name,
            dai_engine_version=dai_engine_version_v1_11_25.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e6",
            cpu=6,
            profile=dai_engine_profile_30.name,
            dai_engine_version=dai_engine_version_v1_11_25.name,
        )
        time.sleep(CACHE_SYNC_SECONDS)

        # Check total order.
        engines = dai_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc")
        assert_engines_order(engines=engines, ids=["e5", "e1", "e3", "e6"])

        page = dai_client.list_engines(workspace_id=workspace_id, page_size=1, order_by="cpu asc, name asc")
        assert len(page.engines) == 1
        assert page.engines[0].engine_id == "e5"
        assert page.next_page_token != ""
        assert page.total_size == 4

        # Create new resource during pagination.
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e2",
            cpu=4,
            profile=dai_engine_profile_30.name,
            dai_engine_version=dai_engine_version_v1_11_25.name,
        )
        # Create new resource during pagination.
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e7",
            cpu=4,
            profile=dai_engine_profile_30.name,
            dai_engine_version=dai_engine_version_v1_11_25.name,
        )
        time.sleep(CACHE_SYNC_SECONDS)

        # Check total order.
        engines = dai_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc")
        assert_engines_order(engines=engines, ids=["e2", "e5", "e7", "e1", "e3", "e6"])

        # List next page using token. Token is based of e5, so the next should be the new e7.
        # Engine e2 will be skipped.
        page = dai_client.list_engines(
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
        e1 = dai_client.get_engine(workspace_id=workspace_id, engine_id="e1")
        e1.delete()
        e1.wait()

        # Check total order.
        engines = dai_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc")
        assert_engines_order(engines=engines, ids=["e2", "e5", "e7", "e3", "e6"])

        # Using page token based of e7. Next engine is e3.
        page = dai_client.list_engines(
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
        e6 = dai_client.get_engine(workspace_id=workspace_id, engine_id="e6")
        e6.delete()
        e6.wait()

        # Check total order.
        engines = dai_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc")
        assert_engines_order(engines=engines, ids=["e2", "e5", "e7", "e3"])

        # Use next page token based of e3. There's nothing left.
        page = dai_client.list_engines(
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
            dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
                name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}", allow_missing=True,
            )


def assert_engines_order(engines: List[DAIEngine], ids: List[str]):
    assert len(engines) == len(ids)

    for i in range(0, len(engines)):
        assert engines[i].engine_id == ids[i]


@pytest.mark.timeout(50)
def test_list_dai_engines_dynamic_dataset_with_filtering(
    dai_client,
    dai_engine_profile_31,
    dai_engine_version_v1_11_26,
):
    workspace_id = "3dd468c5-d50b-44bb-9468-b3c6765bdf21"

    try:
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e1",
            cpu=5,
            profile=dai_engine_profile_31.name,
            dai_engine_version=dai_engine_version_v1_11_26.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e3",
            cpu=5,
            profile=dai_engine_profile_31.name,
            dai_engine_version=dai_engine_version_v1_11_26.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e5",
            cpu=4,
            profile=dai_engine_profile_31.name,
            dai_engine_version=dai_engine_version_v1_11_26.name,
        )
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e6",
            cpu=6,
            profile=dai_engine_profile_31.name,
            dai_engine_version=dai_engine_version_v1_11_26.name,
        )
        time.sleep(CACHE_SYNC_SECONDS)

        # Check total order.
        engines = dai_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc", filter="cpu > 4")
        assert_engines_order(engines=engines, ids=["e1", "e3", "e6"])

        page = dai_client.list_engines(
            workspace_id=workspace_id,
            page_size=1,
            order_by="cpu asc, name asc",
            filter="cpu > 4",
        )
        assert len(page.engines) == 1
        assert page.engines[0].engine_id == "e1"
        assert page.next_page_token != ""
        assert page.total_size == 3

        # Create new resource during pagination.
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e2",
            cpu=4,
            profile=dai_engine_profile_31.name,
            dai_engine_version=dai_engine_version_v1_11_26.name,
        )
        # Create new resource during pagination.
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id="e7",
            cpu=4,
            profile=dai_engine_profile_31.name,
            dai_engine_version=dai_engine_version_v1_11_26.name,
        )
        time.sleep(CACHE_SYNC_SECONDS)

        # Check total order.
        engines = dai_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc", filter="cpu > 4")
        assert_engines_order(engines=engines, ids=["e1", "e3", "e6"])

        page = dai_client.list_engines(
            workspace_id=workspace_id,
            page_size=1,
            page_token=page.next_page_token,
            order_by="cpu asc, name asc",
            filter="cpu > 4",
        )
        assert len(page.engines) == 1
        assert page.engines[0].engine_id == "e3"
        assert page.next_page_token != ""
        assert page.total_size == 3

        e6 = dai_client.get_engine(workspace_id=workspace_id, engine_id="e6")
        e6.delete()
        e6.wait()

        # Check total order.
        engines = dai_client.list_all_engines(workspace_id=workspace_id, order_by="cpu asc, name asc", filter="cpu > 4")
        assert_engines_order(engines=engines, ids=["e1", "e3"])

        # Use next page token based of e3. There's nothing left.
        page = dai_client.list_engines(
            workspace_id=workspace_id,
            page_size=1,
            page_token=page.next_page_token,
            order_by="cpu asc, name asc",
            filter="cpu > 4",
        )
        assert len(page.engines) == 0
        assert page.next_page_token == ""
        assert page.total_size == 2
    finally:
        for engine_id in ["e1", "e2", "e3", "e5", "e6", "e7"]:
            dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
                name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}", allow_missing=True,
            )
