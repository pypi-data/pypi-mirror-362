import http
import json
import time

import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_migrate_creator_with_dai_engine_version(
    dai_client,
    dai_admin_client,
    admin_user_name,
    regular_user_user_name,
    dai_engine_profile_p11,
    dai_engine_version_v1_10_7_2,
):
    workspace_id = "bb425231-bd1e-4868-979e-a127f0e036aa"
    engine_id = "e2-migrate-creator"

    try:
        # Create an engine as the aiem-test-user user
        eng = dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=dai_engine_profile_p11.name,
            dai_engine_version=dai_engine_version_v1_10_7_2.name,
        )
        assert eng.creator == regular_user_user_name
        # As a display name, AIEM is using value directly from access token (one of its subs).
        # In this case it's configured to be field "username" in Keycloak user.
        assert eng.creator_display_name == "test-user"

        time.sleep(CACHE_SYNC_SECONDS)

        # Get the engine as an admin user
        eng_admin = dai_admin_client.get_engine(
            engine_id=engine_id, workspace_id=workspace_id
        )

        # Only stopped engine can be migrated.
        assert eng.state != DAIEngineState.STATE_PAUSED
        with pytest.raises(CustomApiException) as exc:
            eng_admin.migrate_creator(new_creator=admin_user_name)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST

        # Pause the engine
        eng.pause()
        eng.wait()

        # Try to migrate to non-existing user
        with pytest.raises(CustomApiException) as exc:
            eng_admin.migrate_creator(new_creator="users/foo")
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
        assert 'user users/foo not found' in json.loads(exc.value.body)["message"]

        # Migrate creator as an admin user, connect to it as a new creator
        eng_admin.migrate_creator(new_creator=admin_user_name)
        eng_admin.resume()
        eng_admin.wait()
        eng_admin.connect()

        assert eng_admin.creator == admin_user_name
        # When migrating user, AIEM uses for display name value defined in UserServer for that specific user.
        # In this case it's configured to be fields "firstName lastName" in Keycloak user.
        assert eng_admin.creator_display_name == "Test Admin"
    finally:
        dai_admin_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )
