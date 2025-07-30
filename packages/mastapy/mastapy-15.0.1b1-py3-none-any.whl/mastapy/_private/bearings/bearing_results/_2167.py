"""PreloadType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PRELOAD_TYPE = python_net_import("SMT.MastaAPI.Bearings.BearingResults", "PreloadType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PreloadType")
    CastSelf = TypeVar("CastSelf", bound="PreloadType._Cast_PreloadType")


__docformat__ = "restructuredtext en"
__all__ = ("PreloadType",)


class PreloadType(Enum):
    """PreloadType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PRELOAD_TYPE

    NONE = 0
    SOLID_PRELOAD = 1
    SPRING_PRELOAD = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PreloadType.__setattr__ = __enum_setattr
PreloadType.__delattr__ = __enum_delattr
