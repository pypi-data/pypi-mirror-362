"""MicroGeometryDefinitionMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MICRO_GEOMETRY_DEFINITION_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving",
    "MicroGeometryDefinitionMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MicroGeometryDefinitionMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryDefinitionMethod._Cast_MicroGeometryDefinitionMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryDefinitionMethod",)


class MicroGeometryDefinitionMethod(Enum):
    """MicroGeometryDefinitionMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MICRO_GEOMETRY_DEFINITION_METHOD

    NORMAL_TO_INVOLUTE = 0
    ARC_LENGTH = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MicroGeometryDefinitionMethod.__setattr__ = __enum_setattr
MicroGeometryDefinitionMethod.__delattr__ = __enum_delattr
