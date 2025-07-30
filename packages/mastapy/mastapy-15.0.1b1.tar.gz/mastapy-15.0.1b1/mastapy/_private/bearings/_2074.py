"""BasicStaticLoadRatingCalculationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BASIC_STATIC_LOAD_RATING_CALCULATION_METHOD = python_net_import(
    "SMT.MastaAPI.Bearings", "BasicStaticLoadRatingCalculationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BasicStaticLoadRatingCalculationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BasicStaticLoadRatingCalculationMethod._Cast_BasicStaticLoadRatingCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BasicStaticLoadRatingCalculationMethod",)


class BasicStaticLoadRatingCalculationMethod(Enum):
    """BasicStaticLoadRatingCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BASIC_STATIC_LOAD_RATING_CALCULATION_METHOD

    ISO_76_STANDARD = 0
    ISO_76_SUPPLEMENT_2_HYBRID_BEARING_WITH_SILICON_NITRIDE_ELEMENTS = 1
    ISOTR_106571991_LARGE_RACE_GROOVE_RADII = 2
    USERSPECIFIED = 3
    ANSIABMA_92015_AND_ANSIABMA_112014 = 4
    ISO_2005622017E = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BasicStaticLoadRatingCalculationMethod.__setattr__ = __enum_setattr
BasicStaticLoadRatingCalculationMethod.__delattr__ = __enum_delattr
