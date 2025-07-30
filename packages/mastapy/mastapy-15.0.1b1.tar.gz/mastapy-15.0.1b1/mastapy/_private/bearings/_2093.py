"""RatingLife"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RATING_LIFE = python_net_import("SMT.MastaAPI.Bearings", "RatingLife")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RatingLife")
    CastSelf = TypeVar("CastSelf", bound="RatingLife._Cast_RatingLife")


__docformat__ = "restructuredtext en"
__all__ = ("RatingLife",)


class RatingLife(Enum):
    """RatingLife

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RATING_LIFE

    _10 = 0
    _5 = 1
    _4 = 2
    _3 = 3
    _2 = 4
    _1 = 5
    _08 = 6
    _06 = 7
    _04 = 8
    _02 = 9
    _01 = 10
    _008 = 11
    _006 = 12
    _005 = 13


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RatingLife.__setattr__ = __enum_setattr
RatingLife.__delattr__ = __enum_delattr
