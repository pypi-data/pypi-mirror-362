"""FaceGearDiameterFaceWidthSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FACE_GEAR_DIAMETER_FACE_WIDTH_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Face",
    "FaceGearDiameterFaceWidthSpecificationMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FaceGearDiameterFaceWidthSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FaceGearDiameterFaceWidthSpecificationMethod._Cast_FaceGearDiameterFaceWidthSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearDiameterFaceWidthSpecificationMethod",)


class FaceGearDiameterFaceWidthSpecificationMethod(Enum):
    """FaceGearDiameterFaceWidthSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FACE_GEAR_DIAMETER_FACE_WIDTH_SPECIFICATION_METHOD

    FACE_WIDTH_AND_FACE_WIDTH_OFFSET = 0
    INNER_AND_OUTER_DIAMETER = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FaceGearDiameterFaceWidthSpecificationMethod.__setattr__ = __enum_setattr
FaceGearDiameterFaceWidthSpecificationMethod.__delattr__ = __enum_delattr
