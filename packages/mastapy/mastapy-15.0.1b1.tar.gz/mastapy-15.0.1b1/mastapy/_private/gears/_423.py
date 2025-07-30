"""Hand"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HAND = python_net_import("SMT.MastaAPI.Gears", "Hand")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Hand")
    CastSelf = TypeVar("CastSelf", bound="Hand._Cast_Hand")


__docformat__ = "restructuredtext en"
__all__ = ("Hand",)


class Hand(Enum):
    """Hand

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HAND

    LEFT = 0
    RIGHT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


Hand.__setattr__ = __enum_setattr
Hand.__delattr__ = __enum_delattr
