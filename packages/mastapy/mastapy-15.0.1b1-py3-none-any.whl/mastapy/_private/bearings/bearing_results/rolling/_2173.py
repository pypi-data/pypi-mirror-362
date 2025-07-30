"""BallBearingContactCalculation"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BALL_BEARING_CONTACT_CALCULATION = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "BallBearingContactCalculation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BallBearingContactCalculation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BallBearingContactCalculation._Cast_BallBearingContactCalculation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BallBearingContactCalculation",)


class BallBearingContactCalculation(Enum):
    """BallBearingContactCalculation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BALL_BEARING_CONTACT_CALCULATION

    FULL = 0
    BREWE_AND_HAMROCK_1977 = 1
    HAMROCK_AND_BREWE_1983 = 2
    HOUPERT_2016 = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BallBearingContactCalculation.__setattr__ = __enum_setattr
BallBearingContactCalculation.__delattr__ = __enum_delattr
