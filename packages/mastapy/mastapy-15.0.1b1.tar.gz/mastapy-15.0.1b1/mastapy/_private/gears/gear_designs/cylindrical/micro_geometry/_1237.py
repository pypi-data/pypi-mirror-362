"""MicroGeometryLeadToleranceChartView"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MICRO_GEOMETRY_LEAD_TOLERANCE_CHART_VIEW = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "MicroGeometryLeadToleranceChartView",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MicroGeometryLeadToleranceChartView")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryLeadToleranceChartView._Cast_MicroGeometryLeadToleranceChartView",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryLeadToleranceChartView",)


class MicroGeometryLeadToleranceChartView(Enum):
    """MicroGeometryLeadToleranceChartView

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MICRO_GEOMETRY_LEAD_TOLERANCE_CHART_VIEW

    TIP_TO_ROOT_VIEW = 0
    ROOT_TO_TIP_VIEW = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MicroGeometryLeadToleranceChartView.__setattr__ = __enum_setattr
MicroGeometryLeadToleranceChartView.__delattr__ = __enum_delattr
