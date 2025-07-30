"""BasicRackProfiles"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BASIC_RACK_PROFILES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "BasicRackProfiles"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BasicRackProfiles")
    CastSelf = TypeVar("CastSelf", bound="BasicRackProfiles._Cast_BasicRackProfiles")


__docformat__ = "restructuredtext en"
__all__ = ("BasicRackProfiles",)


class BasicRackProfiles(Enum):
    """BasicRackProfiles

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BASIC_RACK_PROFILES

    ISO_53_PROFILE_A = 0
    ISO_53_PROFILE_B = 1
    ISO_53_PROFILE_C = 2
    ISO_53_PROFILE_D = 3
    CUSTOM = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BasicRackProfiles.__setattr__ = __enum_setattr
BasicRackProfiles.__delattr__ = __enum_delattr
