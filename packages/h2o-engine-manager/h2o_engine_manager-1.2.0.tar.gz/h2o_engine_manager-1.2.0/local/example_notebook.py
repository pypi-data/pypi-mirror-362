import os
import time

import h2o_engine_manager
from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.constraint.profile_constraint_duration import (
    ProfileConstraintDuration,
)
from h2o_engine_manager.clients.constraint.profile_constraint_numeric import (
    ProfileConstraintNumeric,
)
from h2o_engine_manager.clients.notebook_engine.engine import NotebookEngine
from h2o_engine_manager.clients.notebook_engine_image.image_config import (
    NotebookEngineImageConfig,
)
from h2o_engine_manager.clients.notebook_engine_profile.config import (
    NotebookEngineProfileConfig,
)

workspace_id = "default"
engine_id = "my-engine"

clients = h2o_engine_manager.login_custom(
    endpoint=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
    refresh_token=os.getenv("PLATFORM_TOKEN_SUPER_ADMIN"),
    issuer_url=os.getenv("PLATFORM_OIDC_URL"),
    client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
)

engine_client = clients.notebook_engine_client
profile_client = clients.notebook_engine_profile_client
image_client = clients.notebook_engine_image_client

p1_config = NotebookEngineProfileConfig(
    notebook_engine_profile_id="p1",
    cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
    gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
    memory_bytes_constraint=ProfileConstraintNumeric(minimum="200Mi", default="800Mi"),
    storage_bytes_constraint=ProfileConstraintNumeric(minimum="200Mi", default="800Mi"),
    max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
    max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
    enabled=True,
    assigned_oidc_roles_enabled=False,
)
profile_client.apply_notebook_engine_profile_configs(
    configs=[p1_config],
    parent="workspaces/global",
)

img1_config = NotebookEngineImageConfig(
    notebook_engine_image_id="img1",
    image="353750902984.dkr.ecr.us-east-1.amazonaws.com/h2oai-notebookengine-cpu:latest-snapshot",
    image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS,
    image_pull_secrets=["regcred"],
)
image_client.apply_notebook_engine_image_configs(
    configs=[img1_config],
    parent="workspaces/global",
)

eng1 = engine_client.create_notebook_engine(
    parent="workspaces/default",
    notebook_engine=NotebookEngine(
        profile="workspaces/global/notebookEngineProfiles/p1",
        notebook_image="workspaces/global/notebookEngineImages/img1",
    ),
    notebook_engine_id=engine_id,
)
print(f"engine: {eng1}")

eng1 = engine_client.wait(name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}")
print(f"engine: {eng1}")

eng1 = engine_client.access_notebook_engine(name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}")
print(f"engine: {eng1}")

eng1 = engine_client.pause_notebook_engine(name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}")
print(f"engine: {eng1}")

eng1 = engine_client.wait(name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}")
print(f"engine: {eng1}")

eng1 = engine_client.resume_notebook_engine(name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}")
print(f"engine: {eng1}")

eng1 = engine_client.wait(name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}")
print(f"engine: {eng1}")

eng1 = engine_client.delete_notebook_engine(name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}")
print(f"engine: {eng1}")

eng1 = engine_client.wait(name=f"workspaces/{workspace_id}/notebookEngines/{engine_id}")
print(f"engine: {eng1}")