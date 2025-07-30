"""CalculationMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CALCULATION_METHODS = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits", "CalculationMethods"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CalculationMethods")
    CastSelf = TypeVar("CastSelf", bound="CalculationMethods._Cast_CalculationMethods")


__docformat__ = "restructuredtext en"
__all__ = ("CalculationMethods",)


class CalculationMethods(Enum):
    """CalculationMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CALCULATION_METHODS

    SPECIFY_PRESSURE = 0
    SPECIFY_INTERFERENCE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CalculationMethods.__setattr__ = __enum_setattr
CalculationMethods.__delattr__ = __enum_delattr
