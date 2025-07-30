"""TimeSeriesLoadCaseGroup"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5949

_TIME_SERIES_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "TimeSeriesLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2888, _2916
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7686,
        _7843,
    )

    Self = TypeVar("Self", bound="TimeSeriesLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="TimeSeriesLoadCaseGroup._Cast_TimeSeriesLoadCaseGroup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TimeSeriesLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TimeSeriesLoadCaseGroup:
    """Special nested class for casting TimeSeriesLoadCaseGroup to subclasses."""

    __parent__: "TimeSeriesLoadCaseGroup"

    @property
    def abstract_load_case_group(self: "CastSelf") -> "_5949.AbstractLoadCaseGroup":
        return self.__parent__._cast(_5949.AbstractLoadCaseGroup)

    @property
    def time_series_load_case_group(self: "CastSelf") -> "TimeSeriesLoadCaseGroup":
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
class TimeSeriesLoadCaseGroup(_5949.AbstractLoadCaseGroup):
    """TimeSeriesLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TIME_SERIES_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load_cases(self: "Self") -> "List[_7843.TimeSeriesLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def compound_multibody_dynamics_analysis(
        self: "Self",
    ) -> "_2916.CompoundMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.CompoundMultibodyDynamicsAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundMultibodyDynamicsAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @exception_bridge
    @enforce_parameter_types
    def analysis_of(
        self: "Self", analysis_type: "_7686.AnalysisType"
    ) -> "_2888.CompoundAnalysis":
        """mastapy.system_model.analyses_and_results.CompoundAnalysis

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
    def cast_to(self: "Self") -> "_Cast_TimeSeriesLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_TimeSeriesLoadCaseGroup
        """
        return _Cast_TimeSeriesLoadCaseGroup(self)
