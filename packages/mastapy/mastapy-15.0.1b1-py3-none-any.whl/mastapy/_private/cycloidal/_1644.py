"""DirectionOfMeasuredModifications"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DIRECTION_OF_MEASURED_MODIFICATIONS = python_net_import(
    "SMT.MastaAPI.Cycloidal", "DirectionOfMeasuredModifications"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DirectionOfMeasuredModifications")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DirectionOfMeasuredModifications._Cast_DirectionOfMeasuredModifications",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DirectionOfMeasuredModifications",)


class DirectionOfMeasuredModifications(Enum):
    """DirectionOfMeasuredModifications

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DIRECTION_OF_MEASURED_MODIFICATIONS

    NORMAL = 0
    RADIAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DirectionOfMeasuredModifications.__setattr__ = __enum_setattr
DirectionOfMeasuredModifications.__delattr__ = __enum_delattr
