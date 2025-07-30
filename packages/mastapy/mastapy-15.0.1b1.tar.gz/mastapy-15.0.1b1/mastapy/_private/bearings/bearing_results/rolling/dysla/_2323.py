"""DynamicBearingAnalysisOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DYNAMIC_BEARING_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.Dysla",
    "DynamicBearingAnalysisOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DynamicBearingAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DynamicBearingAnalysisOptions._Cast_DynamicBearingAnalysisOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicBearingAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicBearingAnalysisOptions:
    """Special nested class for casting DynamicBearingAnalysisOptions to subclasses."""

    __parent__: "DynamicBearingAnalysisOptions"

    @property
    def dynamic_bearing_analysis_options(
        self: "CastSelf",
    ) -> "DynamicBearingAnalysisOptions":
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
class DynamicBearingAnalysisOptions(_0.APIBase):
    """DynamicBearingAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_BEARING_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def element_displacement_damping_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ElementDisplacementDampingFactor")

        if temp is None:
            return 0.0

        return temp

    @element_displacement_damping_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def element_displacement_damping_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ElementDisplacementDampingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def end_revolution(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndRevolution")

        if temp is None:
            return 0.0

        return temp

    @end_revolution.setter
    @exception_bridge
    @enforce_parameter_types
    def end_revolution(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EndRevolution", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def end_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndTime")

        if temp is None:
            return 0.0

        return temp

    @end_time.setter
    @exception_bridge
    @enforce_parameter_types
    def end_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EndTime", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def include_cage(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeCage")

        if temp is None:
            return False

        return temp

    @include_cage.setter
    @exception_bridge
    @enforce_parameter_types
    def include_cage(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IncludeCage", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def include_torsional_vibration_on_inner(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeTorsionalVibrationOnInner")

        if temp is None:
            return False

        return temp

    @include_torsional_vibration_on_inner.setter
    @exception_bridge
    @enforce_parameter_types
    def include_torsional_vibration_on_inner(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeTorsionalVibrationOnInner",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_torsional_vibration_on_outer(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeTorsionalVibrationOnOuter")

        if temp is None:
            return False

        return temp

    @include_torsional_vibration_on_outer.setter
    @exception_bridge
    @enforce_parameter_types
    def include_torsional_vibration_on_outer(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeTorsionalVibrationOnOuter",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def log_all_points_during_cage_impacts(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LogAllPointsDuringCageImpacts")

        if temp is None:
            return False

        return temp

    @log_all_points_during_cage_impacts.setter
    @exception_bridge
    @enforce_parameter_types
    def log_all_points_during_cage_impacts(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LogAllPointsDuringCageImpacts",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def log_all_points(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LogAllPoints")

        if temp is None:
            return False

        return temp

    @log_all_points.setter
    @exception_bridge
    @enforce_parameter_types
    def log_all_points(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "LogAllPoints", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def logging_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoggingFrequency")

        if temp is None:
            return 0.0

        return temp

    @logging_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def logging_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LoggingFrequency", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum_number_of_time_steps(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTimeSteps")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_time_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_time_steps(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfTimeSteps",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def order_of_inner_torsional_vibrations(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OrderOfInnerTorsionalVibrations")

        if temp is None:
            return 0.0

        return temp

    @order_of_inner_torsional_vibrations.setter
    @exception_bridge
    @enforce_parameter_types
    def order_of_inner_torsional_vibrations(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OrderOfInnerTorsionalVibrations",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def order_of_outer_torsional_vibrations(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OrderOfOuterTorsionalVibrations")

        if temp is None:
            return 0.0

        return temp

    @order_of_outer_torsional_vibrations.setter
    @exception_bridge
    @enforce_parameter_types
    def order_of_outer_torsional_vibrations(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OrderOfOuterTorsionalVibrations",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def percentage_amplitude_inner_torsional_vibration(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PercentageAmplitudeInnerTorsionalVibration"
        )

        if temp is None:
            return 0.0

        return temp

    @percentage_amplitude_inner_torsional_vibration.setter
    @exception_bridge
    @enforce_parameter_types
    def percentage_amplitude_inner_torsional_vibration(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PercentageAmplitudeInnerTorsionalVibration",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def percentage_amplitude_outer_torsional_vibration(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PercentageAmplitudeOuterTorsionalVibration"
        )

        if temp is None:
            return 0.0

        return temp

    @percentage_amplitude_outer_torsional_vibration.setter
    @exception_bridge
    @enforce_parameter_types
    def percentage_amplitude_outer_torsional_vibration(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PercentageAmplitudeOuterTorsionalVibration",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_number_of_element_revolutions(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseNumberOfElementRevolutions")

        if temp is None:
            return False

        return temp

    @use_number_of_element_revolutions.setter
    @exception_bridge
    @enforce_parameter_types
    def use_number_of_element_revolutions(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseNumberOfElementRevolutions",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicBearingAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_DynamicBearingAnalysisOptions
        """
        return _Cast_DynamicBearingAnalysisOptions(self)
