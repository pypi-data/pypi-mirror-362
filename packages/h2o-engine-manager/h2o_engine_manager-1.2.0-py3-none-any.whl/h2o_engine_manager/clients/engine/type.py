from enum import Enum

from h2o_engine_manager.gen.model.v1_engine_type import V1EngineType


class EngineType(Enum):
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    TYPE_DRIVERLESS_AI = "TYPE_DRIVERLESS_AI"
    TYPE_H2O = "TYPE_H2O"
    TYPE_NOTEBOOK = "TYPE_NOTEBOOK"

    def to_api_object(self) -> V1EngineType:
        return V1EngineType(self.name)


def from_api_engine_type(type: V1EngineType) -> EngineType:
    return EngineType(str(type))
