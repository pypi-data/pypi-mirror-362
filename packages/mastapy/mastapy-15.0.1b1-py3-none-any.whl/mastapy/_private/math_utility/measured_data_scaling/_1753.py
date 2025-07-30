"""DataScalingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1690
from mastapy._private.utility.units_and_measurements.measurements import (
    _1804,
    _1805,
    _1807,
    _1808,
    _1809,
    _1813,
    _1821,
    _1828,
    _1831,
    _1835,
    _1841,
    _1858,
    _1860,
    _1863,
    _1869,
    _1877,
    _1881,
    _1882,
    _1883,
    _1886,
    _1887,
    _1894,
    _1903,
    _1908,
    _1909,
    _1918,
    _1919,
    _1920,
    _1921,
    _1922,
    _1926,
    _1927,
)

_DATA_SCALING_OPTIONS = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredDataScaling", "DataScalingOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.math_utility import _1674
    from mastapy._private.math_utility.measured_data_scaling import _1754

    Self = TypeVar("Self", bound="DataScalingOptions")
    CastSelf = TypeVar("CastSelf", bound="DataScalingOptions._Cast_DataScalingOptions")


__docformat__ = "restructuredtext en"
__all__ = ("DataScalingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DataScalingOptions:
    """Special nested class for casting DataScalingOptions to subclasses."""

    __parent__: "DataScalingOptions"

    @property
    def data_scaling_options(self: "CastSelf") -> "DataScalingOptions":
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
class DataScalingOptions(_0.APIBase):
    """DataScalingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATA_SCALING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def dynamic_scaling(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling":
        """EnumWithSelectedValue[mastapy.math_utility.DynamicsResponseScaling]"""
        temp = pythonnet_property_get(self.wrapped, "DynamicScaling")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @dynamic_scaling.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_scaling(self: "Self", value: "_1690.DynamicsResponseScaling") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DynamicScaling", value)

    @property
    @exception_bridge
    def weighting(self: "Self") -> "_1674.AcousticWeighting":
        """mastapy.math_utility.AcousticWeighting"""
        temp = pythonnet_property_get(self.wrapped, "Weighting")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.AcousticWeighting"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1674", "AcousticWeighting"
        )(value)

    @weighting.setter
    @exception_bridge
    @enforce_parameter_types
    def weighting(self: "Self", value: "_1674.AcousticWeighting") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.AcousticWeighting"
        )
        pythonnet_property_set(self.wrapped, "Weighting", value)

    @property
    @exception_bridge
    def acceleration_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1804.Acceleration]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Acceleration]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AccelerationReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1804.Acceleration](temp)

    @property
    @exception_bridge
    def angle_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1805.Angle]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Angle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngleReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1805.Angle](temp)

    @property
    @exception_bridge
    def angular_acceleration_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1809.AngularAcceleration]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.AngularAcceleration]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularAccelerationReferenceValues"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1809.AngularAcceleration](
            temp
        )

    @property
    @exception_bridge
    def angular_velocity_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1813.AngularVelocity]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.AngularVelocity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularVelocityReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1813.AngularVelocity](temp)

    @property
    @exception_bridge
    def damage_rate(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1821.DamageRate]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.DamageRate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageRate")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1821.DamageRate](temp)

    @property
    @exception_bridge
    def energy_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1828.Energy]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Energy]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1828.Energy](temp)

    @property
    @exception_bridge
    def force_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1835.Force]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Force]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1835.Force](temp)

    @property
    @exception_bridge
    def frequency_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1841.Frequency]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Frequency]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1841.Frequency](temp)

    @property
    @exception_bridge
    def linear_stiffness_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1869.LinearStiffness]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.LinearStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearStiffnessReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1869.LinearStiffness](temp)

    @property
    @exception_bridge
    def mass_per_unit_time_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1877.MassPerUnitTime]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.MassPerUnitTime]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassPerUnitTimeReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1877.MassPerUnitTime](temp)

    @property
    @exception_bridge
    def medium_length_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1858.LengthMedium]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.LengthMedium]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MediumLengthReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1858.LengthMedium](temp)

    @property
    @exception_bridge
    def percentage(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1882.Percentage]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Percentage]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Percentage")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1882.Percentage](temp)

    @property
    @exception_bridge
    def power_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1883.Power]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Power]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1883.Power](temp)

    @property
    @exception_bridge
    def power_small_per_unit_area_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1887.PowerSmallPerArea]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.PowerSmallPerArea]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerSmallPerUnitAreaReferenceValues"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1887.PowerSmallPerArea](
            temp
        )

    @property
    @exception_bridge
    def power_small_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1886.PowerSmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.PowerSmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerSmallReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1886.PowerSmall](temp)

    @property
    @exception_bridge
    def pressure_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1894.PressureSmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.PressureSmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1894.PressureSmall](temp)

    @property
    @exception_bridge
    def safety_factor(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1903.SafetyFactor]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.SafetyFactor]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1903.SafetyFactor](temp)

    @property
    @exception_bridge
    def short_length_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1860.LengthShort]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.LengthShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShortLengthReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1860.LengthShort](temp)

    @property
    @exception_bridge
    def short_time_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1918.TimeShort]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.TimeShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShortTimeReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1918.TimeShort](temp)

    @property
    @exception_bridge
    def small_angle_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1807.AngleSmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.AngleSmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallAngleReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1807.AngleSmall](temp)

    @property
    @exception_bridge
    def small_energy_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1831.EnergySmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.EnergySmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallEnergyReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1831.EnergySmall](temp)

    @property
    @exception_bridge
    def small_velocity_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1927.VelocitySmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.VelocitySmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallVelocityReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1927.VelocitySmall](temp)

    @property
    @exception_bridge
    def stress_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1908.Stress]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Stress]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1908.Stress](temp)

    @property
    @exception_bridge
    def temperature_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1909.Temperature]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Temperature]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemperatureReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1909.Temperature](temp)

    @property
    @exception_bridge
    def torque_converter_inverse_k(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1921.TorqueConverterInverseK]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.TorqueConverterInverseK]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueConverterInverseK")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _1921.TorqueConverterInverseK
        ](temp)

    @property
    @exception_bridge
    def torque_converter_k(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1922.TorqueConverterK]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.TorqueConverterK]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueConverterK")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1922.TorqueConverterK](
            temp
        )

    @property
    @exception_bridge
    def torque_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1920.Torque]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Torque]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1920.Torque](temp)

    @property
    @exception_bridge
    def unmeasureable(self: "Self") -> "_1754.DataScalingReferenceValues[_1881.Number]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Number]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Unmeasureable")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1881.Number](temp)

    @property
    @exception_bridge
    def velocity_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1926.Velocity]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.Velocity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VelocityReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1926.Velocity](temp)

    @property
    @exception_bridge
    def very_short_length_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1863.LengthVeryShort]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.LengthVeryShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VeryShortLengthReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1863.LengthVeryShort](temp)

    @property
    @exception_bridge
    def very_short_time_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1919.TimeVeryShort]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.TimeVeryShort]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VeryShortTimeReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1919.TimeVeryShort](temp)

    @property
    @exception_bridge
    def very_small_angle_reference_values(
        self: "Self",
    ) -> "_1754.DataScalingReferenceValues[_1808.AngleVerySmall]":
        """mastapy.math_utility.measured_data_scaling.DataScalingReferenceValues[mastapy.utility.units_and_measurements.measurements.AngleVerySmall]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VerySmallAngleReferenceValues")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1808.AngleVerySmall](temp)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DataScalingOptions":
        """Cast to another type.

        Returns:
            _Cast_DataScalingOptions
        """
        return _Cast_DataScalingOptions(self)
