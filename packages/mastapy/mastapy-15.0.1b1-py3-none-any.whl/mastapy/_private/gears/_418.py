"""GearSetModes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_SET_MODES = python_net_import("SMT.MastaAPI.Gears", "GearSetModes")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearSetModes")
    CastSelf = TypeVar("CastSelf", bound="GearSetModes._Cast_GearSetModes")


__docformat__ = "restructuredtext en"
__all__ = ("GearSetModes",)


class GearSetModes(Enum):
    """GearSetModes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_SET_MODES

    DESIGN = 0
    MICRO_GEOMETRY = 1
    MICRO_GEOMETRY_ADVANCED_LTCA = 2
    CYLINDRICAL_MANUFACTURING_POWER_FLOW = 3
    CYLINDRICAL_MANUFACTURING_SYSTEM_DEFLECTION = 4
    BEVEL_MANUFACTURING = 5
    BEVEL_LTCA = 6


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearSetModes.__setattr__ = __enum_setattr
GearSetModes.__delattr__ = __enum_delattr
