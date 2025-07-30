"""WheelFormatMachineTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WHEEL_FORMAT_MACHINE_TYPES = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "WheelFormatMachineTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WheelFormatMachineTypes")
    CastSelf = TypeVar(
        "CastSelf", bound="WheelFormatMachineTypes._Cast_WheelFormatMachineTypes"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WheelFormatMachineTypes",)


class WheelFormatMachineTypes(Enum):
    """WheelFormatMachineTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WHEEL_FORMAT_MACHINE_TYPES

    COMPATIBLE_WITH_NO608_609_610 = 0
    COMPATIBLE_WITH_NO606_607 = 1
    UNKNOWN = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WheelFormatMachineTypes.__setattr__ = __enum_setattr
WheelFormatMachineTypes.__delattr__ = __enum_delattr
