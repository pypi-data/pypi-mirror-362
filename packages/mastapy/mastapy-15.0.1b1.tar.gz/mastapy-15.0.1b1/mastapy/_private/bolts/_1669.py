"""StandardSizes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_STANDARD_SIZES = python_net_import("SMT.MastaAPI.Bolts", "StandardSizes")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StandardSizes")
    CastSelf = TypeVar("CastSelf", bound="StandardSizes._Cast_StandardSizes")


__docformat__ = "restructuredtext en"
__all__ = ("StandardSizes",)


class StandardSizes(Enum):
    """StandardSizes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _STANDARD_SIZES

    NON_STANDARD_SIZE = 0
    M4 = 4
    M5 = 5
    M6 = 6
    M7 = 7
    M8 = 8
    M9 = 9
    M10 = 10
    M12 = 12
    M14 = 14
    M16 = 16
    M18 = 18
    M20 = 20
    M22 = 22
    M24 = 24
    M27 = 27
    M30 = 30
    M33 = 33
    M36 = 36
    M39 = 39


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


StandardSizes.__setattr__ = __enum_setattr
StandardSizes.__delattr__ = __enum_delattr
