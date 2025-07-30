"""DynamicForceLoadCase"""

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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.load_cases_and_analyses import _1530, _1556

_DYNAMIC_FORCE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "DynamicForceLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1533,
        _1537,
        _1538,
        _1543,
        _1553,
        _1557,
    )

    Self = TypeVar("Self", bound="DynamicForceLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="DynamicForceLoadCase._Cast_DynamicForceLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicForceLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicForceLoadCase:
    """Special nested class for casting DynamicForceLoadCase to subclasses."""

    __parent__: "DynamicForceLoadCase"

    @property
    def basic_dynamic_force_load_case(
        self: "CastSelf",
    ) -> "_1530.BasicDynamicForceLoadCase":
        return self.__parent__._cast(_1530.BasicDynamicForceLoadCase)

    @property
    def electric_machine_load_case_base(
        self: "CastSelf",
    ) -> "_1543.ElectricMachineLoadCaseBase":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1543

        return self.__parent__._cast(_1543.ElectricMachineLoadCaseBase)

    @property
    def dynamic_force_load_case(self: "CastSelf") -> "DynamicForceLoadCase":
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
class DynamicForceLoadCase(_1530.BasicDynamicForceLoadCase):
    """DynamicForceLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_FORCE_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def control_strategy(self: "Self") -> "_1538.ElectricMachineControlStrategy":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineControlStrategy"""
        temp = pythonnet_property_get(self.wrapped, "ControlStrategy")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.ElectricMachineControlStrategy",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1538",
            "ElectricMachineControlStrategy",
        )(value)

    @control_strategy.setter
    @exception_bridge
    @enforce_parameter_types
    def control_strategy(
        self: "Self", value: "_1538.ElectricMachineControlStrategy"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.ElectricMachineControlStrategy",
        )
        pythonnet_property_set(self.wrapped, "ControlStrategy", value)

    @property
    @exception_bridge
    def include_resistive_voltages(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeResistiveVoltages")

        if temp is None:
            return False

        return temp

    @include_resistive_voltages.setter
    @exception_bridge
    @enforce_parameter_types
    def include_resistive_voltages(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeResistiveVoltages",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def load_specification(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_SpecifyTorqueOrCurrent":
        """EnumWithSelectedValue[mastapy.electric_machines.load_cases_and_analyses.SpecifyTorqueOrCurrent]"""
        temp = pythonnet_property_get(self.wrapped, "LoadSpecification")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_SpecifyTorqueOrCurrent.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @load_specification.setter
    @exception_bridge
    @enforce_parameter_types
    def load_specification(self: "Self", value: "_1556.SpecifyTorqueOrCurrent") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SpecifyTorqueOrCurrent.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LoadSpecification", value)

    @property
    @exception_bridge
    def maximum_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumSpeed")

        if temp is None:
            return 0.0

        return temp

    @maximum_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumSpeed", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def minimum_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumSpeed")

        if temp is None:
            return 0.0

        return temp

    @minimum_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumSpeed", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_operating_points(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfOperatingPoints")

        if temp is None:
            return 0

        return temp

    @number_of_operating_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_operating_points(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfOperatingPoints",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def operating_points_specification_method(
        self: "Self",
    ) -> "_1553.OperatingPointsSpecificationMethod":
        """mastapy.electric_machines.load_cases_and_analyses.OperatingPointsSpecificationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "OperatingPointsSpecificationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.OperatingPointsSpecificationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1553",
            "OperatingPointsSpecificationMethod",
        )(value)

    @operating_points_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def operating_points_specification_method(
        self: "Self", value: "_1553.OperatingPointsSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.OperatingPointsSpecificationMethod",
        )
        pythonnet_property_set(
            self.wrapped, "OperatingPointsSpecificationMethod", value
        )

    @property
    @exception_bridge
    def speed_points_distribution(self: "Self") -> "_1557.SpeedPointsDistribution":
        """mastapy.electric_machines.load_cases_and_analyses.SpeedPointsDistribution"""
        temp = pythonnet_property_get(self.wrapped, "SpeedPointsDistribution")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.SpeedPointsDistribution",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1557",
            "SpeedPointsDistribution",
        )(value)

    @speed_points_distribution.setter
    @exception_bridge
    @enforce_parameter_types
    def speed_points_distribution(
        self: "Self", value: "_1557.SpeedPointsDistribution"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.SpeedPointsDistribution",
        )
        pythonnet_property_set(self.wrapped, "SpeedPointsDistribution", value)

    @property
    @exception_bridge
    def basic_mechanical_loss_settings(
        self: "Self",
    ) -> "_1537.ElectricMachineBasicMechanicalLossSettings":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineBasicMechanicalLossSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicMechanicalLossSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def add_operating_point(
        self: "Self", torque: "float", speed: "float"
    ) -> "_1533.DynamicForcesOperatingPoint":
        """mastapy.electric_machines.load_cases_and_analyses.DynamicForcesOperatingPoint

        Args:
            torque (float)
            speed (float)
        """
        torque = float(torque)
        speed = float(speed)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddOperatingPoint",
            torque if torque else 0.0,
            speed if speed else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def set_speeds(self: "Self", values: "List[float]") -> None:
        """Method does not return.

        Args:
            values (List[float])
        """
        values = conversion.mp_to_pn_list_float(values)
        pythonnet_method_call(self.wrapped, "SetSpeeds", values)

    @exception_bridge
    @enforce_parameter_types
    def set_speeds_in_si_units(self: "Self", values: "List[float]") -> None:
        """Method does not return.

        Args:
            values (List[float])
        """
        values = conversion.mp_to_pn_list_float(values)
        pythonnet_method_call(self.wrapped, "SetSpeedsInSIUnits", values)

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicForceLoadCase":
        """Cast to another type.

        Returns:
            _Cast_DynamicForceLoadCase
        """
        return _Cast_DynamicForceLoadCase(self)
