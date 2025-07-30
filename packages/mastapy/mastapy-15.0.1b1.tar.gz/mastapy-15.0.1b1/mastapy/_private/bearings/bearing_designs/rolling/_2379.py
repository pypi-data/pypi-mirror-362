"""SleeveType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SLEEVE_TYPE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "SleeveType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SleeveType")
    CastSelf = TypeVar("CastSelf", bound="SleeveType._Cast_SleeveType")


__docformat__ = "restructuredtext en"
__all__ = ("SleeveType",)


class SleeveType(Enum):
    """SleeveType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SLEEVE_TYPE

    NONE = 0
    WITHDRAWAL = 1
    ADAPTER = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SleeveType.__setattr__ = __enum_setattr
SleeveType.__delattr__ = __enum_delattr
