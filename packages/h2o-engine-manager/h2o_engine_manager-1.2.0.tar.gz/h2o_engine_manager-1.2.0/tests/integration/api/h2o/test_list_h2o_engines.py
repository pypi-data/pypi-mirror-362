import time
from typing import List

from h2o_engine_manager.clients.h2o_engine.h2o_engine import H2OEngine
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_list(
    h2o_engine_client,
    delete_all_h2os_before_after,
    h2o_engine_profile_p4,
    h2o_engine_version_v1,
):
    workspace_id = "99fbaf4a-87cc-460d-bc03-b21d016dbfa1"

    # No engines to be found.
    page = h2o_engine_client.list_engines(workspace_id=workspace_id)
    assert len(page.engines) == 0
    assert page.next_page_token == ""
    assert page.total_size == 0

    h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id="e1",
        node_count=1,
        cpu=1,
        gpu=0,
        memory_bytes="2Gi",
        display_name="my engine 1",
        max_idle_duration="5h",
        max_running_duration="10h",
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id="e2",
        node_count=1,
        cpu=2,
        gpu=0,
        memory_bytes="2Gi",
        display_name="my engine 2",
        max_idle_duration="5h",
        max_running_duration="10h",
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id="e3",
        node_count=1,
        cpu=3,
        gpu=0,
        memory_bytes="2Gi",
        display_name="my engine 3",
        max_idle_duration="5h",
        max_running_duration="10h",
        profile=h2o_engine_profile_p4.name,
        h2o_engine_version=h2o_engine_version_v1.name,
    )

    time.sleep(CACHE_SYNC_SECONDS)

    # List first page.
    page = h2o_engine_client.list_engines(workspace_id=workspace_id, page_size=1)
    assert len(page.engines) == 1
    assert page.next_page_token != ""
    assert page.total_size == 3

    # List second (last) page.
    page = h2o_engine_client.list_engines(
        workspace_id=workspace_id, page_size=2, page_token=page.next_page_token
    )
    assert len(page.engines) == 2
    assert page.next_page_token == ""
    assert page.total_size == 3

    # Test exceeding max page size.
    page = h2o_engine_client.list_engines(workspace_id=workspace_id, page_size=1001)
    assert len(page.engines) == 3
    assert page.next_page_token == ""
    assert page.total_size == 3

    # Test empty after filter.
    page = h2o_engine_client.list_engines(
        workspace_id=workspace_id, filter="cpu = 0 AND cpu != 0"
    )
    assert len(page.engines) == 0
    assert page.next_page_token == ""
    assert page.total_size == 0

    # Test orderBy and filter.
    page = h2o_engine_client.list_engines(
        workspace_id=workspace_id,
        order_by="cpu asc, name desc",
        filter="cpu >= 2 AND gpu <= 2",
    )
    assert len(page.engines) == 2
    assert page.next_page_token == ""
    assert page.total_size == 2
    check_ordered_filtered(engines=page.engines)


def check_ordered_filtered(engines: List[H2OEngine]):
    # Hardcoded values based on filter/orderBy params in tests.
    for i in range(0, len(engines) - 1):
        assert engines[i].cpu >= 2
        assert engines[i].gpu <= 2

        assert engines[i].cpu <= engines[i + 1].cpu
        if engines[i].cpu == engines[i + 1].cpu:
            assert engines[i].name >= engines[i + 1].name
