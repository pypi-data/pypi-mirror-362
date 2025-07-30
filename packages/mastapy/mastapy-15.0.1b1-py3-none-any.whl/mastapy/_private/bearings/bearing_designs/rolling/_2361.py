"""DiameterSeries"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DIAMETER_SERIES = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "DiameterSeries"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DiameterSeries")
    CastSelf = TypeVar("CastSelf", bound="DiameterSeries._Cast_DiameterSeries")


__docformat__ = "restructuredtext en"
__all__ = ("DiameterSeries",)


class DiameterSeries(Enum):
    """DiameterSeries

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DIAMETER_SERIES

    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _7 = 7
    _8 = 8
    _9 = 9


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DiameterSeries.__setattr__ = __enum_setattr
DiameterSeries.__delattr__ = __enum_delattr
