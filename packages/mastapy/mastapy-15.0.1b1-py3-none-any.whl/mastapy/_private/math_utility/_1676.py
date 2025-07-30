"""Axis"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_AXIS = python_net_import("SMT.MastaAPI.MathUtility", "Axis")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Axis")
    CastSelf = TypeVar("CastSelf", bound="Axis._Cast_Axis")


__docformat__ = "restructuredtext en"
__all__ = ("Axis",)


class Axis(Enum):
    """Axis

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _AXIS

    X = 0
    Y = 1
    Z = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


Axis.__setattr__ = __enum_setattr
Axis.__delattr__ = __enum_delattr
