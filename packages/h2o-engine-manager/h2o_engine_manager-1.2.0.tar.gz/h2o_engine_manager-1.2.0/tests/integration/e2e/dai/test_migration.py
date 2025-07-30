import os
import subprocess

import pytest


# Overwriting default pytest timeout for this long-running test method.
@pytest.mark.timeout(900)
@pytest.mark.skip(
    reason="Infra has been destroyed with latest cloud-dev wipe. Test is turned off until further migration "
           "development is needed."
)
def test_steam_migration(dai_client):
    """
    Goal of this test is to verify migration from the static Steam deployment.
    """
    # Configure migration.
    os.environ["H2O_PLATFORM_TOKEN"] = os.getenv("PLATFORM_TOKEN_ADMIN")
    os.environ["AIEM_URL"] = os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST")
    os.environ["STEAM_URL"] = "http://a1f0680a35630490ab3639f9b7b85b86-1387703942.us-east-1.elb.amazonaws.com:9555/"
    os.environ["STEAM_ADMIN_PAT"] = os.getenv("STEAM_MIGRATION_ADMIN_PAT")
    os.environ["UPGRADE_VERSION"] = "1.10.4"
    os.environ["ISSUER_URL"] = os.getenv("PLATFORM_OIDC_URL")
    os.environ["CLIENT_ID"] = os.getenv("PLATFORM_OIDC_CLIENT_ID")

    migration_finished = False

    # Migrated engines will have these IDs.
    migrated_engines_id = ["mig1-26", "mig2-27", "mig3-28", "renamed-29", "non-dai-data-30"]

    try:
        # Call the script.
        subprocess.check_call(["hatch", "run", "test:python", "../migrator/migrate_steam.py"])
        migration_finished = True

        # Test that all engines were migrated.
        for engine_id in migrated_engines_id:
            dai_client.get_engine(workspace_id="default", engine_id=engine_id)

        # Resume one of the migrated engines, connect and verify internal state (experiment).
        engine = dai_client.get_engine(workspace_id="default", engine_id="mig1-26")
        engine.resume()
        engine.wait()
        dai = engine.connect()

        # Experiment was trained on the Steam-launched instance, it should migrate and be found on the AIEM-resumed engine.
        assert dai.experiments.get("e43451bc-313f-11ee-b6db-0683cc8dda2a").name == "waputimo"

        # Verify also second instance that was created with non-dai uid/gid.
        engine = dai_client.get_engine(workspace_id="default", engine_id="non-dai-data-30")
        engine.resume()
        engine.wait()
        dai = engine.connect()
        assert dai.experiments.get("b5131ca2-31de-11ee-a164-d2fd64940e25").name == "simewola"

    finally:
        allow_missing = False
        if not migration_finished:
            # If the migration failed, then we cannot know whether the engines were created.
            allow_missing = True

        for engine_id in migrated_engines_id:
            dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
                name=f"workspaces/default/daiEngines/{engine_id}", allow_missing=allow_missing)
