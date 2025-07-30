"""GearWindageAndChurningLossCalculationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_WINDAGE_AND_CHURNING_LOSS_CALCULATION_METHOD = python_net_import(
    "SMT.MastaAPI.Gears", "GearWindageAndChurningLossCalculationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearWindageAndChurningLossCalculationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearWindageAndChurningLossCalculationMethod._Cast_GearWindageAndChurningLossCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearWindageAndChurningLossCalculationMethod",)


class GearWindageAndChurningLossCalculationMethod(Enum):
    """GearWindageAndChurningLossCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_WINDAGE_AND_CHURNING_LOSS_CALCULATION_METHOD

    ISOTR_1417912001 = 0
    TAMAIS_METHOD = 1
    SCRIPT = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearWindageAndChurningLossCalculationMethod.__setattr__ = __enum_setattr
GearWindageAndChurningLossCalculationMethod.__delattr__ = __enum_delattr
