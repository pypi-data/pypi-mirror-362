"""ThermalExpansionOptionForGroundedNodes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_THERMAL_EXPANSION_OPTION_FOR_GROUNDED_NODES = python_net_import(
    "SMT.MastaAPI.SystemModel", "ThermalExpansionOptionForGroundedNodes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ThermalExpansionOptionForGroundedNodes")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ThermalExpansionOptionForGroundedNodes._Cast_ThermalExpansionOptionForGroundedNodes",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThermalExpansionOptionForGroundedNodes",)


class ThermalExpansionOptionForGroundedNodes(Enum):
    """ThermalExpansionOptionForGroundedNodes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _THERMAL_EXPANSION_OPTION_FOR_GROUNDED_NODES

    NO_EXPANSION = 0
    EXPAND_ALWAYS = 1
    EXPAND_IF_NO_GROUNDED_FE_SUBSTRUCTURES = 2
    EXPAND_IF_NO_FE_HOUSING = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ThermalExpansionOptionForGroundedNodes.__setattr__ = __enum_setattr
ThermalExpansionOptionForGroundedNodes.__delattr__ = __enum_delattr
