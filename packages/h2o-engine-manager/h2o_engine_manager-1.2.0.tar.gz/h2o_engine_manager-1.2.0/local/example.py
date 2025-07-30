import os

import h2o_engine_manager

workspace_id = "default"
engine_id = "my-engine"

daiengine_client = h2o_engine_manager.login_custom(
    endpoint=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
    refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
    issuer_url=os.getenv("PLATFORM_OIDC_URL"),
    client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
).dai_engine_client

print(f"total engines ({workspace_id}): {daiengine_client.list_engines(workspace_id=workspace_id).total_size}")

engine = daiengine_client.create_engine(
    workspace_id=workspace_id,
    engine_id=engine_id,
    cpu=1,
    gpu=0,
    memory_bytes="8Gi",
    storage_bytes="16Gi",
    max_idle_duration="15m",
    max_running_duration="2d",
    display_name="My engine",
)
print(f"{engine_id}: {engine.state.value}")

engine.wait()

print(f"{engine_id}: {engine.state.value}")
print(f"total engines ({workspace_id}): {daiengine_client.list_engines(workspace_id=workspace_id).total_size}")

# engine.connect()

engine.delete()
print(f"{engine_id}: {engine.state.value}")

engine.wait(timeout_seconds=100)
print(f"total engines ({workspace_id}): {daiengine_client.list_engines(workspace_id=workspace_id).total_size}")
