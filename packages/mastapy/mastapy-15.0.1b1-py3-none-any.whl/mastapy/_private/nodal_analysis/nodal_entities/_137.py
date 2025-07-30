"""ShearAreaFactorMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SHEAR_AREA_FACTOR_METHOD = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "ShearAreaFactorMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShearAreaFactorMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="ShearAreaFactorMethod._Cast_ShearAreaFactorMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShearAreaFactorMethod",)


class ShearAreaFactorMethod(Enum):
    """ShearAreaFactorMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SHEAR_AREA_FACTOR_METHOD

    _109 = 0
    LINEAR_BETWEEN_109_SOLID_AND_2_THIN_WALLED = 1
    LINEAR_BETWEEN_1089_SOLID_AND_1053_THIN_WALLED = 2
    HOOGENBOOM_PAPER = 3
    EULERBERNOULLI = 4
    _1 = 5
    _2 = 6
    STEINBOECK = 7


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ShearAreaFactorMethod.__setattr__ = __enum_setattr
ShearAreaFactorMethod.__delattr__ = __enum_delattr
