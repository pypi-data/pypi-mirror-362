"""ToothProportionsInputMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TOOTH_PROPORTIONS_INPUT_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "ToothProportionsInputMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ToothProportionsInputMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothProportionsInputMethod._Cast_ToothProportionsInputMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothProportionsInputMethod",)


class ToothProportionsInputMethod(Enum):
    """ToothProportionsInputMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TOOTH_PROPORTIONS_INPUT_METHOD

    DIRECT_DIMENSIONAL_INPUT = 0
    ADDENDUMDEPTH_FACTORS = 1
    GLEASON_FACTORS_OLD = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ToothProportionsInputMethod.__setattr__ = __enum_setattr
ToothProportionsInputMethod.__delattr__ = __enum_delattr
