"""GearBlankFactorCalculationOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_BLANK_FACTOR_CALCULATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "GearBlankFactorCalculationOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearBlankFactorCalculationOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearBlankFactorCalculationOptions._Cast_GearBlankFactorCalculationOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearBlankFactorCalculationOptions",)


class GearBlankFactorCalculationOptions(Enum):
    """GearBlankFactorCalculationOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_BLANK_FACTOR_CALCULATION_OPTIONS

    AVERAGE_VALUE = 0
    MINIMUM_VALUE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearBlankFactorCalculationOptions.__setattr__ = __enum_setattr
GearBlankFactorCalculationOptions.__delattr__ = __enum_delattr
