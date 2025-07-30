"""BearingRow"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_ROW = python_net_import("SMT.MastaAPI.Bearings", "BearingRow")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingRow")
    CastSelf = TypeVar("CastSelf", bound="BearingRow._Cast_BearingRow")


__docformat__ = "restructuredtext en"
__all__ = ("BearingRow",)


class BearingRow(Enum):
    """BearingRow

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_ROW

    LEFT = 0
    RIGHT = 1
    SINGLE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingRow.__setattr__ = __enum_setattr
BearingRow.__delattr__ = __enum_delattr
