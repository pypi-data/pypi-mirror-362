"""BearingProtectionLevel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_PROTECTION_LEVEL = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "BearingProtectionLevel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingProtectionLevel")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingProtectionLevel._Cast_BearingProtectionLevel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingProtectionLevel",)


class BearingProtectionLevel(Enum):
    """BearingProtectionLevel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_PROTECTION_LEVEL

    NONE = 0
    INTERNAL_GEOMETRY_HIDDEN = 1
    INTERNAL_GEOMETRY_AND_ADVANCED_BEARING_RESULTS_HIDDEN = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingProtectionLevel.__setattr__ = __enum_setattr
BearingProtectionLevel.__delattr__ = __enum_delattr
