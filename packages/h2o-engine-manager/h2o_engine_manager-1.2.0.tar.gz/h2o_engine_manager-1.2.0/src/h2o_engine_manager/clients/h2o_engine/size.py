from dataclasses import dataclass
from typing import Optional

from h2o_engine_manager.clients.convert import duration_convertor
from h2o_engine_manager.clients.convert import quantity_convertor
from h2o_engine_manager.gen.model.v1_h2_o_engine_size import V1H2OEngineSize
from h2o_engine_manager.gen.model.v1_h2_o_engine_size_limits import (
    V1H2OEngineSizeLimits,
)


@dataclass
class H2OEngineSizeLimits:
    """
    Attributes:
        memory_bytes_per_node_min (str):
            Minimum memory (in bytes) required per node. Supports quantity suffixes.
            Examples values: "1000", "1Mi", "20Gi", "20G".
        node_count_min (int):
            Minimum number of nodes required.
        memory_bytes_per_node_max (Optional[str]):
            Maximum memory (in bytes) allowed per node. Defaults to None. Supports quantity suffixes.
            Examples values: "1000", "1Mi", "20Gi", "20G".
        node_count_max (Optional[int]):
            Maximum number of nodes allowed. Defaults to None.


    Limits required for H2OEngine size calculation.
    """
    memory_bytes_per_node_min: str
    node_count_min: int
    memory_bytes_per_node_max: Optional[str] = None
    node_count_max: Optional[int] = None

    def h2o_engine_size_limits_to_api_obj(self) -> V1H2OEngineSizeLimits:
        node_count_max_str = None
        if self.node_count_max is not None:
            node_count_max_str = str(self.node_count_max)

        return V1H2OEngineSizeLimits(
            memory_bytes_per_node_min=quantity_convertor.quantity_to_number_str(
                quantity=self.memory_bytes_per_node_min,
            ),
            node_count_min=str(self.node_count_min),
            memory_bytes_per_node_max=quantity_convertor.optional_quantity_to_number_str(
                quantity=self.memory_bytes_per_node_max,
            ),
            node_count_max=node_count_max_str,
        )


@dataclass
class H2OEngineSize:
    """
    Recommended H2OEngine size.

    Attributes:
        memory_bytes (str):
            Total recommended memory size in bytes. Supports quantity suffixes.
        node_count (int):
            Recommended number of nodes.

    """
    memory_bytes: str
    node_count: int


def h2o_engine_size_from_api_obj(api_obj: V1H2OEngineSize) -> H2OEngineSize:
    return H2OEngineSize(
        memory_bytes=quantity_convertor.number_str_to_quantity(number_str=api_obj.memory_bytes),
        node_count=quantity_convertor.quantity_to_number(quantity=api_obj.node_count),
    )
