"""BasicDynamicLoadRatingCalculationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BASIC_DYNAMIC_LOAD_RATING_CALCULATION_METHOD = python_net_import(
    "SMT.MastaAPI.Bearings", "BasicDynamicLoadRatingCalculationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BasicDynamicLoadRatingCalculationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BasicDynamicLoadRatingCalculationMethod._Cast_BasicDynamicLoadRatingCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BasicDynamicLoadRatingCalculationMethod",)


class BasicDynamicLoadRatingCalculationMethod(Enum):
    """BasicDynamicLoadRatingCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BASIC_DYNAMIC_LOAD_RATING_CALCULATION_METHOD

    ISO_2812007_STANDARD = 0
    ISO_281_A52011_HYBRID_BEARING_WITH_SILICON_NITRIDE_ELEMENTS = 1
    ISOTR_128112008E_USING_ACTUAL_BEARING_INTERNAL_GEOMETRY = 2
    USERSPECIFIED = 3
    ANSIABMA_92015_AND_ANSIABMA_112014 = 4
    ISO_2005612017E = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BasicDynamicLoadRatingCalculationMethod.__setattr__ = __enum_setattr
BasicDynamicLoadRatingCalculationMethod.__delattr__ = __enum_delattr
