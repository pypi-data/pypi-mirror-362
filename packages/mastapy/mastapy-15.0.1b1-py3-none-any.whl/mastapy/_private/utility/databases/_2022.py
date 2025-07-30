"""ConnectionState"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONNECTION_STATE = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "ConnectionState"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConnectionState")
    CastSelf = TypeVar("CastSelf", bound="ConnectionState._Cast_ConnectionState")


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionState",)


class ConnectionState(Enum):
    """ConnectionState

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONNECTION_STATE

    CLOSED = 0
    OPEN = 1
    CONNECTING = 2
    EXECUTING = 4
    FETCHING = 8
    BROKEN = 16


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ConnectionState.__setattr__ = __enum_setattr
ConnectionState.__delattr__ = __enum_delattr
