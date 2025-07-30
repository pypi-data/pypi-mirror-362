"""LargerOrSmaller"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LARGER_OR_SMALLER = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "LargerOrSmaller"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LargerOrSmaller")
    CastSelf = TypeVar("CastSelf", bound="LargerOrSmaller._Cast_LargerOrSmaller")


__docformat__ = "restructuredtext en"
__all__ = ("LargerOrSmaller",)


class LargerOrSmaller(Enum):
    """LargerOrSmaller

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LARGER_OR_SMALLER

    LARGER_VALUES = 0
    SMALLER_VALUES = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LargerOrSmaller.__setattr__ = __enum_setattr
LargerOrSmaller.__delattr__ = __enum_delattr
