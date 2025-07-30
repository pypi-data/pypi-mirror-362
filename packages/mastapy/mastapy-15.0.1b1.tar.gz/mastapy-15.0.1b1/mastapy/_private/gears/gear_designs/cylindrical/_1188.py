"""SpurGearLoadSharingCodes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPUR_GEAR_LOAD_SHARING_CODES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "SpurGearLoadSharingCodes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SpurGearLoadSharingCodes")
    CastSelf = TypeVar(
        "CastSelf", bound="SpurGearLoadSharingCodes._Cast_SpurGearLoadSharingCodes"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpurGearLoadSharingCodes",)


class SpurGearLoadSharingCodes(Enum):
    """SpurGearLoadSharingCodes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPUR_GEAR_LOAD_SHARING_CODES

    LOAD_AT_HPSTC = 0
    LOAD_AT_TIP = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SpurGearLoadSharingCodes.__setattr__ = __enum_setattr
SpurGearLoadSharingCodes.__delattr__ = __enum_delattr
