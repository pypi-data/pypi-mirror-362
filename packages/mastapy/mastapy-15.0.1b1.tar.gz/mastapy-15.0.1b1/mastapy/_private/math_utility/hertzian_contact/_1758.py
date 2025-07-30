"""HertzianContactDeflectionCalculationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HERTZIAN_CONTACT_DEFLECTION_CALCULATION_METHOD = python_net_import(
    "SMT.MastaAPI.MathUtility.HertzianContact",
    "HertzianContactDeflectionCalculationMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HertzianContactDeflectionCalculationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HertzianContactDeflectionCalculationMethod._Cast_HertzianContactDeflectionCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HertzianContactDeflectionCalculationMethod",)


class HertzianContactDeflectionCalculationMethod(Enum):
    """HertzianContactDeflectionCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HERTZIAN_CONTACT_DEFLECTION_CALCULATION_METHOD

    WEBER = 0
    SIMPLIFIED_WEBER = 1
    HOUPERT_VERSION_1 = 2
    HOUPERT_VERSION_2 = 3
    PALMGREN = 4
    MODIFIED_PALMGREN = 5
    LI = 6
    TRIPP = 7
    UMEZAWA = 8


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HertzianContactDeflectionCalculationMethod.__setattr__ = __enum_setattr
HertzianContactDeflectionCalculationMethod.__delattr__ = __enum_delattr
