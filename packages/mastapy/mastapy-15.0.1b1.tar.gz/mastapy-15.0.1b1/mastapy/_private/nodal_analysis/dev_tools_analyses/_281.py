"""FESurfaceAndNonDeformedDrawingOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FE_SURFACE_AND_NON_DEFORMED_DRAWING_OPTION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses",
    "FESurfaceAndNonDeformedDrawingOption",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FESurfaceAndNonDeformedDrawingOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESurfaceAndNonDeformedDrawingOption._Cast_FESurfaceAndNonDeformedDrawingOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESurfaceAndNonDeformedDrawingOption",)


class FESurfaceAndNonDeformedDrawingOption(Enum):
    """FESurfaceAndNonDeformedDrawingOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FE_SURFACE_AND_NON_DEFORMED_DRAWING_OPTION

    NONE = 0
    TRANSPARENT_DEFORMED = 1
    SOLID_DEFORMED = 2
    TRANSPARENT_DEFORMEDTRANSPARENT_NONDEFORMED = 3
    SOLID_DEFORMEDTRANSPARENT_NONDEFORMED = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FESurfaceAndNonDeformedDrawingOption.__setattr__ = __enum_setattr
FESurfaceAndNonDeformedDrawingOption.__delattr__ = __enum_delattr
