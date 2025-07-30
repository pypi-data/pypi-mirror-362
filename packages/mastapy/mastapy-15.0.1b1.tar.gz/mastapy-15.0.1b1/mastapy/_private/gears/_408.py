"""CoefficientOfFrictionCalculationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COEFFICIENT_OF_FRICTION_CALCULATION_METHOD = python_net_import(
    "SMT.MastaAPI.Gears", "CoefficientOfFrictionCalculationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CoefficientOfFrictionCalculationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoefficientOfFrictionCalculationMethod._Cast_CoefficientOfFrictionCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoefficientOfFrictionCalculationMethod",)


class CoefficientOfFrictionCalculationMethod(Enum):
    """CoefficientOfFrictionCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COEFFICIENT_OF_FRICTION_CALCULATION_METHOD

    ISOTR_1417912001 = 0
    ISOTR_1417912001_WITH_SURFACE_ROUGHNESS_PARAMETER = 1
    ISOTR_1417922001 = 2
    ISOTR_1417922001_MARTINS_ET_AL = 3
    DROZDOV_AND_GAVRIKOV = 4
    ODONOGHUE_AND_CAMERON = 5
    MISHARIN = 6
    ISO_TC60 = 7
    BENEDICT_AND_KELLEY = 8
    MATSUMOTO = 9
    USERSPECIFIED = 10
    SCRIPT = 11


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CoefficientOfFrictionCalculationMethod.__setattr__ = __enum_setattr
CoefficientOfFrictionCalculationMethod.__delattr__ = __enum_delattr
