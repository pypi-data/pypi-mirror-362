"""MountingPointSurfaceFinishes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MOUNTING_POINT_SURFACE_FINISHES = python_net_import(
    "SMT.MastaAPI.Bearings", "MountingPointSurfaceFinishes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MountingPointSurfaceFinishes")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountingPointSurfaceFinishes._Cast_MountingPointSurfaceFinishes",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountingPointSurfaceFinishes",)


class MountingPointSurfaceFinishes(Enum):
    """MountingPointSurfaceFinishes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MOUNTING_POINT_SURFACE_FINISHES

    ACCURATELY_GROUND = 0
    VERY_SMOOTH_TURNED_SURFACE = 1
    ACCURATELY_TURNED_SURFACE = 2
    MACHINE_REAMED = 3
    USERSPECIFIED = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MountingPointSurfaceFinishes.__setattr__ = __enum_setattr
MountingPointSurfaceFinishes.__delattr__ = __enum_delattr
