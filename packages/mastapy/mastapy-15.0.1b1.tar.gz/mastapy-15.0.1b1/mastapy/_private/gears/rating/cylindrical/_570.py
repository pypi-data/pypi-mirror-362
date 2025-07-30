"""RatingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RATING_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "RatingMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RatingMethod")
    CastSelf = TypeVar("CastSelf", bound="RatingMethod._Cast_RatingMethod")


__docformat__ = "restructuredtext en"
__all__ = ("RatingMethod",)


class RatingMethod(Enum):
    """RatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RATING_METHOD

    METHOD_B = 0
    METHOD_C = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RatingMethod.__setattr__ = __enum_setattr
RatingMethod.__delattr__ = __enum_delattr
