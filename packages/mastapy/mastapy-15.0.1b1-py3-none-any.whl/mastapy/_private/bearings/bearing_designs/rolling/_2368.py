"""HeightSeries"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HEIGHT_SERIES = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "HeightSeries"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HeightSeries")
    CastSelf = TypeVar("CastSelf", bound="HeightSeries._Cast_HeightSeries")


__docformat__ = "restructuredtext en"
__all__ = ("HeightSeries",)


class HeightSeries(Enum):
    """HeightSeries

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HEIGHT_SERIES

    _1 = 1
    _7 = 7
    _9 = 9


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HeightSeries.__setattr__ = __enum_setattr
HeightSeries.__delattr__ = __enum_delattr
