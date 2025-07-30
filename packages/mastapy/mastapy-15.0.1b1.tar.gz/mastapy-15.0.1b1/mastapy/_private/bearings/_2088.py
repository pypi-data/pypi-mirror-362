"""HybridSteelAll"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HYBRID_STEEL_ALL = python_net_import("SMT.MastaAPI.Bearings", "HybridSteelAll")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HybridSteelAll")
    CastSelf = TypeVar("CastSelf", bound="HybridSteelAll._Cast_HybridSteelAll")


__docformat__ = "restructuredtext en"
__all__ = ("HybridSteelAll",)


class HybridSteelAll(Enum):
    """HybridSteelAll

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HYBRID_STEEL_ALL

    ALL = 0
    STEEL = 1
    HYBRID = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HybridSteelAll.__setattr__ = __enum_setattr
HybridSteelAll.__delattr__ = __enum_delattr
