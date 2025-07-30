"""CylindricalGearProfileModifications"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_PROFILE_MODIFICATIONS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearProfileModifications"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearProfileModifications")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearProfileModifications._Cast_CylindricalGearProfileModifications",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearProfileModifications",)


class CylindricalGearProfileModifications(Enum):
    """CylindricalGearProfileModifications

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CYLINDRICAL_GEAR_PROFILE_MODIFICATIONS

    NONE = 0
    HIGH_LOAD = 1
    SMOOTH_MESHING = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CylindricalGearProfileModifications.__setattr__ = __enum_setattr
CylindricalGearProfileModifications.__delattr__ = __enum_delattr
