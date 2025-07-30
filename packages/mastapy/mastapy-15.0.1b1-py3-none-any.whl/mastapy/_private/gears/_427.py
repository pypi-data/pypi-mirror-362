"""MicroGeometryModel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MICRO_GEOMETRY_MODEL = python_net_import("SMT.MastaAPI.Gears", "MicroGeometryModel")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MicroGeometryModel")
    CastSelf = TypeVar("CastSelf", bound="MicroGeometryModel._Cast_MicroGeometryModel")


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryModel",)


class MicroGeometryModel(Enum):
    """MicroGeometryModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MICRO_GEOMETRY_MODEL

    NONE = 0
    ESTIMATED_FROM_MACRO_GEOMETRY = 1
    SPECIFIED_MICRO_GEOMETRY = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MicroGeometryModel.__setattr__ = __enum_setattr
MicroGeometryModel.__delattr__ = __enum_delattr
