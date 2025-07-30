"""HelicalGearMicroGeometryOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HELICAL_GEAR_MICRO_GEOMETRY_OPTION = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336", "HelicalGearMicroGeometryOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HelicalGearMicroGeometryOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HelicalGearMicroGeometryOption._Cast_HelicalGearMicroGeometryOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HelicalGearMicroGeometryOption",)


class HelicalGearMicroGeometryOption(Enum):
    """HelicalGearMicroGeometryOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HELICAL_GEAR_MICRO_GEOMETRY_OPTION

    SUITABLE = 0
    BASED_ON_PRACTICAL_EXPERIENCE = 1
    NONE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HelicalGearMicroGeometryOption.__setattr__ = __enum_setattr
HelicalGearMicroGeometryOption.__delattr__ = __enum_delattr
