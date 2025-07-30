"""JournalBearingType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_JOURNAL_BEARING_TYPE = python_net_import("SMT.MastaAPI.Bearings", "JournalBearingType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="JournalBearingType")
    CastSelf = TypeVar("CastSelf", bound="JournalBearingType._Cast_JournalBearingType")


__docformat__ = "restructuredtext en"
__all__ = ("JournalBearingType",)


class JournalBearingType(Enum):
    """JournalBearingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _JOURNAL_BEARING_TYPE

    PLAIN_OIL_FED = 0
    PLAIN_GREASE_FILLED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


JournalBearingType.__setattr__ = __enum_setattr
JournalBearingType.__delattr__ = __enum_delattr
