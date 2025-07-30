"""HypoidRatingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HYPOID_RATING_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Hypoid", "HypoidRatingMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HypoidRatingMethod")
    CastSelf = TypeVar("CastSelf", bound="HypoidRatingMethod._Cast_HypoidRatingMethod")


__docformat__ = "restructuredtext en"
__all__ = ("HypoidRatingMethod",)


class HypoidRatingMethod(Enum):
    """HypoidRatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HYPOID_RATING_METHOD

    GLEASON = 0
    ISO_103002014 = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HypoidRatingMethod.__setattr__ = __enum_setattr
HypoidRatingMethod.__delattr__ = __enum_delattr
