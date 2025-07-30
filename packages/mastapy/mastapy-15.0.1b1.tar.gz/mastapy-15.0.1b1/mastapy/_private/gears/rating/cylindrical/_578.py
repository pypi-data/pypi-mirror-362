"""ToothThicknesses"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TOOTH_THICKNESSES = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "ToothThicknesses"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ToothThicknesses")
    CastSelf = TypeVar("CastSelf", bound="ToothThicknesses._Cast_ToothThicknesses")


__docformat__ = "restructuredtext en"
__all__ = ("ToothThicknesses",)


class ToothThicknesses(Enum):
    """ToothThicknesses

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TOOTH_THICKNESSES

    DESIGN_ZERO_BACKLASH = 0
    MINIMUM = 1
    AVERAGE = 2
    MAXIMUM = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ToothThicknesses.__setattr__ = __enum_setattr
ToothThicknesses.__delattr__ = __enum_delattr
