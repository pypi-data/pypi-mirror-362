import pytest

from h2o_engine_manager.clients.constraint.profile_constraint_duration import (
    ProfileConstraintDuration,
)
from h2o_engine_manager.clients.constraint.profile_constraint_numeric import (
    ProfileConstraintNumeric,
)
from h2o_engine_manager.clients.notebook_engine_profile.profile import (
    NotebookEngineProfile,
)


@pytest.fixture(scope="function")
def notebook_engine_profile_p1(notebook_engine_profile_client_super_admin):
    created_profile = notebook_engine_profile_client_super_admin.create_notebook_engine_profile(
        parent="workspaces/global",
        notebook_engine_profile=NotebookEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            enabled=True,
            assigned_oidc_roles_enabled=False,
            storage_class_name="sc1",
            gpu_resource_name="amd.com/gpu",
        ),
        notebook_engine_profile_id="p1",
    )
    name = created_profile.name

    yield created_profile

    notebook_engine_profile_client_super_admin.delete_notebook_engine_profile(name=name)


@pytest.fixture(scope="function")
def notebook_engine_profile_p2(notebook_engine_profile_client_super_admin):
    created_profile = notebook_engine_profile_client_super_admin.create_notebook_engine_profile(
        parent="workspaces/global",
        notebook_engine_profile=NotebookEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            enabled=True,
            assigned_oidc_roles_enabled=False,
        ),
        notebook_engine_profile_id="p2",
    )
    name = created_profile.name

    yield created_profile

    notebook_engine_profile_client_super_admin.delete_notebook_engine_profile(name=name)


@pytest.fixture(scope="function")
def notebook_engine_profile_p3(notebook_engine_profile_client_super_admin):
    created_profile = notebook_engine_profile_client_super_admin.create_notebook_engine_profile(
        parent="workspaces/global",
        notebook_engine_profile=NotebookEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1", maximum="3"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="3", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi", maximum="2Gi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi", maximum="2Gi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="8h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="8h"),
            enabled=True,
            assigned_oidc_roles_enabled=False,
            storage_class_name="sc3",
        ),
        notebook_engine_profile_id="p3",
    )
    name = created_profile.name

    yield created_profile

    notebook_engine_profile_client_super_admin.delete_notebook_engine_profile(name=name)


@pytest.fixture(scope="function")
def notebook_engine_profile_p4(notebook_engine_profile_client_super_admin):
    created_profile = notebook_engine_profile_client_super_admin.create_notebook_engine_profile(
        parent="workspaces/global",
        notebook_engine_profile=NotebookEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1", maximum="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="0"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi", maximum="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi", maximum="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="4h", default="4h", maximum="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="4h", default="4h", maximum="4h"),
            enabled=True,
            assigned_oidc_roles_enabled=False,
            storage_class_name="sc4",
        ),
        notebook_engine_profile_id="p4",
    )
    name = created_profile.name

    yield created_profile

    notebook_engine_profile_client_super_admin.delete_notebook_engine_profile(name=name)
