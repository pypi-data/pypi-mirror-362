"""RoundingMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ROUNDING_METHODS = python_net_import("SMT.MastaAPI.Utility", "RoundingMethods")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RoundingMethods")
    CastSelf = TypeVar("CastSelf", bound="RoundingMethods._Cast_RoundingMethods")


__docformat__ = "restructuredtext en"
__all__ = ("RoundingMethods",)


class RoundingMethods(Enum):
    """RoundingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ROUNDING_METHODS

    AUTO = 0
    SIGNIFICANT_FIGURES = 1
    DECIMAL_PLACES = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RoundingMethods.__setattr__ = __enum_setattr
RoundingMethods.__delattr__ = __enum_delattr
