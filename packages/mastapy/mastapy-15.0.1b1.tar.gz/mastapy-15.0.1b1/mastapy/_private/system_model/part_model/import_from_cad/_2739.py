"""HousedOrMounted"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HOUSED_OR_MOUNTED = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "HousedOrMounted"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HousedOrMounted")
    CastSelf = TypeVar("CastSelf", bound="HousedOrMounted._Cast_HousedOrMounted")


__docformat__ = "restructuredtext en"
__all__ = ("HousedOrMounted",)


class HousedOrMounted(Enum):
    """HousedOrMounted

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HOUSED_OR_MOUNTED

    HOUSED = 0
    MOUNTED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HousedOrMounted.__setattr__ = __enum_setattr
HousedOrMounted.__delattr__ = __enum_delattr
