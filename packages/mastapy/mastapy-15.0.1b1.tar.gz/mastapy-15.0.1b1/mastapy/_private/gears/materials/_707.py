"""RatingMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RATING_METHODS = python_net_import("SMT.MastaAPI.Gears.Materials", "RatingMethods")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RatingMethods")
    CastSelf = TypeVar("CastSelf", bound="RatingMethods._Cast_RatingMethods")


__docformat__ = "restructuredtext en"
__all__ = ("RatingMethods",)


class RatingMethods(Enum):
    """RatingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RATING_METHODS

    AGMA_2003C10 = 0
    GLEASON = 1
    ISO_103002014 = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RatingMethods.__setattr__ = __enum_setattr
RatingMethods.__delattr__ = __enum_delattr
