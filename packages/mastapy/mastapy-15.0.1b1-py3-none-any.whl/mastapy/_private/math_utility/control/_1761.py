"""PIDControlSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_PID_CONTROL_SETTINGS = python_net_import(
    "SMT.MastaAPI.MathUtility.Control", "PIDControlSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1707
    from mastapy._private.math_utility.measured_data import _1749

    Self = TypeVar("Self", bound="PIDControlSettings")
    CastSelf = TypeVar("CastSelf", bound="PIDControlSettings._Cast_PIDControlSettings")


__docformat__ = "restructuredtext en"
__all__ = ("PIDControlSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PIDControlSettings:
    """Special nested class for casting PIDControlSettings to subclasses."""

    __parent__: "PIDControlSettings"

    @property
    def pid_control_settings(self: "CastSelf") -> "PIDControlSettings":
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
class PIDControlSettings(_0.APIBase):
    """PIDControlSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PID_CONTROL_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def control_start_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ControlStartTime")

        if temp is None:
            return 0.0

        return temp

    @control_start_time.setter
    @exception_bridge
    @enforce_parameter_types
    def control_start_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ControlStartTime", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def differential_gain(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DifferentialGain")

        if temp is None:
            return 0.0

        return temp

    @differential_gain.setter
    @exception_bridge
    @enforce_parameter_types
    def differential_gain(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DifferentialGain", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def differential_gain_vs_time_and_error(
        self: "Self",
    ) -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "DifferentialGainVsTimeAndError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @differential_gain_vs_time_and_error.setter
    @exception_bridge
    @enforce_parameter_types
    def differential_gain_vs_time_and_error(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "DifferentialGainVsTimeAndError", value.wrapped
        )

    @property
    @exception_bridge
    def differential_time_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DifferentialTimeConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def integral_gain(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "IntegralGain")

        if temp is None:
            return 0.0

        return temp

    @integral_gain.setter
    @exception_bridge
    @enforce_parameter_types
    def integral_gain(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "IntegralGain", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def integral_gain_vs_time_and_error(self: "Self") -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "IntegralGainVsTimeAndError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @integral_gain_vs_time_and_error.setter
    @exception_bridge
    @enforce_parameter_types
    def integral_gain_vs_time_and_error(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "IntegralGainVsTimeAndError", value.wrapped
        )

    @property
    @exception_bridge
    def integral_time_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntegralTimeConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def max_change_in_manipulated_value_per_unit_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaxChangeInManipulatedValuePerUnitTime"
        )

        if temp is None:
            return 0.0

        return temp

    @max_change_in_manipulated_value_per_unit_time.setter
    @exception_bridge
    @enforce_parameter_types
    def max_change_in_manipulated_value_per_unit_time(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaxChangeInManipulatedValuePerUnitTime",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def max_manipulated_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaxManipulatedValue")

        if temp is None:
            return 0.0

        return temp

    @max_manipulated_value.setter
    @exception_bridge
    @enforce_parameter_types
    def max_manipulated_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaxManipulatedValue",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def min_manipulated_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinManipulatedValue")

        if temp is None:
            return 0.0

        return temp

    @min_manipulated_value.setter
    @exception_bridge
    @enforce_parameter_types
    def min_manipulated_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinManipulatedValue",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pid_calculates_change_in_manipulated_value(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "PIDCalculatesChangeInManipulatedValue"
        )

        if temp is None:
            return False

        return temp

    @pid_calculates_change_in_manipulated_value.setter
    @exception_bridge
    @enforce_parameter_types
    def pid_calculates_change_in_manipulated_value(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PIDCalculatesChangeInManipulatedValue",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def proportional_gain(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProportionalGain")

        if temp is None:
            return 0.0

        return temp

    @proportional_gain.setter
    @exception_bridge
    @enforce_parameter_types
    def proportional_gain(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ProportionalGain", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def proportional_gain_vs_time_and_error(
        self: "Self",
    ) -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ProportionalGainVsTimeAndError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @proportional_gain_vs_time_and_error.setter
    @exception_bridge
    @enforce_parameter_types
    def proportional_gain_vs_time_and_error(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "ProportionalGainVsTimeAndError", value.wrapped
        )

    @property
    @exception_bridge
    def set_point_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SetPointValue")

        if temp is None:
            return 0.0

        return temp

    @set_point_value.setter
    @exception_bridge
    @enforce_parameter_types
    def set_point_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SetPointValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def update_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UpdateFrequency")

        if temp is None:
            return 0.0

        return temp

    @update_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def update_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "UpdateFrequency", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def update_method(self: "Self") -> "_1707.PIDControlUpdateMethod":
        """mastapy.math_utility.PIDControlUpdateMethod"""
        temp = pythonnet_property_get(self.wrapped, "UpdateMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.PIDControlUpdateMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1707", "PIDControlUpdateMethod"
        )(value)

    @update_method.setter
    @exception_bridge
    @enforce_parameter_types
    def update_method(self: "Self", value: "_1707.PIDControlUpdateMethod") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.PIDControlUpdateMethod"
        )
        pythonnet_property_set(self.wrapped, "UpdateMethod", value)

    @property
    @exception_bridge
    def update_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UpdateTime")

        if temp is None:
            return 0.0

        return temp

    @update_time.setter
    @exception_bridge
    @enforce_parameter_types
    def update_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "UpdateTime", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def use_differential_gain_scheduling(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDifferentialGainScheduling")

        if temp is None:
            return False

        return temp

    @use_differential_gain_scheduling.setter
    @exception_bridge
    @enforce_parameter_types
    def use_differential_gain_scheduling(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDifferentialGainScheduling",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_integral_gain_scheduling(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseIntegralGainScheduling")

        if temp is None:
            return False

        return temp

    @use_integral_gain_scheduling.setter
    @exception_bridge
    @enforce_parameter_types
    def use_integral_gain_scheduling(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseIntegralGainScheduling",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_integrator_anti_windup(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseIntegratorAntiWindup")

        if temp is None:
            return False

        return temp

    @use_integrator_anti_windup.setter
    @exception_bridge
    @enforce_parameter_types
    def use_integrator_anti_windup(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseIntegratorAntiWindup",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_proportional_gain_scheduling(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseProportionalGainScheduling")

        if temp is None:
            return False

        return temp

    @use_proportional_gain_scheduling.setter
    @exception_bridge
    @enforce_parameter_types
    def use_proportional_gain_scheduling(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseProportionalGainScheduling",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PIDControlSettings":
        """Cast to another type.

        Returns:
            _Cast_PIDControlSettings
        """
        return _Cast_PIDControlSettings(self)
