"""DrawDefiningGearOrBoth"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DRAW_DEFINING_GEAR_OR_BOTH = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry", "DrawDefiningGearOrBoth"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DrawDefiningGearOrBoth")
    CastSelf = TypeVar(
        "CastSelf", bound="DrawDefiningGearOrBoth._Cast_DrawDefiningGearOrBoth"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DrawDefiningGearOrBoth",)


class DrawDefiningGearOrBoth(Enum):
    """DrawDefiningGearOrBoth

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DRAW_DEFINING_GEAR_OR_BOTH

    DEFINING_GEAR = 0
    BOTH = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DrawDefiningGearOrBoth.__setattr__ = __enum_setattr
DrawDefiningGearOrBoth.__delattr__ = __enum_delattr
