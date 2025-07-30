"""ResidualStressCalculationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RESIDUAL_STRESS_CALCULATION_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ResidualStressCalculationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ResidualStressCalculationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ResidualStressCalculationMethod._Cast_ResidualStressCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResidualStressCalculationMethod",)


class ResidualStressCalculationMethod(Enum):
    """ResidualStressCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RESIDUAL_STRESS_CALCULATION_METHOD

    MACKALDENER = 0
    LANG = 1
    MULLER_ET_AL = 2
    USERSPECIFIED = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ResidualStressCalculationMethod.__setattr__ = __enum_setattr
ResidualStressCalculationMethod.__delattr__ = __enum_delattr
