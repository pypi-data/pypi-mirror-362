"""HobEdgeTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HOB_EDGE_TYPES = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "HobEdgeTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HobEdgeTypes")
    CastSelf = TypeVar("CastSelf", bound="HobEdgeTypes._Cast_HobEdgeTypes")


__docformat__ = "restructuredtext en"
__all__ = ("HobEdgeTypes",)


class HobEdgeTypes(Enum):
    """HobEdgeTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HOB_EDGE_TYPES

    ARC = 0
    CATMULLROM_SPLINE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HobEdgeTypes.__setattr__ = __enum_setattr
HobEdgeTypes.__delattr__ = __enum_delattr
