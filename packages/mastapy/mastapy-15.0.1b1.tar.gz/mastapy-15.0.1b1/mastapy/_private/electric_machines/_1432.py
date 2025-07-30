"""RotorType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ROTOR_TYPE = python_net_import("SMT.MastaAPI.ElectricMachines", "RotorType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RotorType")
    CastSelf = TypeVar("CastSelf", bound="RotorType._Cast_RotorType")


__docformat__ = "restructuredtext en"
__all__ = ("RotorType",)


class RotorType(Enum):
    """RotorType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ROTOR_TYPE

    VSHAPED = 0
    USHAPED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RotorType.__setattr__ = __enum_setattr
RotorType.__delattr__ = __enum_delattr
