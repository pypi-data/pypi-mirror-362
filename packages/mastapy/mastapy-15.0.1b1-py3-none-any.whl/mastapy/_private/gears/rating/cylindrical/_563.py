"""DynamicFactorMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DYNAMIC_FACTOR_METHODS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "DynamicFactorMethods"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DynamicFactorMethods")
    CastSelf = TypeVar(
        "CastSelf", bound="DynamicFactorMethods._Cast_DynamicFactorMethods"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicFactorMethods",)


class DynamicFactorMethods(Enum):
    """DynamicFactorMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DYNAMIC_FACTOR_METHODS

    METHOD_B = 0
    METHOD_C = 1
    SELECT_AUTOMATICALLY = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DynamicFactorMethods.__setattr__ = __enum_setattr
DynamicFactorMethods.__delattr__ = __enum_delattr
