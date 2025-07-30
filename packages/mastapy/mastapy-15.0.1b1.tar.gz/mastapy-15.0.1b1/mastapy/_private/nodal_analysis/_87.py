"""RatingTypeForBearingReliability"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RATING_TYPE_FOR_BEARING_RELIABILITY = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "RatingTypeForBearingReliability"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RatingTypeForBearingReliability")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RatingTypeForBearingReliability._Cast_RatingTypeForBearingReliability",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RatingTypeForBearingReliability",)


class RatingTypeForBearingReliability(Enum):
    """RatingTypeForBearingReliability

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RATING_TYPE_FOR_BEARING_RELIABILITY

    ISO_2812007 = 0
    ISO_2812007_WITH_LIFE_MODIFICATION_FACTOR = 1
    ISO_162812025 = 2
    ISO_162812025_WITH_LIFE_MODIFICATION_FACTOR = 3
    ANSIABMA_92015_AND_ANSIABMA_112014 = 4
    ANSIABMA_92015_AND_ANSIABMA_112014_WITH_LIFE_MODIFICATION_FACTORS = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RatingTypeForBearingReliability.__setattr__ = __enum_setattr
RatingTypeForBearingReliability.__delattr__ = __enum_delattr
