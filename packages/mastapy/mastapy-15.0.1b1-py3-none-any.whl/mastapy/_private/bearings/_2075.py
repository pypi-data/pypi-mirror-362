"""BearingCageMaterial"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_CAGE_MATERIAL = python_net_import(
    "SMT.MastaAPI.Bearings", "BearingCageMaterial"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingCageMaterial")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingCageMaterial._Cast_BearingCageMaterial"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingCageMaterial",)


class BearingCageMaterial(Enum):
    """BearingCageMaterial

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_CAGE_MATERIAL

    STEEL = 0
    BRASS = 1
    PLASTIC = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingCageMaterial.__setattr__ = __enum_setattr
BearingCageMaterial.__delattr__ = __enum_delattr
