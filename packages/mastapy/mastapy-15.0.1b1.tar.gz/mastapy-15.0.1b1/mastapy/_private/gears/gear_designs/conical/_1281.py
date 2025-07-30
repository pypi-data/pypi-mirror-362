"""CutterBladeType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CUTTER_BLADE_TYPE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "CutterBladeType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CutterBladeType")
    CastSelf = TypeVar("CastSelf", bound="CutterBladeType._Cast_CutterBladeType")


__docformat__ = "restructuredtext en"
__all__ = ("CutterBladeType",)


class CutterBladeType(Enum):
    """CutterBladeType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CUTTER_BLADE_TYPE

    STRAIGHT = 0
    CIRCULAR_ARC = 1
    PARABOLIC = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CutterBladeType.__setattr__ = __enum_setattr
CutterBladeType.__delattr__ = __enum_delattr
