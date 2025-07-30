"""GeometryTypeForComponentImport"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEOMETRY_TYPE_FOR_COMPONENT_IMPORT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "GeometryTypeForComponentImport"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GeometryTypeForComponentImport")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeometryTypeForComponentImport._Cast_GeometryTypeForComponentImport",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryTypeForComponentImport",)


class GeometryTypeForComponentImport(Enum):
    """GeometryTypeForComponentImport

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEOMETRY_TYPE_FOR_COMPONENT_IMPORT

    CYLINDER = 0
    CONE = 1
    PLANE = 2
    TORUS = 3
    UNHANDLED_GEOMETRY = 4
    EDGE = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GeometryTypeForComponentImport.__setattr__ = __enum_setattr
GeometryTypeForComponentImport.__delattr__ = __enum_delattr
