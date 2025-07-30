"""BoltTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BOLT_TYPES = python_net_import("SMT.MastaAPI.Bolts", "BoltTypes")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BoltTypes")
    CastSelf = TypeVar("CastSelf", bound="BoltTypes._Cast_BoltTypes")


__docformat__ = "restructuredtext en"
__all__ = ("BoltTypes",)


class BoltTypes(Enum):
    """BoltTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BOLT_TYPES

    THROUGH_BOLTED_JOINT = 0
    TAPPED_THREAD_JOINT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BoltTypes.__setattr__ = __enum_setattr
BoltTypes.__delattr__ = __enum_delattr
