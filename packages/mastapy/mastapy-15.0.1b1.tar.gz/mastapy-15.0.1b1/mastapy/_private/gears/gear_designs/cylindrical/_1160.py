"""GeometrySpecificationType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEOMETRY_SPECIFICATION_TYPE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "GeometrySpecificationType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GeometrySpecificationType")
    CastSelf = TypeVar(
        "CastSelf", bound="GeometrySpecificationType._Cast_GeometrySpecificationType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometrySpecificationType",)


class GeometrySpecificationType(Enum):
    """GeometrySpecificationType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEOMETRY_SPECIFICATION_TYPE

    BASIC_RACK = 0
    PINION_TYPE_CUTTER = 1
    EXISTING_CUTTER_OBSOLETE = 2
    MANUFACTURING_CONFIGURATION = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GeometrySpecificationType.__setattr__ = __enum_setattr
GeometrySpecificationType.__delattr__ = __enum_delattr
