import http
import time
from typing import List

import pytest

from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.api.dai.create_dai_request import *
from tests.integration.conftest import CACHE_SYNC_SECONDS


def create_engines(dai_client, workspace_id):
    req1 = CreateDAIEngineRequest(
        workspace_id=workspace_id, engine_id="test-list-engine1", cpu=1, gpu=3, version="latest"
    )
    req2 = CreateDAIEngineRequest(
        workspace_id=workspace_id, engine_id="test-list-engine2", cpu=2, gpu=2, version="1.10.5-mock"
    )
    req3 = CreateDAIEngineRequest(
        workspace_id=workspace_id, engine_id="test-list-engine3", cpu=2, gpu=1, version="1.10.6"
    )
    create_dai_from_request(dai_client, req1)
    create_dai_from_request(dai_client, req2)
    create_dai_from_request(dai_client, req3)

    time.sleep(CACHE_SYNC_SECONDS)


@pytest.mark.parametrize(
    ["workspace_id", "page_size", "page_token", "order_by", "filter_str"],
    [
        ("default", -20, "", "", ""),
        ("default", 0, "non-existing-token", "", ""),
        ("default", 0, "", "incorrect order by", ""),
        ("default", 0, "", "", "incorrect filter"),
    ],
)
def test_list_validation(
    dai_client, workspace_id, page_size, page_token, order_by, filter_str
):
    with pytest.raises(CustomApiException) as exc:
        dai_client.list_engines(
            workspace_id=workspace_id,
            page_size=page_size,
            page_token=page_token,
            order_by=order_by,
            filter=filter_str,
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_list(dai_client):
    workspace_id="32d12eaa-6602-47ee-b037-a2c21a994ad4"
    # Test no engines found.
    page = dai_client.list_engines(workspace_id)
    assert len(page.engines) == 0
    assert page.next_page_token == ""
    assert page.total_size == 0

    # Arrange
    create_engines(dai_client=dai_client, workspace_id=workspace_id)

    # Test getting first page.
    page = dai_client.list_engines(workspace_id=workspace_id, page_size=1)
    assert len(page.engines) == 1
    assert page.next_page_token != ""
    assert page.total_size == 3

    # Test getting second page.
    page = dai_client.list_engines(
        workspace_id=workspace_id, page_size=1, page_token=page.next_page_token
    )
    assert len(page.engines) == 1
    assert page.next_page_token != ""
    assert page.total_size == 3

    # Test getting last page.
    page = dai_client.list_engines(
        workspace_id=workspace_id, page_size=1, page_token=page.next_page_token
    )
    assert len(page.engines) == 1
    assert page.next_page_token == ""
    assert page.total_size == 3

    # Test exceeding max page size.
    page = dai_client.list_engines(workspace_id=workspace_id, page_size=1001)
    assert len(page.engines) == 3
    assert page.next_page_token == ""
    assert page.total_size == 3

    # Test empty after filter.
    page = dai_client.list_engines(
        workspace_id=workspace_id, filter="cpu = 0 AND cpu != 0"
    )
    assert len(page.engines) == 0
    assert page.next_page_token == ""
    assert page.total_size == 0

    # Test orderBy and filter.
    page = dai_client.list_engines(
        workspace_id=workspace_id,
        order_by="cpu asc, name desc",
        filter="cpu >= 2 AND gpu <= 2",
    )
    assert len(page.engines) == 2
    assert page.next_page_token == ""
    assert page.total_size == 2
    check_ordered_filtered(engines=page.engines)


def test_list_all(dai_client):
    workspace_id = "01c2b5a8-4c1c-42b2-af6f-71e41a6ce22f"
    create_engines(dai_client=dai_client, workspace_id=workspace_id)

    # Test basic list_all.
    engines = dai_client.list_all_engines(workspace_id=workspace_id)
    assert len(engines) == 3

    # Test list_all with additional params.
    engines = dai_client.list_all_engines(
        workspace_id=workspace_id,
        order_by="cpu asc, name desc",
        filter="cpu >= 2 AND gpu <= 2",
    )
    assert len(engines) == 2
    check_ordered_filtered(engines=engines)

    # Test version sorting & filtering.
    engines = dai_client.list_all_engines(
        workspace_id=workspace_id,
        order_by="version asc",
        filter="version < \"latest\" AND version >= \"1.10.5-mock\"",
    )
    assert len(engines) == 2
    assert engines[0].version == "1.10.5-mock"
    assert engines[1].version == "1.10.6"

    # Test version sorting & filtering.
    engines = dai_client.list_all_engines(
        workspace_id=workspace_id, filter="version = \"latest\""
    )
    assert len(engines) == 1
    assert engines[0].version == "1.10.6.1"

    # Test order by UID.
    page = dai_client.list_engines(workspace_id=workspace_id, order_by="uid desc")

    for i in range(0, len(page.engines) - 1):
        assert page.engines[i].uid >= page.engines[i + 1].uid


def check_ordered_filtered(engines: List[DAIEngine]):
    # Hardcoded values based on filter/orderBy params in tests.
    for i in range(0, len(engines) - 1):
        assert engines[i].cpu >= 2
        assert engines[i].gpu <= 2

        assert engines[i].cpu <= engines[i + 1].cpu
        if engines[i].cpu == engines[i + 1].cpu:
            assert engines[i].name >= engines[i + 1].name
