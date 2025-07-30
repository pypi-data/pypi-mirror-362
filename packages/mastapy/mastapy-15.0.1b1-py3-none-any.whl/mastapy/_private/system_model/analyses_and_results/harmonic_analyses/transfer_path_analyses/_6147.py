"""TransferPathAnalysisCharts"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_TRANSFER_PATH_ANALYSIS_CHARTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.TransferPathAnalyses",
    "TransferPathAnalysisCharts",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="TransferPathAnalysisCharts")
    CastSelf = TypeVar(
        "CastSelf", bound="TransferPathAnalysisCharts._Cast_TransferPathAnalysisCharts"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransferPathAnalysisCharts",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransferPathAnalysisCharts:
    """Special nested class for casting TransferPathAnalysisCharts to subclasses."""

    __parent__: "TransferPathAnalysisCharts"

    @property
    def transfer_path_analysis_charts(self: "CastSelf") -> "TransferPathAnalysisCharts":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class TransferPathAnalysisCharts(_0.APIBase):
    """TransferPathAnalysisCharts

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSFER_PATH_ANALYSIS_CHARTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def force_at_transfer_path_node_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceAtTransferPathNodeChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def responses_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResponsesChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def transmissibility_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissibilityChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TransferPathAnalysisCharts":
        """Cast to another type.

        Returns:
            _Cast_TransferPathAnalysisCharts
        """
        return _Cast_TransferPathAnalysisCharts(self)
