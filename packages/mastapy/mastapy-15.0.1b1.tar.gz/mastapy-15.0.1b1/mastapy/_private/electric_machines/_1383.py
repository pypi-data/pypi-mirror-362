"""DoubleLayerWindingSlotPositions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DOUBLE_LAYER_WINDING_SLOT_POSITIONS = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "DoubleLayerWindingSlotPositions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DoubleLayerWindingSlotPositions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DoubleLayerWindingSlotPositions._Cast_DoubleLayerWindingSlotPositions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DoubleLayerWindingSlotPositions",)


class DoubleLayerWindingSlotPositions(Enum):
    """DoubleLayerWindingSlotPositions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DOUBLE_LAYER_WINDING_SLOT_POSITIONS

    RIGHTLEFT = 0
    TOPBOTTOM = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DoubleLayerWindingSlotPositions.__setattr__ = __enum_setattr
DoubleLayerWindingSlotPositions.__delattr__ = __enum_delattr
