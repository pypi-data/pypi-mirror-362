"""NotchShape"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_NOTCH_SHAPE = python_net_import("SMT.MastaAPI.ElectricMachines", "NotchShape")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NotchShape")
    CastSelf = TypeVar("CastSelf", bound="NotchShape._Cast_NotchShape")


__docformat__ = "restructuredtext en"
__all__ = ("NotchShape",)


class NotchShape(Enum):
    """NotchShape

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _NOTCH_SHAPE

    TYPE_1 = 0
    TYPE_2 = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


NotchShape.__setattr__ = __enum_setattr
NotchShape.__delattr__ = __enum_delattr
