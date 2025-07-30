"""ProfileToothDrawingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PROFILE_TOOTH_DRAWING_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ProfileToothDrawingMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ProfileToothDrawingMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="ProfileToothDrawingMethod._Cast_ProfileToothDrawingMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfileToothDrawingMethod",)


class ProfileToothDrawingMethod(Enum):
    """ProfileToothDrawingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PROFILE_TOOTH_DRAWING_METHOD

    DRAW_TO_TIP_DIAMETER = 0
    DRAW_TO_ROOT_DIAMETER = 1
    DRAW_TO_REFERENCE_DIAMETER = 2
    DRAW_TO_ROOT_AND_TIP_DIAMETER = 3
    DONT_DRAW_GEAR = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ProfileToothDrawingMethod.__setattr__ = __enum_setattr
ProfileToothDrawingMethod.__delattr__ = __enum_delattr
