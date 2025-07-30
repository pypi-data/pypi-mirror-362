"""DIN3967ToleranceSeries"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DIN3967_TOLERANCE_SERIES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "DIN3967ToleranceSeries"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DIN3967ToleranceSeries")
    CastSelf = TypeVar(
        "CastSelf", bound="DIN3967ToleranceSeries._Cast_DIN3967ToleranceSeries"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DIN3967ToleranceSeries",)


class DIN3967ToleranceSeries(Enum):
    """DIN3967ToleranceSeries

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DIN3967_TOLERANCE_SERIES

    _21 = 21
    _22 = 22
    _23 = 23
    _24 = 24
    _25 = 25
    _26 = 26
    _27 = 27
    _28 = 28
    _29 = 29
    _30 = 30


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DIN3967ToleranceSeries.__setattr__ = __enum_setattr
DIN3967ToleranceSeries.__delattr__ = __enum_delattr
