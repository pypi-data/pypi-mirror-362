"""FESurfaceDrawingOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FE_SURFACE_DRAWING_OPTION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FESurfaceDrawingOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FESurfaceDrawingOption")
    CastSelf = TypeVar(
        "CastSelf", bound="FESurfaceDrawingOption._Cast_FESurfaceDrawingOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESurfaceDrawingOption",)


class FESurfaceDrawingOption(Enum):
    """FESurfaceDrawingOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FE_SURFACE_DRAWING_OPTION

    NONE = 0
    TRANSPARENT = 1
    SOLID = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FESurfaceDrawingOption.__setattr__ = __enum_setattr
FESurfaceDrawingOption.__delattr__ = __enum_delattr
