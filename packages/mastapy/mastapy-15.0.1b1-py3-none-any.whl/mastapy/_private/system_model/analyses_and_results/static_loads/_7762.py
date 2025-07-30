"""GearMeshTEOrderType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_MESH_TE_ORDER_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearMeshTEOrderType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearMeshTEOrderType")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshTEOrderType._Cast_GearMeshTEOrderType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshTEOrderType",)


class GearMeshTEOrderType(Enum):
    """GearMeshTEOrderType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_MESH_TE_ORDER_TYPE

    ORDERS_WITH_RESPECT_TO_PRIMARY_MESH_ORDER = 0
    ORDERS_WITH_RESPECT_TO_REFERENCE_SHAFT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearMeshTEOrderType.__setattr__ = __enum_setattr
GearMeshTEOrderType.__delattr__ = __enum_delattr
