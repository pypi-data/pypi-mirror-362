"""TopremEntryType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TOPREM_ENTRY_TYPE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "TopremEntryType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TopremEntryType")
    CastSelf = TypeVar("CastSelf", bound="TopremEntryType._Cast_TopremEntryType")


__docformat__ = "restructuredtext en"
__all__ = ("TopremEntryType",)


class TopremEntryType(Enum):
    """TopremEntryType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TOPREM_ENTRY_TYPE

    TOPREM_LETTER = 0
    VALUES = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TopremEntryType.__setattr__ = __enum_setattr
TopremEntryType.__delattr__ = __enum_delattr
