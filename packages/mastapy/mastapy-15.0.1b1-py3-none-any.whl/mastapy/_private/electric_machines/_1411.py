"""IronLossCoefficientSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_IRON_LOSS_COEFFICIENT_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "IronLossCoefficientSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="IronLossCoefficientSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="IronLossCoefficientSpecificationMethod._Cast_IronLossCoefficientSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("IronLossCoefficientSpecificationMethod",)


class IronLossCoefficientSpecificationMethod(Enum):
    """IronLossCoefficientSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _IRON_LOSS_COEFFICIENT_SPECIFICATION_METHOD

    SPECIFIED = 0
    OBTAINED_FROM_LOSS_CURVES = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


IronLossCoefficientSpecificationMethod.__setattr__ = __enum_setattr
IronLossCoefficientSpecificationMethod.__delattr__ = __enum_delattr
