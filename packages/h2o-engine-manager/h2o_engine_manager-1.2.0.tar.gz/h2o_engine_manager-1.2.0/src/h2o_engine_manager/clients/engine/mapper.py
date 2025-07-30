from h2o_engine_manager.clients.convert import quantity_convertor
from h2o_engine_manager.clients.engine.engine import Engine
from h2o_engine_manager.clients.engine.state import from_api_engine_state
from h2o_engine_manager.clients.engine.type import from_api_engine_type
from h2o_engine_manager.gen.model.v1_engine import V1Engine


def from_api_engine(api_engine: V1Engine) -> Engine:
    """
    Map generated Engine object into custom Engine object.

    Args:
        api_engine: generated Engine object

    Returns:
        mapped Engine object
    """

    total_disk_size_bytes = None
    if api_engine.total_disk_size_bytes is not None:
        total_disk_size_bytes = quantity_convertor.number_str_to_quantity(
            api_engine.total_disk_size_bytes
        )

    free_disk_size_bytes = None
    if api_engine.free_disk_size_bytes is not None:
        free_disk_size_bytes = quantity_convertor.number_str_to_quantity(
            api_engine.free_disk_size_bytes
        )

    return Engine(
        name=api_engine.name,
        uid=api_engine.uid,
        creator=api_engine.creator,
        creator_display_name=api_engine.creator_display_name,
        engine_type=from_api_engine_type(api_engine.type),
        state=from_api_engine_state(api_engine.state),
        reconciling=api_engine.reconciling,
        create_time=api_engine.create_time,
        update_time=api_engine.update_time,
        delete_time=api_engine.delete_time,
        resume_time=api_engine.resume_time,
        login_url=api_engine.login_url,
        annotations=api_engine.annotations,
        display_name=api_engine.display_name,
        version=api_engine.version,
        deprecated_version=api_engine.deprecated_version,
        deleted_version=api_engine.deleted_version,
        cpu=api_engine.cpu,
        gpu=api_engine.gpu,
        memory_bytes=quantity_convertor.number_str_to_quantity(api_engine.memory_bytes),
        storage_bytes=quantity_convertor.number_str_to_quantity(
            api_engine.storage_bytes
        ),
        storage_resizing=api_engine.storage_resizing,
        total_disk_size_bytes=total_disk_size_bytes,
        free_disk_size_bytes=free_disk_size_bytes,
        profile=api_engine.profile,
        visitable=api_engine.visitable,
    )
