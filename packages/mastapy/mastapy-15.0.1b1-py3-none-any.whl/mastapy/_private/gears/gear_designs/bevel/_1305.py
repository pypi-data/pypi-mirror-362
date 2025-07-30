"""EdgeRadiusType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_EDGE_RADIUS_TYPE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "EdgeRadiusType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="EdgeRadiusType")
    CastSelf = TypeVar("CastSelf", bound="EdgeRadiusType._Cast_EdgeRadiusType")


__docformat__ = "restructuredtext en"
__all__ = ("EdgeRadiusType",)


class EdgeRadiusType(Enum):
    """EdgeRadiusType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _EDGE_RADIUS_TYPE

    USERSPECIFIED = 0
    CALCULATED_MAXIMUM = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


EdgeRadiusType.__setattr__ = __enum_setattr
EdgeRadiusType.__delattr__ = __enum_delattr
