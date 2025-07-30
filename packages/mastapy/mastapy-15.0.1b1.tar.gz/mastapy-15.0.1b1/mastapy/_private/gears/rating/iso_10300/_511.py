"""GeneralLoadFactorCalculationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GENERAL_LOAD_FACTOR_CALCULATION_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "GeneralLoadFactorCalculationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GeneralLoadFactorCalculationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeneralLoadFactorCalculationMethod._Cast_GeneralLoadFactorCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeneralLoadFactorCalculationMethod",)


class GeneralLoadFactorCalculationMethod(Enum):
    """GeneralLoadFactorCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GENERAL_LOAD_FACTOR_CALCULATION_METHOD

    METHOD_B = 0
    METHOD_C = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GeneralLoadFactorCalculationMethod.__setattr__ = __enum_setattr
GeneralLoadFactorCalculationMethod.__delattr__ = __enum_delattr
