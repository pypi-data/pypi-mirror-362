import pprint
from typing import Optional

from h2o_engine_manager.clients.convert import duration_convertor
from h2o_engine_manager.gen.model.v1_profile_constraint_duration import (
    V1ProfileConstraintDuration,
)


class ProfileConstraintDuration:
    def __init__(self, minimum: str, default: str, maximum: Optional[str] = None):
        self.minimum = minimum
        self.default = default
        self.maximum = maximum

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_api_object(self):
        maximum = None
        if self.maximum is not None:
            maximum = duration_convertor.duration_to_seconds(self.maximum)

        return V1ProfileConstraintDuration(
            min=duration_convertor.duration_to_seconds(self.minimum),
            default=duration_convertor.duration_to_seconds(self.default),
            max=maximum,
        )


def from_api_object(api_object: V1ProfileConstraintDuration) -> ProfileConstraintDuration:
    return ProfileConstraintDuration(
        minimum=duration_convertor.seconds_to_duration(api_object.min),
        default=duration_convertor.seconds_to_duration(api_object.default),
        maximum=duration_convertor.optional_seconds_to_duration(api_object.max),
    )
