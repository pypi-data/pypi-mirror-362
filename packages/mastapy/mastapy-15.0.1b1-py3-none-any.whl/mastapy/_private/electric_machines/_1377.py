"""CoilPositionInSlot"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COIL_POSITION_IN_SLOT = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CoilPositionInSlot"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CoilPositionInSlot")
    CastSelf = TypeVar("CastSelf", bound="CoilPositionInSlot._Cast_CoilPositionInSlot")


__docformat__ = "restructuredtext en"
__all__ = ("CoilPositionInSlot",)


class CoilPositionInSlot(Enum):
    """CoilPositionInSlot

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COIL_POSITION_IN_SLOT

    CENTRE = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CoilPositionInSlot.__setattr__ = __enum_setattr
CoilPositionInSlot.__delattr__ = __enum_delattr
