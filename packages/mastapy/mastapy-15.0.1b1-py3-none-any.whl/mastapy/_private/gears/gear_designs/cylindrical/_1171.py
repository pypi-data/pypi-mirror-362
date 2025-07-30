"""MicroGeometryConvention"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MICRO_GEOMETRY_CONVENTION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "MicroGeometryConvention"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MicroGeometryConvention")
    CastSelf = TypeVar(
        "CastSelf", bound="MicroGeometryConvention._Cast_MicroGeometryConvention"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryConvention",)


class MicroGeometryConvention(Enum):
    """MicroGeometryConvention

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MICRO_GEOMETRY_CONVENTION

    MASTA_DEFAULT_MATERIAL = 0
    LDP = 1
    ISOAGMADINVDIVDE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MicroGeometryConvention.__setattr__ = __enum_setattr
MicroGeometryConvention.__delattr__ = __enum_delattr
