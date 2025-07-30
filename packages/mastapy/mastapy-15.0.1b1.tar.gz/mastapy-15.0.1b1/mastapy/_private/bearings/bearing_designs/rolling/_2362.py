"""FatigueLoadLimitCalculationMethodEnum"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FATIGUE_LOAD_LIMIT_CALCULATION_METHOD_ENUM = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling",
    "FatigueLoadLimitCalculationMethodEnum",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FatigueLoadLimitCalculationMethodEnum")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FatigueLoadLimitCalculationMethodEnum._Cast_FatigueLoadLimitCalculationMethodEnum",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FatigueLoadLimitCalculationMethodEnum",)


class FatigueLoadLimitCalculationMethodEnum(Enum):
    """FatigueLoadLimitCalculationMethodEnum

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FATIGUE_LOAD_LIMIT_CALCULATION_METHOD_ENUM

    BASIC = 0
    ADVANCED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FatigueLoadLimitCalculationMethodEnum.__setattr__ = __enum_setattr
FatigueLoadLimitCalculationMethodEnum.__delattr__ = __enum_delattr
