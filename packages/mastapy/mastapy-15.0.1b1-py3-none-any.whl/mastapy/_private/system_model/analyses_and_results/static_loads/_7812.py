"""ResetMicroGeometryOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RESET_MICRO_GEOMETRY_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ResetMicroGeometryOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ResetMicroGeometryOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="ResetMicroGeometryOptions._Cast_ResetMicroGeometryOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResetMicroGeometryOptions",)


class ResetMicroGeometryOptions(Enum):
    """ResetMicroGeometryOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RESET_MICRO_GEOMETRY_OPTIONS

    RESET_OPTIONS = 0
    RESET_TO_DESIGN_MICRO_GEOMETRY = 1
    RESET_TO_NO_MODIFICATION = 2
    COPY_TO_NEW_DESIGN_MICRO_GEOMETRY = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ResetMicroGeometryOptions.__setattr__ = __enum_setattr
ResetMicroGeometryOptions.__delattr__ = __enum_delattr
