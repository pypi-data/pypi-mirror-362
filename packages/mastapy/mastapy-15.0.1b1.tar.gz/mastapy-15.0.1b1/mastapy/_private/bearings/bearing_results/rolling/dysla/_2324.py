"""RevolutionsType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_REVOLUTIONS_TYPE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.Dysla", "RevolutionsType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RevolutionsType")
    CastSelf = TypeVar("CastSelf", bound="RevolutionsType._Cast_RevolutionsType")


__docformat__ = "restructuredtext en"
__all__ = ("RevolutionsType",)


class RevolutionsType(Enum):
    """RevolutionsType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _REVOLUTIONS_TYPE

    ELEMENT_REVOLUTIONS = 0
    RELATIVE_RING_REVOLUTIONS = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RevolutionsType.__setattr__ = __enum_setattr
RevolutionsType.__delattr__ = __enum_delattr
