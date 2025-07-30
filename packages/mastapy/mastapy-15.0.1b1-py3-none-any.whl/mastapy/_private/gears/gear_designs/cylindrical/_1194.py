"""TipAlterationCoefficientMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TIP_ALTERATION_COEFFICIENT_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "TipAlterationCoefficientMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TipAlterationCoefficientMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TipAlterationCoefficientMethod._Cast_TipAlterationCoefficientMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TipAlterationCoefficientMethod",)


class TipAlterationCoefficientMethod(Enum):
    """TipAlterationCoefficientMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TIP_ALTERATION_COEFFICIENT_METHOD

    USERSPECIFIED = 0
    B = 1
    C = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TipAlterationCoefficientMethod.__setattr__ = __enum_setattr
TipAlterationCoefficientMethod.__delattr__ = __enum_delattr
