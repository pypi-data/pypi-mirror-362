"""DegreeOfFreedom"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DEGREE_OF_FREEDOM = python_net_import("SMT.MastaAPI.MathUtility", "DegreeOfFreedom")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DegreeOfFreedom")
    CastSelf = TypeVar("CastSelf", bound="DegreeOfFreedom._Cast_DegreeOfFreedom")


__docformat__ = "restructuredtext en"
__all__ = ("DegreeOfFreedom",)


class DegreeOfFreedom(Enum):
    """DegreeOfFreedom

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DEGREE_OF_FREEDOM

    X = 0
    Y = 1
    Z = 2
    ΘX = 3
    ΘY = 4
    ΘZ = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DegreeOfFreedom.__setattr__ = __enum_setattr
DegreeOfFreedom.__delattr__ = __enum_delattr
