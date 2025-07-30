"""MicropittingRatingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MICROPITTING_RATING_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "MicropittingRatingMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MicropittingRatingMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="MicropittingRatingMethod._Cast_MicropittingRatingMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicropittingRatingMethod",)


class MicropittingRatingMethod(Enum):
    """MicropittingRatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MICROPITTING_RATING_METHOD

    ISOTR_1514412010 = 0
    ISOTR_1514412014 = 1
    ISOTS_6336222018 = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MicropittingRatingMethod.__setattr__ = __enum_setattr
MicropittingRatingMethod.__delattr__ = __enum_delattr
