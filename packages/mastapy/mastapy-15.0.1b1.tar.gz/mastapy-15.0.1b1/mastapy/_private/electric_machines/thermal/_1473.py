"""InletLocation"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INLET_LOCATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "InletLocation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InletLocation")
    CastSelf = TypeVar("CastSelf", bound="InletLocation._Cast_InletLocation")


__docformat__ = "restructuredtext en"
__all__ = ("InletLocation",)


class InletLocation(Enum):
    """InletLocation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INLET_LOCATION

    FRONT = 0
    REAR = 1
    MIDDLE = 2
    CUSTOM = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


InletLocation.__setattr__ = __enum_setattr
InletLocation.__delattr__ = __enum_delattr
