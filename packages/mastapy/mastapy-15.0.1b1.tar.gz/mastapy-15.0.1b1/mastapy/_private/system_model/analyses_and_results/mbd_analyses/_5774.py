"""ShapeOfInitialAccelerationPeriodForRunUp"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SHAPE_OF_INITIAL_ACCELERATION_PERIOD_FOR_RUN_UP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "ShapeOfInitialAccelerationPeriodForRunUp",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShapeOfInitialAccelerationPeriodForRunUp")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShapeOfInitialAccelerationPeriodForRunUp._Cast_ShapeOfInitialAccelerationPeriodForRunUp",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShapeOfInitialAccelerationPeriodForRunUp",)


class ShapeOfInitialAccelerationPeriodForRunUp(Enum):
    """ShapeOfInitialAccelerationPeriodForRunUp

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SHAPE_OF_INITIAL_ACCELERATION_PERIOD_FOR_RUN_UP

    LINEAR = 0
    QUADRATIC = 1
    CUBIC = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ShapeOfInitialAccelerationPeriodForRunUp.__setattr__ = __enum_setattr
ShapeOfInitialAccelerationPeriodForRunUp.__delattr__ = __enum_delattr
