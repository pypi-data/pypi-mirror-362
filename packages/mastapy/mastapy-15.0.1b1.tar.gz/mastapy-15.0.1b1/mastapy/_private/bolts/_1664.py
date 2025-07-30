"""HeadCapTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HEAD_CAP_TYPES = python_net_import("SMT.MastaAPI.Bolts", "HeadCapTypes")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HeadCapTypes")
    CastSelf = TypeVar("CastSelf", bound="HeadCapTypes._Cast_HeadCapTypes")


__docformat__ = "restructuredtext en"
__all__ = ("HeadCapTypes",)


class HeadCapTypes(Enum):
    """HeadCapTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HEAD_CAP_TYPES

    HEXAGONAL_HEAD = 0
    SOCKET_HEAD = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HeadCapTypes.__setattr__ = __enum_setattr
HeadCapTypes.__delattr__ = __enum_delattr
