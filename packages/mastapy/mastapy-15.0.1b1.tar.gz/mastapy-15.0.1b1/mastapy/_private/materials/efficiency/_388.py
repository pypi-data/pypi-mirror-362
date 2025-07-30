"""OilPumpDriveType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_OIL_PUMP_DRIVE_TYPE = python_net_import(
    "SMT.MastaAPI.Materials.Efficiency", "OilPumpDriveType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OilPumpDriveType")
    CastSelf = TypeVar("CastSelf", bound="OilPumpDriveType._Cast_OilPumpDriveType")


__docformat__ = "restructuredtext en"
__all__ = ("OilPumpDriveType",)


class OilPumpDriveType(Enum):
    """OilPumpDriveType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _OIL_PUMP_DRIVE_TYPE

    MECHANICAL = 0
    ELECTRICAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


OilPumpDriveType.__setattr__ = __enum_setattr
OilPumpDriveType.__delattr__ = __enum_delattr
