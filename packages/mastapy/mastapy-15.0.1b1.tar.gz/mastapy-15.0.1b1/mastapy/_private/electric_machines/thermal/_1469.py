"""HeatTransferCoefficientCalculationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HEAT_TRANSFER_COEFFICIENT_CALCULATION_METHOD = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "HeatTransferCoefficientCalculationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HeatTransferCoefficientCalculationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HeatTransferCoefficientCalculationMethod._Cast_HeatTransferCoefficientCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HeatTransferCoefficientCalculationMethod",)


class HeatTransferCoefficientCalculationMethod(Enum):
    """HeatTransferCoefficientCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HEAT_TRANSFER_COEFFICIENT_CALCULATION_METHOD

    CONVECTION_CORRELATION = 0
    USERSPECIFIED_HTC = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HeatTransferCoefficientCalculationMethod.__setattr__ = __enum_setattr
HeatTransferCoefficientCalculationMethod.__delattr__ = __enum_delattr
