"""HousingFlowDirection"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HOUSING_FLOW_DIRECTION = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "HousingFlowDirection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HousingFlowDirection")
    CastSelf = TypeVar(
        "CastSelf", bound="HousingFlowDirection._Cast_HousingFlowDirection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HousingFlowDirection",)


class HousingFlowDirection(Enum):
    """HousingFlowDirection

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HOUSING_FLOW_DIRECTION

    FRONT_TO_REAR = 0
    REAR_TO_FRONT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HousingFlowDirection.__setattr__ = __enum_setattr
HousingFlowDirection.__delattr__ = __enum_delattr
