"""LubricationMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LUBRICATION_METHODS = python_net_import("SMT.MastaAPI.Gears", "LubricationMethods")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LubricationMethods")
    CastSelf = TypeVar("CastSelf", bound="LubricationMethods._Cast_LubricationMethods")


__docformat__ = "restructuredtext en"
__all__ = ("LubricationMethods",)


class LubricationMethods(Enum):
    """LubricationMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LUBRICATION_METHODS

    SPRAYINJECTION_LUBRICATION = 0
    DIP_LUBRICATION = 1
    SUBMERGED = 2
    ADDITIONAL_SPRAY_LUBRICATION = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LubricationMethods.__setattr__ = __enum_setattr
LubricationMethods.__delattr__ = __enum_delattr
