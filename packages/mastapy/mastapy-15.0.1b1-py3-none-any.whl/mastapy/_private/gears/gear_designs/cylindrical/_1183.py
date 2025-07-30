"""Scuffing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1184
from mastapy._private.utility import _1779

_SCUFFING = python_net_import("SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "Scuffing")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1185, _1186

    Self = TypeVar("Self", bound="Scuffing")
    CastSelf = TypeVar("CastSelf", bound="Scuffing._Cast_Scuffing")


__docformat__ = "restructuredtext en"
__all__ = ("Scuffing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Scuffing:
    """Special nested class for casting Scuffing to subclasses."""

    __parent__: "Scuffing"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def scuffing(self: "CastSelf") -> "Scuffing":
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
class Scuffing(_1779.IndependentReportablePropertiesBase["Scuffing"]):
    """Scuffing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SCUFFING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bulk_tooth_temperature_of_test_gears_flash_temperature_method(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "BulkToothTemperatureOfTestGearsFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @bulk_tooth_temperature_of_test_gears_flash_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def bulk_tooth_temperature_of_test_gears_flash_temperature_method(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "BulkToothTemperatureOfTestGearsFlashTemperatureMethod",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def bulk_tooth_temperature_of_test_gears_integral_temperature_method(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "BulkToothTemperatureOfTestGearsIntegralTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @bulk_tooth_temperature_of_test_gears_integral_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def bulk_tooth_temperature_of_test_gears_integral_temperature_method(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "BulkToothTemperatureOfTestGearsIntegralTemperatureMethod",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def coefficient_of_friction_method_flash_temperature_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods":
        """EnumWithSelectedValue[mastapy.gears.gear_designs.cylindrical.ScuffingCoefficientOfFrictionMethods]"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionMethodFlashTemperatureMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @coefficient_of_friction_method_flash_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_method_flash_temperature_method(
        self: "Self", value: "_1184.ScuffingCoefficientOfFrictionMethods"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "CoefficientOfFrictionMethodFlashTemperatureMethod", value
        )

    @property
    @exception_bridge
    def contact_time_at_high_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactTimeAtHighVelocity")

        if temp is None:
            return 0.0

        return temp

    @contact_time_at_high_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_time_at_high_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ContactTimeAtHighVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def contact_time_at_medium_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactTimeAtMediumVelocity")

        if temp is None:
            return 0.0

        return temp

    @contact_time_at_medium_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_time_at_medium_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ContactTimeAtMediumVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def estimate_oil_test_results_for_long_contact_times(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "EstimateOilTestResultsForLongContactTimes"
        )

        if temp is None:
            return False

        return temp

    @estimate_oil_test_results_for_long_contact_times.setter
    @exception_bridge
    @enforce_parameter_types
    def estimate_oil_test_results_for_long_contact_times(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EstimateOilTestResultsForLongContactTimes",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def estimate_tooth_temperature(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "EstimateToothTemperature")

        if temp is None:
            return False

        return temp

    @estimate_tooth_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def estimate_tooth_temperature(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EstimateToothTemperature",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def maximum_flash_temperature_of_test_gears_flash_temperature_method(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumFlashTemperatureOfTestGearsFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_flash_temperature_of_test_gears_flash_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_flash_temperature_of_test_gears_flash_temperature_method(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumFlashTemperatureOfTestGearsFlashTemperatureMethod",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mean_coefficient_of_friction_flash_temperature_method(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MeanCoefficientOfFrictionFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @mean_coefficient_of_friction_flash_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_coefficient_of_friction_flash_temperature_method(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanCoefficientOfFrictionFlashTemperatureMethod",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mean_flash_temperature_of_test_gears_integral_temperature_method(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MeanFlashTemperatureOfTestGearsIntegralTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @mean_flash_temperature_of_test_gears_integral_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_flash_temperature_of_test_gears_integral_temperature_method(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanFlashTemperatureOfTestGearsIntegralTemperatureMethod",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def scuffing_temperature_at_high_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ScuffingTemperatureAtHighVelocity")

        if temp is None:
            return 0.0

        return temp

    @scuffing_temperature_at_high_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def scuffing_temperature_at_high_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ScuffingTemperatureAtHighVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def scuffing_temperature_at_medium_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingTemperatureAtMediumVelocity"
        )

        if temp is None:
            return 0.0

        return temp

    @scuffing_temperature_at_medium_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def scuffing_temperature_at_medium_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ScuffingTemperatureAtMediumVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def scuffing_temperature_method_agma(
        self: "Self",
    ) -> "_1185.ScuffingTemperatureMethodsAGMA":
        """mastapy.gears.gear_designs.cylindrical.ScuffingTemperatureMethodsAGMA"""
        temp = pythonnet_property_get(self.wrapped, "ScuffingTemperatureMethodAGMA")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ScuffingTemperatureMethodsAGMA",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1185",
            "ScuffingTemperatureMethodsAGMA",
        )(value)

    @scuffing_temperature_method_agma.setter
    @exception_bridge
    @enforce_parameter_types
    def scuffing_temperature_method_agma(
        self: "Self", value: "_1185.ScuffingTemperatureMethodsAGMA"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ScuffingTemperatureMethodsAGMA",
        )
        pythonnet_property_set(self.wrapped, "ScuffingTemperatureMethodAGMA", value)

    @property
    @exception_bridge
    def scuffing_temperature_method_iso(
        self: "Self",
    ) -> "_1186.ScuffingTemperatureMethodsISO":
        """mastapy.gears.gear_designs.cylindrical.ScuffingTemperatureMethodsISO"""
        temp = pythonnet_property_get(self.wrapped, "ScuffingTemperatureMethodISO")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ScuffingTemperatureMethodsISO",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1186",
            "ScuffingTemperatureMethodsISO",
        )(value)

    @scuffing_temperature_method_iso.setter
    @exception_bridge
    @enforce_parameter_types
    def scuffing_temperature_method_iso(
        self: "Self", value: "_1186.ScuffingTemperatureMethodsISO"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ScuffingTemperatureMethodsISO",
        )
        pythonnet_property_set(self.wrapped, "ScuffingTemperatureMethodISO", value)

    @property
    @exception_bridge
    def user_input_scuffing_integral_temperature_for_long_contact_times(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "UserInputScuffingIntegralTemperatureForLongContactTimes"
        )

        if temp is None:
            return 0.0

        return temp

    @user_input_scuffing_integral_temperature_for_long_contact_times.setter
    @exception_bridge
    @enforce_parameter_types
    def user_input_scuffing_integral_temperature_for_long_contact_times(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserInputScuffingIntegralTemperatureForLongContactTimes",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def user_input_scuffing_temperature_flash_temperature_method(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "UserInputScuffingTemperatureFlashTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @user_input_scuffing_temperature_flash_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def user_input_scuffing_temperature_flash_temperature_method(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserInputScuffingTemperatureFlashTemperatureMethod",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def user_input_scuffing_temperature_integral_temperature_method(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "UserInputScuffingTemperatureIntegralTemperatureMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @user_input_scuffing_temperature_integral_temperature_method.setter
    @exception_bridge
    @enforce_parameter_types
    def user_input_scuffing_temperature_integral_temperature_method(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserInputScuffingTemperatureIntegralTemperatureMethod",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def user_input_scuffing_temperature_for_long_contact_times(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "UserInputScuffingTemperatureForLongContactTimes"
        )

        if temp is None:
            return 0.0

        return temp

    @user_input_scuffing_temperature_for_long_contact_times.setter
    @exception_bridge
    @enforce_parameter_types
    def user_input_scuffing_temperature_for_long_contact_times(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserInputScuffingTemperatureForLongContactTimes",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Scuffing":
        """Cast to another type.

        Returns:
            _Cast_Scuffing
        """
        return _Cast_Scuffing(self)
