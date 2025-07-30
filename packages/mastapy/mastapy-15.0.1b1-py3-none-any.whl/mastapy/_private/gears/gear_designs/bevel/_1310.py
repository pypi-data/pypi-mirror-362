"""ToothThicknessSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TOOTH_THICKNESS_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "ToothThicknessSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ToothThicknessSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothThicknessSpecificationMethod._Cast_ToothThicknessSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothThicknessSpecificationMethod",)


class ToothThicknessSpecificationMethod(Enum):
    """ToothThicknessSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TOOTH_THICKNESS_SPECIFICATION_METHOD

    CIRCULAR_THICKNESS_FACTOR = 0
    WHEEL_MEAN_SLOT_WIDTH = 1
    WHEEL_FINISH_CUTTER_POINT_WIDTH = 2
    PINION_MEAN_TRANSVERSE_CIRCULAR_THICKNESS = 3
    PINION_OUTER_TRANSVERSE_CIRCULAR_THICKNESS = 4
    EQUAL_STRESS = 5
    EQUAL_LIFE = 6
    STRENGTH_FACTOR = 7


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ToothThicknessSpecificationMethod.__setattr__ = __enum_setattr
ToothThicknessSpecificationMethod.__delattr__ = __enum_delattr
