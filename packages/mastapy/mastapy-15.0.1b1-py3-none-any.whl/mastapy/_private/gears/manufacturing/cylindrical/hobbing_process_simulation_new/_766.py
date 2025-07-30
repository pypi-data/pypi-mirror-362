"""CentreDistanceOffsetMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CENTRE_DISTANCE_OFFSET_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "CentreDistanceOffsetMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CentreDistanceOffsetMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="CentreDistanceOffsetMethod._Cast_CentreDistanceOffsetMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CentreDistanceOffsetMethod",)


class CentreDistanceOffsetMethod(Enum):
    """CentreDistanceOffsetMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CENTRE_DISTANCE_OFFSET_METHOD

    CONSTANT_CENTRE_DISTANCE_OFFSET = 0
    PARABOLIC_CURVE_FOR_CENTRE_DISTANCE_OFFSET = 1
    SPECIFIED_GEAR_LEAD_MODIFICATION = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CentreDistanceOffsetMethod.__setattr__ = __enum_setattr
CentreDistanceOffsetMethod.__delattr__ = __enum_delattr
