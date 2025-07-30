"""ToothSlotStyle"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TOOTH_SLOT_STYLE = python_net_import("SMT.MastaAPI.ElectricMachines", "ToothSlotStyle")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ToothSlotStyle")
    CastSelf = TypeVar("CastSelf", bound="ToothSlotStyle._Cast_ToothSlotStyle")


__docformat__ = "restructuredtext en"
__all__ = ("ToothSlotStyle",)


class ToothSlotStyle(Enum):
    """ToothSlotStyle

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TOOTH_SLOT_STYLE

    PARALLEL_TOOTH = 0
    PARALLEL_SLOT = 1
    USERDEFINED = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ToothSlotStyle.__setattr__ = __enum_setattr
ToothSlotStyle.__delattr__ = __enum_delattr
