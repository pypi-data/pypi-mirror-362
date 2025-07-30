"""SealLocation"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SEAL_LOCATION = python_net_import("SMT.MastaAPI.Bearings", "SealLocation")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SealLocation")
    CastSelf = TypeVar("CastSelf", bound="SealLocation._Cast_SealLocation")


__docformat__ = "restructuredtext en"
__all__ = ("SealLocation",)


class SealLocation(Enum):
    """SealLocation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SEAL_LOCATION

    NONE = 0
    ONE_SIDE = 1
    BOTH_SIDES = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SealLocation.__setattr__ = __enum_setattr
SealLocation.__delattr__ = __enum_delattr
