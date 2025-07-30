"""HeadingType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HEADING_TYPE = python_net_import("SMT.MastaAPI.HTML", "HeadingType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HeadingType")
    CastSelf = TypeVar("CastSelf", bound="HeadingType._Cast_HeadingType")


__docformat__ = "restructuredtext en"
__all__ = ("HeadingType",)


class HeadingType(Enum):
    """HeadingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HEADING_TYPE

    VERY_SMALL = 0
    REGULAR = 1
    MEDIUM = 2
    LARGE = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HeadingType.__setattr__ = __enum_setattr
HeadingType.__delattr__ = __enum_delattr
