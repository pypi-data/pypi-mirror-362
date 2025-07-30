from enum import Enum

from h2o_engine_manager.gen.model.dai_engine_profile_config_editability import (
    DAIEngineProfileConfigEditability,
)


class ConfigEditability(Enum):
    CONFIG_EDITABILITY_UNSPECIFIED = "CONFIG_EDITABILITY_UNSPECIFIED"
    CONFIG_EDITABILITY_DISABLED = "CONFIG_EDITABILITY_DISABLED"
    CONFIG_EDITABILITY_BASE_CONFIG_ONLY = "CONFIG_EDITABILITY_BASE_CONFIG_ONLY"
    CONFIG_EDITABILITY_FULL = "CONFIG_EDITABILITY_FULL"

    def to_api_object(self) -> DAIEngineProfileConfigEditability:
        return DAIEngineProfileConfigEditability(self.name)


def from_api_object(api_object: DAIEngineProfileConfigEditability) -> ConfigEditability:
    return ConfigEditability(str(api_object))
