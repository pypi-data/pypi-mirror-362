"""BeltDriveType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BELT_DRIVE_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDriveType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BeltDriveType")
    CastSelf = TypeVar("CastSelf", bound="BeltDriveType._Cast_BeltDriveType")


__docformat__ = "restructuredtext en"
__all__ = ("BeltDriveType",)


class BeltDriveType(Enum):
    """BeltDriveType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BELT_DRIVE_TYPE

    PUSHBELT = 0
    PULLBELT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BeltDriveType.__setattr__ = __enum_setattr
BeltDriveType.__delattr__ = __enum_delattr
