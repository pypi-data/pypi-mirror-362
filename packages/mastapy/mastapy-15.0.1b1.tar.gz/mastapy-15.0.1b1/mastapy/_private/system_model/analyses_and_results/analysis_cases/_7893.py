"""TimeSeriesLoadAnalysisCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7877

_TIME_SERIES_LOAD_ANALYSIS_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases",
    "TimeSeriesLoadAnalysisCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5751
    from mastapy._private.system_model.analyses_and_results.static_loads import _7843

    Self = TypeVar("Self", bound="TimeSeriesLoadAnalysisCase")
    CastSelf = TypeVar(
        "CastSelf", bound="TimeSeriesLoadAnalysisCase._Cast_TimeSeriesLoadAnalysisCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TimeSeriesLoadAnalysisCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TimeSeriesLoadAnalysisCase:
    """Special nested class for casting TimeSeriesLoadAnalysisCase to subclasses."""

    __parent__: "TimeSeriesLoadAnalysisCase"

    @property
    def analysis_case(self: "CastSelf") -> "_7877.AnalysisCase":
        return self.__parent__._cast(_7877.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2891.Context":
        from mastapy._private.system_model.analyses_and_results import _2891

        return self.__parent__._cast(_2891.Context)

    @property
    def multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5751.MultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5751,
        )

        return self.__parent__._cast(_5751.MultibodyDynamicsAnalysis)

    @property
    def time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "TimeSeriesLoadAnalysisCase":
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
class TimeSeriesLoadAnalysisCase(_7877.AnalysisCase):
    """TimeSeriesLoadAnalysisCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TIME_SERIES_LOAD_ANALYSIS_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load_case(self: "Self") -> "_7843.TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TimeSeriesLoadAnalysisCase":
        """Cast to another type.

        Returns:
            _Cast_TimeSeriesLoadAnalysisCase
        """
        return _Cast_TimeSeriesLoadAnalysisCase(self)
