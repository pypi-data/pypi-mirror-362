"""GeometryModellerDimensionType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEOMETRY_MODELLER_DIMENSION_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "GeometryModellerDimensionType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GeometryModellerDimensionType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeometryModellerDimensionType._Cast_GeometryModellerDimensionType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryModellerDimensionType",)


class GeometryModellerDimensionType(Enum):
    """GeometryModellerDimensionType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEOMETRY_MODELLER_DIMENSION_TYPE

    UNITLESS = 0
    ANGLE = 1
    LENGTH = 2
    COUNT = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GeometryModellerDimensionType.__setattr__ = __enum_setattr
GeometryModellerDimensionType.__delattr__ = __enum_delattr
