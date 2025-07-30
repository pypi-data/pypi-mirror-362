"""BHCurveExtrapolationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BH_CURVE_EXTRAPOLATION_METHOD = python_net_import(
    "SMT.MastaAPI.Materials", "BHCurveExtrapolationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BHCurveExtrapolationMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="BHCurveExtrapolationMethod._Cast_BHCurveExtrapolationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BHCurveExtrapolationMethod",)


class BHCurveExtrapolationMethod(Enum):
    """BHCurveExtrapolationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BH_CURVE_EXTRAPOLATION_METHOD

    NONE = 0
    STRAIGHT_LINE = 1
    LAW_OF_APPROACH_TO_SATURATION = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BHCurveExtrapolationMethod.__setattr__ = __enum_setattr
BHCurveExtrapolationMethod.__delattr__ = __enum_delattr
