"""FillFactorSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FILL_FACTOR_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "FillFactorSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FillFactorSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FillFactorSpecificationMethod._Cast_FillFactorSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FillFactorSpecificationMethod",)


class FillFactorSpecificationMethod(Enum):
    """FillFactorSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FILL_FACTOR_SPECIFICATION_METHOD

    CALCULATED_FROM_WIRE_DIMENSIONS = 0
    SPECIFIED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FillFactorSpecificationMethod.__setattr__ = __enum_setattr
FillFactorSpecificationMethod.__delattr__ = __enum_delattr
