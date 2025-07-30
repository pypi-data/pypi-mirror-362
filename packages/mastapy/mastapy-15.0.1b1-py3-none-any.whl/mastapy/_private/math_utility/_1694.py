"""ExtrapolationOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_EXTRAPOLATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.MathUtility", "ExtrapolationOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ExtrapolationOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="ExtrapolationOptions._Cast_ExtrapolationOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExtrapolationOptions",)


class ExtrapolationOptions(Enum):
    """ExtrapolationOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _EXTRAPOLATION_OPTIONS

    FLAT = 0
    LINEAR = 1
    THROW_EXCEPTION = 2
    WRAP = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ExtrapolationOptions.__setattr__ = __enum_setattr
ExtrapolationOptions.__delattr__ = __enum_delattr
