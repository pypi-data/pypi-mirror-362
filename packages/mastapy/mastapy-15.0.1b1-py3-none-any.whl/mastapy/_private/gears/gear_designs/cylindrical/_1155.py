"""DoubleAxisScaleAndRange"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DOUBLE_AXIS_SCALE_AND_RANGE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "DoubleAxisScaleAndRange"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DoubleAxisScaleAndRange")
    CastSelf = TypeVar(
        "CastSelf", bound="DoubleAxisScaleAndRange._Cast_DoubleAxisScaleAndRange"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DoubleAxisScaleAndRange",)


class DoubleAxisScaleAndRange(Enum):
    """DoubleAxisScaleAndRange

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DOUBLE_AXIS_SCALE_AND_RANGE

    MASTA_DEFAULT = 0
    EQUAL_SCALE = 1
    EQUAL_RANGE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DoubleAxisScaleAndRange.__setattr__ = __enum_setattr
DoubleAxisScaleAndRange.__delattr__ = __enum_delattr
