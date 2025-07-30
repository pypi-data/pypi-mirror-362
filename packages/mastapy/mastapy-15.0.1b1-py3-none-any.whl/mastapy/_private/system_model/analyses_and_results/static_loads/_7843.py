"""TimeSeriesLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7673

_TIME_SERIES_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "TimeSeriesLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7877
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5961,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5745,
        _5751,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7686

    Self = TypeVar("Self", bound="TimeSeriesLoadCase")
    CastSelf = TypeVar("CastSelf", bound="TimeSeriesLoadCase._Cast_TimeSeriesLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("TimeSeriesLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TimeSeriesLoadCase:
    """Special nested class for casting TimeSeriesLoadCase to subclasses."""

    __parent__: "TimeSeriesLoadCase"

    @property
    def load_case(self: "CastSelf") -> "_7673.LoadCase":
        return self.__parent__._cast(_7673.LoadCase)

    @property
    def context(self: "CastSelf") -> "_2891.Context":
        from mastapy._private.system_model.analyses_and_results import _2891

        return self.__parent__._cast(_2891.Context)

    @property
    def time_series_load_case(self: "CastSelf") -> "TimeSeriesLoadCase":
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
class TimeSeriesLoadCase(_7673.LoadCase):
    """TimeSeriesLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TIME_SERIES_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def duration_for_rating(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DurationForRating")

        if temp is None:
            return 0.0

        return temp

    @duration_for_rating.setter
    @exception_bridge
    @enforce_parameter_types
    def duration_for_rating(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DurationForRating",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def driva_analysis_options(self: "Self") -> "_5745.MBDAnalysisOptions":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MBDAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DRIVAAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def multibody_dynamics_analysis(self: "Self") -> "_5751.MultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MultibodyDynamicsAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MultibodyDynamicsAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def time_series_load_case_group(self: "Self") -> "_5961.TimeSeriesLoadCaseGroup":
        """mastapy.system_model.analyses_and_results.load_case_groups.TimeSeriesLoadCaseGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesLoadCaseGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def duplicate(
        self: "Self",
        new_load_case_group: "_5961.TimeSeriesLoadCaseGroup",
        name: "str" = "None",
    ) -> "TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Args:
            new_load_case_group (mastapy.system_model.analyses_and_results.load_case_groups.TimeSeriesLoadCaseGroup)
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "Duplicate",
            new_load_case_group.wrapped if new_load_case_group else None,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def analysis_of(
        self: "Self", analysis_type: "_7686.AnalysisType"
    ) -> "_7877.AnalysisCase":
        """mastapy.system_model.analyses_and_results.analysis_cases.AnalysisCase

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)
        """
        analysis_type = conversion.mp_to_pn_enum(
            analysis_type,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.AnalysisType",
        )
        method_result = pythonnet_method_call(self.wrapped, "AnalysisOf", analysis_type)
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TimeSeriesLoadCase":
        """Cast to another type.

        Returns:
            _Cast_TimeSeriesLoadCase
        """
        return _Cast_TimeSeriesLoadCase(self)
