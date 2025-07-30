"""ManufacturingTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MANUFACTURING_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "ManufacturingTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ManufacturingTypes")
    CastSelf = TypeVar("CastSelf", bound="ManufacturingTypes._Cast_ManufacturingTypes")


__docformat__ = "restructuredtext en"
__all__ = ("ManufacturingTypes",)


class ManufacturingTypes(Enum):
    """ManufacturingTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MANUFACTURING_TYPES

    BROACHING = 0
    HOBBING = 1
    GEAR_SHAPING = 2
    COLD_ROLLING = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ManufacturingTypes.__setattr__ = __enum_setattr
ManufacturingTypes.__delattr__ = __enum_delattr
