"""RegionID"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_REGION_ID = python_net_import("SMT.MastaAPI.ElectricMachines", "RegionID")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RegionID")
    CastSelf = TypeVar("CastSelf", bound="RegionID._Cast_RegionID")


__docformat__ = "restructuredtext en"
__all__ = ("RegionID",)


class RegionID(Enum):
    """RegionID

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _REGION_ID

    STATOR_CORE = 0
    STATOR_SLOT = 1
    STATOR_WEDGE = 2
    REGION_BETWEEN_WEDGE_AND_AIR_GAP = 3
    AIR_GAP_STATOR_SIDE = 4
    STATOR_CUTOUTS = 5
    STATOR_COOLING_CHANNEL = 6
    ROTOR_CORE = 7
    ROTOR_AIR_REGION = 8
    ROTOR_COOLING_CHANNEL = 9
    MAGNET = 10
    AIR_GAP_ROTOR_SIDE = 11
    SHAFT = 12
    CONDUCTOR = 13
    FIELD_WINDING = 14
    LINER = 15
    STATOR_TEETH = 16
    CONDUCTOR_INSULATION = 17


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RegionID.__setattr__ = __enum_setattr
RegionID.__delattr__ = __enum_delattr
