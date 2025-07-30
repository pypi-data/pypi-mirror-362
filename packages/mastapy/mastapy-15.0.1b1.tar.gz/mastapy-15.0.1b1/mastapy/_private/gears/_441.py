"""WormType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WORM_TYPE = python_net_import("SMT.MastaAPI.Gears", "WormType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WormType")
    CastSelf = TypeVar("CastSelf", bound="WormType._Cast_WormType")


__docformat__ = "restructuredtext en"
__all__ = ("WormType",)


class WormType(Enum):
    """WormType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WORM_TYPE

    ZA = 0
    ZN = 1
    ZI = 2
    ZK = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WormType.__setattr__ = __enum_setattr
WormType.__delattr__ = __enum_delattr
