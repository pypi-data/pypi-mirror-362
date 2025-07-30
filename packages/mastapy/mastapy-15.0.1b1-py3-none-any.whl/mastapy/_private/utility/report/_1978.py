"""FontStyle"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FONT_STYLE = python_net_import("SMT.MastaAPI.Utility.Report", "FontStyle")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FontStyle")
    CastSelf = TypeVar("CastSelf", bound="FontStyle._Cast_FontStyle")


__docformat__ = "restructuredtext en"
__all__ = ("FontStyle",)


class FontStyle(Enum):
    """FontStyle

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FONT_STYLE

    NORMAL = 0
    ITALIC = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FontStyle.__setattr__ = __enum_setattr
FontStyle.__delattr__ = __enum_delattr
