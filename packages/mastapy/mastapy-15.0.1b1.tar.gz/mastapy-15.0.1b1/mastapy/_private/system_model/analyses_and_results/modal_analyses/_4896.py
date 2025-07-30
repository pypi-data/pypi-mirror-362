"""DynamicsResponse3DChartType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DYNAMICS_RESPONSE_3D_CHART_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "DynamicsResponse3DChartType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DynamicsResponse3DChartType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DynamicsResponse3DChartType._Cast_DynamicsResponse3DChartType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicsResponse3DChartType",)


class DynamicsResponse3DChartType(Enum):
    """DynamicsResponse3DChartType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DYNAMICS_RESPONSE_3D_CHART_TYPE

    WATERFALL_FREQUENCY_AND_SPEED = 0
    ORDER_MAP_ORDER_AND_SPEED = 1
    TORQUE_MAP = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DynamicsResponse3DChartType.__setattr__ = __enum_setattr
DynamicsResponse3DChartType.__delattr__ = __enum_delattr
