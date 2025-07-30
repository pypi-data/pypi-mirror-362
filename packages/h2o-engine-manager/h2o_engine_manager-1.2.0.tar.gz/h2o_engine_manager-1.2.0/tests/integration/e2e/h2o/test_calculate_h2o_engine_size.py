from h2o_engine_manager.clients.h2o_engine.size import H2OEngineSizeLimits


def test_calculate_h2o_engine_size_raw_dataset(h2o_engine_client):
    # unlimited
    recommended_size = h2o_engine_client.calculate_h2o_engine_size_raw_dataset(
        dataset_size_bytes="1k",
        limits=H2OEngineSizeLimits(
            memory_bytes_per_node_min="100",
            node_count_min=2,
        )
    )
    assert recommended_size.memory_bytes == "2500"
    assert recommended_size.node_count == 2

    # limited
    recommended_size = h2o_engine_client.calculate_h2o_engine_size_raw_dataset(
        dataset_size_bytes="1k",
        limits=H2OEngineSizeLimits(
            memory_bytes_per_node_min="100",
            node_count_min=1,
            memory_bytes_per_node_max="200",
            node_count_max=2,
        )
    )
    assert recommended_size.memory_bytes == "200"
    assert recommended_size.node_count == 2


def test_calculate_h2o_engine_size_compressed_dataset(h2o_engine_client):
    recommended_size = h2o_engine_client.calculate_h2o_engine_size_compressed_dataset(
        rows_count=100,
        columns_count=100,
        limits=H2OEngineSizeLimits(
            memory_bytes_per_node_min="100",
            node_count_min=2,
        )
    )
    assert recommended_size.memory_bytes == "160k"
    assert recommended_size.node_count == 2
