"""InternalClearanceClass"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INTERNAL_CLEARANCE_CLASS = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "InternalClearanceClass"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InternalClearanceClass")
    CastSelf = TypeVar(
        "CastSelf", bound="InternalClearanceClass._Cast_InternalClearanceClass"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InternalClearanceClass",)


class InternalClearanceClass(Enum):
    """InternalClearanceClass

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INTERNAL_CLEARANCE_CLASS

    GROUP_2 = 0
    GROUP_N = 1
    GROUP_3 = 2
    GROUP_4 = 3
    GROUP_5 = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


InternalClearanceClass.__setattr__ = __enum_setattr
InternalClearanceClass.__delattr__ = __enum_delattr
