"""GearPositions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_POSITIONS = python_net_import(
    "SMT.MastaAPI.Utility.ModalAnalysis.Gears", "GearPositions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearPositions")
    CastSelf = TypeVar("CastSelf", bound="GearPositions._Cast_GearPositions")


__docformat__ = "restructuredtext en"
__all__ = ("GearPositions",)


class GearPositions(Enum):
    """GearPositions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_POSITIONS

    UNSPECIFIED = 0
    PINION = 1
    WHEEL = 2
    SUN = 3
    PLANET = 4
    ANNULUS = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearPositions.__setattr__ = __enum_setattr
GearPositions.__delattr__ = __enum_delattr
