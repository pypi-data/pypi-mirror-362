"""HeadingSize"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HEADING_SIZE = python_net_import("SMT.MastaAPI.Utility.Report", "HeadingSize")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HeadingSize")
    CastSelf = TypeVar("CastSelf", bound="HeadingSize._Cast_HeadingSize")


__docformat__ = "restructuredtext en"
__all__ = ("HeadingSize",)


class HeadingSize(Enum):
    """HeadingSize

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HEADING_SIZE

    REGULAR = 0
    MEDIUM = 1
    LARGE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HeadingSize.__setattr__ = __enum_setattr
HeadingSize.__delattr__ = __enum_delattr
