import pprint
from typing import Optional

from h2o_engine_manager.clients.convert import quantity_convertor
from h2o_engine_manager.gen.model.v1_profile_constraint_numeric import (
    V1ProfileConstraintNumeric,
)


class ProfileConstraintNumeric:
    def __init__(
        self,
        minimum: str,
        default: str,
        maximum: Optional[str] = None,
        cumulative_maximum: Optional[str] = None,
    ):
        self.minimum = minimum
        self.default = default
        self.maximum = maximum
        self.cumulative_maximum = cumulative_maximum

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_api_object(self):
        maximum = None
        if self.maximum is not None:
            maximum = quantity_convertor.quantity_to_number_str(self.maximum)

        cumulative_maximum = None
        if self.cumulative_maximum is not None:
            cumulative_maximum = quantity_convertor.quantity_to_number_str(self.cumulative_maximum)

        return V1ProfileConstraintNumeric(
            min=quantity_convertor.quantity_to_number_str(self.minimum),
            default=quantity_convertor.quantity_to_number_str(self.default),
            max=maximum,
            cumulative_max=cumulative_maximum,
        )


def from_api_object(api_object: V1ProfileConstraintNumeric) -> ProfileConstraintNumeric:
    maximum = None
    if api_object.max is not None:
        maximum = quantity_convertor.number_str_to_quantity(api_object.max)

    cumulative_maximum = None
    if api_object.cumulative_max is not None:
        cumulative_maximum = quantity_convertor.number_str_to_quantity(api_object.cumulative_max)

    return ProfileConstraintNumeric(
        minimum=quantity_convertor.number_str_to_quantity(api_object.min),
        default=quantity_convertor.number_str_to_quantity(api_object.default),
        maximum=maximum,
        cumulative_maximum=cumulative_maximum,
    )
