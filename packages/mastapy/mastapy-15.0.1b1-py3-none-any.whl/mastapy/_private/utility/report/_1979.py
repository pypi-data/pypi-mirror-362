"""FontWeight"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FONT_WEIGHT = python_net_import("SMT.MastaAPI.Utility.Report", "FontWeight")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FontWeight")
    CastSelf = TypeVar("CastSelf", bound="FontWeight._Cast_FontWeight")


__docformat__ = "restructuredtext en"
__all__ = ("FontWeight",)


class FontWeight(Enum):
    """FontWeight

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FONT_WEIGHT

    NORMAL = 0
    BOLD = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FontWeight.__setattr__ = __enum_setattr
FontWeight.__delattr__ = __enum_delattr
