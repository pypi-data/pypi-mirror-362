"""SectionEnd"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SECTION_END = python_net_import("SMT.MastaAPI.NodalAnalysis", "SectionEnd")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SectionEnd")
    CastSelf = TypeVar("CastSelf", bound="SectionEnd._Cast_SectionEnd")


__docformat__ = "restructuredtext en"
__all__ = ("SectionEnd",)


class SectionEnd(Enum):
    """SectionEnd

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SECTION_END

    LEFT = 0
    RIGHT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SectionEnd.__setattr__ = __enum_setattr
SectionEnd.__delattr__ = __enum_delattr
