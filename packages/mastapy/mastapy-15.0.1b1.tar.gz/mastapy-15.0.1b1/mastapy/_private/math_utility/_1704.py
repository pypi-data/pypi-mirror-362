"""ComplexMagnitudeMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COMPLEX_MAGNITUDE_METHOD = python_net_import(
    "SMT.MastaAPI.MathUtility", "ComplexMagnitudeMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ComplexMagnitudeMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="ComplexMagnitudeMethod._Cast_ComplexMagnitudeMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComplexMagnitudeMethod",)


class ComplexMagnitudeMethod(Enum):
    """ComplexMagnitudeMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COMPLEX_MAGNITUDE_METHOD

    PEAK_AMPLITUDE = 0
    PEAKTOPEAK_AMPLITUDE = 1
    RMS_AMPLITUDE = 2
    MAGNITUDE_OF_COMPLEX_MODULI = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ComplexMagnitudeMethod.__setattr__ = __enum_setattr
ComplexMagnitudeMethod.__delattr__ = __enum_delattr
