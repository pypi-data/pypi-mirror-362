"""EndWindingCoolingFlowSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_END_WINDING_COOLING_FLOW_SOURCE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "EndWindingCoolingFlowSource"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="EndWindingCoolingFlowSource")
    CastSelf = TypeVar(
        "CastSelf",
        bound="EndWindingCoolingFlowSource._Cast_EndWindingCoolingFlowSource",
    )


__docformat__ = "restructuredtext en"
__all__ = ("EndWindingCoolingFlowSource",)


class EndWindingCoolingFlowSource(Enum):
    """EndWindingCoolingFlowSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _END_WINDING_COOLING_FLOW_SOURCE

    NONE = 0
    CUSTOM = 1
    COOLING_JACKET = 2
    STATOR_CHANNEL = 3
    SHAFT_CHANNEL = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


EndWindingCoolingFlowSource.__setattr__ = __enum_setattr
EndWindingCoolingFlowSource.__delattr__ = __enum_delattr
