"""RatingTypeForShaftReliability"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RATING_TYPE_FOR_SHAFT_RELIABILITY = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "RatingTypeForShaftReliability"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RatingTypeForShaftReliability")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RatingTypeForShaftReliability._Cast_RatingTypeForShaftReliability",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RatingTypeForShaftReliability",)


class RatingTypeForShaftReliability(Enum):
    """RatingTypeForShaftReliability

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RATING_TYPE_FOR_SHAFT_RELIABILITY

    FATIGUE_FOR_FINITE_LIFE = 0
    FATIGUE_FOR_INFINITE_LIFE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RatingTypeForShaftReliability.__setattr__ = __enum_setattr
RatingTypeForShaftReliability.__delattr__ = __enum_delattr
