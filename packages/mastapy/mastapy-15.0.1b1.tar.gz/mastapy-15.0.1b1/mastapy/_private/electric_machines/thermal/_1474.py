"""RegionIDForThermalAnalysis"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_REGION_ID_FOR_THERMAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "RegionIDForThermalAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RegionIDForThermalAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="RegionIDForThermalAnalysis._Cast_RegionIDForThermalAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RegionIDForThermalAnalysis",)


class RegionIDForThermalAnalysis(Enum):
    """RegionIDForThermalAnalysis

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _REGION_ID_FOR_THERMAL_ANALYSIS

    HOUSING = 0
    ENDCAP = 1
    FLUID_CHANNEL = 2
    FLUID_CHANNEL_WALL = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RegionIDForThermalAnalysis.__setattr__ = __enum_setattr
RegionIDForThermalAnalysis.__delattr__ = __enum_delattr
