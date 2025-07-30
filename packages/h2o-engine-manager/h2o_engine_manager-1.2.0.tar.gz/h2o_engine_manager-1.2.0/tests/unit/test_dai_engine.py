from h2o_engine_manager.clients.dai_engine.dai_engine import DAIEngine
from h2o_engine_manager.clients.dai_engine.dai_engine import from_dai_engine_api_object


# Tests that custom DAI engine object can be transformed to and from
# generated client stubs.
def test_dai_engine_api_conversion():
    # Initialize with all writeable parameters
    engine = DAIEngine(
        cpu=1,
        gpu=1,
        memory_bytes="1G",
        storage_bytes="10Gi",
        config={"key": "val"},
        annotations={"key": "val"},
        max_idle_duration="5s",
        max_running_duration="2s",
        display_name="Display name",
    )
    # Convert to generated stub object
    api_engine = engine.to_api_object()
    # Convert back to custom object
    engine2 = from_dai_engine_api_object(client_info=None, api_engine=api_engine)
    # Verify attr similarity
    assert engine.__dict__ == engine2.__dict__
