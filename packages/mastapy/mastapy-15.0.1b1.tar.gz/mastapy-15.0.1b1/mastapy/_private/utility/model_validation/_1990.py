"""StatusItemSeverity"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_STATUS_ITEM_SEVERITY = python_net_import(
    "SMT.MastaAPI.Utility.ModelValidation", "StatusItemSeverity"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StatusItemSeverity")
    CastSelf = TypeVar("CastSelf", bound="StatusItemSeverity._Cast_StatusItemSeverity")


__docformat__ = "restructuredtext en"
__all__ = ("StatusItemSeverity",)


class StatusItemSeverity(Enum):
    """StatusItemSeverity

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _STATUS_ITEM_SEVERITY

    HEADER = 1
    INFORMATION = 16
    WARNING = 256
    ERROR = 4096


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


StatusItemSeverity.__setattr__ = __enum_setattr
StatusItemSeverity.__delattr__ = __enum_delattr
