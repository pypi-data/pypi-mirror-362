"""PowerRatingF1EstimationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_POWER_RATING_F1_ESTIMATION_METHOD = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "PowerRatingF1EstimationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PowerRatingF1EstimationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PowerRatingF1EstimationMethod._Cast_PowerRatingF1EstimationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PowerRatingF1EstimationMethod",)


class PowerRatingF1EstimationMethod(Enum):
    """PowerRatingF1EstimationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _POWER_RATING_F1_ESTIMATION_METHOD

    ISOTR_141792001 = 0
    USERSPECIFIED = 1
    ONEDIMENSIONAL_LOOKUP_TABLE = 2
    TWODIMENSIONAL_LOOKUP_TABLE = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PowerRatingF1EstimationMethod.__setattr__ = __enum_setattr
PowerRatingF1EstimationMethod.__delattr__ = __enum_delattr
