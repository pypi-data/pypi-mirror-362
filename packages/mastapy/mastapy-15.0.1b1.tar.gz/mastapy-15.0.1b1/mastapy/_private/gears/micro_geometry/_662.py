"""FlankSide"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FLANK_SIDE = python_net_import("SMT.MastaAPI.Gears.MicroGeometry", "FlankSide")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FlankSide")
    CastSelf = TypeVar("CastSelf", bound="FlankSide._Cast_FlankSide")


__docformat__ = "restructuredtext en"
__all__ = ("FlankSide",)


class FlankSide(Enum):
    """FlankSide

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FLANK_SIDE

    LEFT_SIDE = 0
    RIGHT_SIDE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FlankSide.__setattr__ = __enum_setattr
FlankSide.__delattr__ = __enum_delattr
