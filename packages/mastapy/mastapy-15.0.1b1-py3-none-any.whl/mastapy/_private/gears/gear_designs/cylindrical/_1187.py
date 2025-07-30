"""ShaperEdgeTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SHAPER_EDGE_TYPES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ShaperEdgeTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaperEdgeTypes")
    CastSelf = TypeVar("CastSelf", bound="ShaperEdgeTypes._Cast_ShaperEdgeTypes")


__docformat__ = "restructuredtext en"
__all__ = ("ShaperEdgeTypes",)


class ShaperEdgeTypes(Enum):
    """ShaperEdgeTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SHAPER_EDGE_TYPES

    SINGLE_CIRCLE = 0
    CATMULLROM_SPLINE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ShaperEdgeTypes.__setattr__ = __enum_setattr
ShaperEdgeTypes.__delattr__ = __enum_delattr
