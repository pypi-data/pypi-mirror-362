"""ElectricMachineSearchRegionSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ELECTRIC_MACHINE_SEARCH_REGION_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel",
    "ElectricMachineSearchRegionSpecificationMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElectricMachineSearchRegionSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineSearchRegionSpecificationMethod._Cast_ElectricMachineSearchRegionSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineSearchRegionSpecificationMethod",)


class ElectricMachineSearchRegionSpecificationMethod(Enum):
    """ElectricMachineSearchRegionSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ELECTRIC_MACHINE_SEARCH_REGION_SPECIFICATION_METHOD

    FROM_POWER_LOAD = 0
    FROM_ELECTRIC_MACHINE_DETAIL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ElectricMachineSearchRegionSpecificationMethod.__setattr__ = __enum_setattr
ElectricMachineSearchRegionSpecificationMethod.__delattr__ = __enum_delattr
