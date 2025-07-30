"""SpeedOptionsForHarmonicAnalysisResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7878
from mastapy._private.system_model.analyses_and_results.static_loads import _7674

_SPEED_OPTIONS_FOR_HARMONIC_ANALYSIS_RESULTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "SpeedOptionsForHarmonicAnalysisResults",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="SpeedOptionsForHarmonicAnalysisResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpeedOptionsForHarmonicAnalysisResults._Cast_SpeedOptionsForHarmonicAnalysisResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpeedOptionsForHarmonicAnalysisResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpeedOptionsForHarmonicAnalysisResults:
    """Special nested class for casting SpeedOptionsForHarmonicAnalysisResults to subclasses."""

    __parent__: "SpeedOptionsForHarmonicAnalysisResults"

    @property
    def abstract_analysis_options(self: "CastSelf") -> "_7878.AbstractAnalysisOptions":
        return self.__parent__._cast(_7878.AbstractAnalysisOptions)

    @property
    def speed_options_for_harmonic_analysis_results(
        self: "CastSelf",
    ) -> "SpeedOptionsForHarmonicAnalysisResults":
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
class SpeedOptionsForHarmonicAnalysisResults(
    _7878.AbstractAnalysisOptions[_7674.StaticLoadCase]
):
    """SpeedOptionsForHarmonicAnalysisResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPEED_OPTIONS_FOR_HARMONIC_ANALYSIS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Maximum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Maximum", value)

    @property
    @exception_bridge
    def minimum(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Minimum")

        if temp is None:
            return 0.0

        return temp

    @minimum.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Minimum", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_speeds(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSpeeds")

        if temp is None:
            return 0

        return temp

    @number_of_speeds.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_speeds(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSpeeds", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def reference_power_load_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferencePowerLoadSpeed")

        if temp is None:
            return 0.0

        return temp

    @reference_power_load_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_power_load_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReferencePowerLoadSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def show_result_in_time_domain(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowResultInTimeDomain")

        if temp is None:
            return False

        return temp

    @show_result_in_time_domain.setter
    @exception_bridge
    @enforce_parameter_types
    def show_result_in_time_domain(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowResultInTimeDomain",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SpeedOptionsForHarmonicAnalysisResults":
        """Cast to another type.

        Returns:
            _Cast_SpeedOptionsForHarmonicAnalysisResults
        """
        return _Cast_SpeedOptionsForHarmonicAnalysisResults(self)
