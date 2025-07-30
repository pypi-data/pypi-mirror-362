"""BoltShankType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BOLT_SHANK_TYPE = python_net_import("SMT.MastaAPI.Bolts", "BoltShankType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BoltShankType")
    CastSelf = TypeVar("CastSelf", bound="BoltShankType._Cast_BoltShankType")


__docformat__ = "restructuredtext en"
__all__ = ("BoltShankType",)


class BoltShankType(Enum):
    """BoltShankType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BOLT_SHANK_TYPE

    SHANKED = 0
    NECKED_DOWN = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BoltShankType.__setattr__ = __enum_setattr
BoltShankType.__delattr__ = __enum_delattr
