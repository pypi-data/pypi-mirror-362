"""MagnetClearance"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MAGNET_CLEARANCE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "MagnetClearance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MagnetClearance")
    CastSelf = TypeVar("CastSelf", bound="MagnetClearance._Cast_MagnetClearance")


__docformat__ = "restructuredtext en"
__all__ = ("MagnetClearance",)


class MagnetClearance(Enum):
    """MagnetClearance

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MAGNET_CLEARANCE

    INSIDE = 0
    OUTSIDE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MagnetClearance.__setattr__ = __enum_setattr
MagnetClearance.__delattr__ = __enum_delattr
