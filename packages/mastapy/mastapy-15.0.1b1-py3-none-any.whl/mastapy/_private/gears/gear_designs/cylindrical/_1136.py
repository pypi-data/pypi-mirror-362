"""CylindricalGearProfileMeasurementType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_PROFILE_MEASUREMENT_TYPE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "CylindricalGearProfileMeasurementType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearProfileMeasurementType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearProfileMeasurementType._Cast_CylindricalGearProfileMeasurementType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearProfileMeasurementType",)


class CylindricalGearProfileMeasurementType(Enum):
    """CylindricalGearProfileMeasurementType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CYLINDRICAL_GEAR_PROFILE_MEASUREMENT_TYPE

    DIAMETER = 0
    RADIUS = 1
    ROLL_ANGLE = 2
    ROLL_DISTANCE = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CylindricalGearProfileMeasurementType.__setattr__ = __enum_setattr
CylindricalGearProfileMeasurementType.__delattr__ = __enum_delattr
