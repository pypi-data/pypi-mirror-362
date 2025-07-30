"""PowerLoadLoadCase"""

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
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
    overridable,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model import _2428
from mastapy._private.system_model.analyses_and_results.static_loads import _7849, _7853
from mastapy._private.system_model.fe import _2595

_POWER_LOAD_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PowerLoadLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility import _1718
    from mastapy._private.math_utility.control import _1761
    from mastapy._private.math_utility.measured_data import _1749
    from mastapy._private.nodal_analysis.varying_input_components import _103
    from mastapy._private.system_model import _2427, _2429
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5803
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7706,
        _7740,
        _7795,
        _7799,
    )
    from mastapy._private.system_model.part_model import _2703

    Self = TypeVar("Self", bound="PowerLoadLoadCase")
    CastSelf = TypeVar("CastSelf", bound="PowerLoadLoadCase._Cast_PowerLoadLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PowerLoadLoadCase:
    """Special nested class for casting PowerLoadLoadCase to subclasses."""

    __parent__: "PowerLoadLoadCase"

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7853.VirtualComponentLoadCase":
        return self.__parent__._cast(_7853.VirtualComponentLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7795.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7795,
        )

        return self.__parent__._cast(_7795.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7706.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7706,
        )

        return self.__parent__._cast(_7706.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def power_load_load_case(self: "CastSelf") -> "PowerLoadLoadCase":
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
class PowerLoadLoadCase(_7853.VirtualComponentLoadCase):
    """PowerLoadLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POWER_LOAD_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def constant_resistance_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConstantResistanceCoefficient")

        if temp is None:
            return 0.0

        return temp

    @constant_resistance_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def constant_resistance_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ConstantResistanceCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def constant_resistance_coefficient_time_profile(
        self: "Self",
    ) -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "ConstantResistanceCoefficientTimeProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @constant_resistance_coefficient_time_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def constant_resistance_coefficient_time_profile(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "ConstantResistanceCoefficientTimeProfile", value.wrapped
        )

    @property
    @exception_bridge
    def constant_torque(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ConstantTorque")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @constant_torque.setter
    @exception_bridge
    @enforce_parameter_types
    def constant_torque(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ConstantTorque", value)

    @property
    @exception_bridge
    def drag_torque_specification_method(
        self: "Self",
    ) -> "_2427.PowerLoadDragTorqueSpecificationMethod":
        """mastapy.system_model.PowerLoadDragTorqueSpecificationMethod"""
        temp = pythonnet_property_get(self.wrapped, "DragTorqueSpecificationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PowerLoadDragTorqueSpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model._2427",
            "PowerLoadDragTorqueSpecificationMethod",
        )(value)

    @drag_torque_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def drag_torque_specification_method(
        self: "Self", value: "_2427.PowerLoadDragTorqueSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PowerLoadDragTorqueSpecificationMethod"
        )
        pythonnet_property_set(self.wrapped, "DragTorqueSpecificationMethod", value)

    @property
    @exception_bridge
    def drag_torque_vs_speed_and_time(self: "Self") -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "DragTorqueVsSpeedAndTime")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @drag_torque_vs_speed_and_time.setter
    @exception_bridge
    @enforce_parameter_types
    def drag_torque_vs_speed_and_time(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "DragTorqueVsSpeedAndTime", value.wrapped)

    @property
    @exception_bridge
    def dynamic_torsional_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DynamicTorsionalStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_torsional_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_torsional_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DynamicTorsionalStiffness", value)

    @property
    @exception_bridge
    def electric_machine_data_set_selector(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet":
        """ListWithSelectedItem[mastapy.system_model.fe.ElectricMachineDataSet]"""
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDataSetSelector")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ElectricMachineDataSet",
        )(temp)

    @electric_machine_data_set_selector.setter
    @exception_bridge
    @enforce_parameter_types
    def electric_machine_data_set_selector(
        self: "Self", value: "_2595.ElectricMachineDataSet"
    ) -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineDataSet.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ElectricMachineDataSetSelector", value)

    @property
    @exception_bridge
    def engine_throttle_position(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EngineThrottlePosition")

        if temp is None:
            return 0.0

        return temp

    @engine_throttle_position.setter
    @exception_bridge
    @enforce_parameter_types
    def engine_throttle_position(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EngineThrottlePosition",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def engine_throttle_time_profile(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "EngineThrottleTimeProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @engine_throttle_time_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def engine_throttle_time_profile(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "EngineThrottleTimeProfile", value.wrapped)

    @property
    @exception_bridge
    def first_order_lag_cutoff_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstOrderLagCutoffFrequency")

        if temp is None:
            return 0.0

        return temp

    @first_order_lag_cutoff_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def first_order_lag_cutoff_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FirstOrderLagCutoffFrequency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def first_order_lag_time_constant(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstOrderLagTimeConstant")

        if temp is None:
            return 0.0

        return temp

    @first_order_lag_time_constant.setter
    @exception_bridge
    @enforce_parameter_types
    def first_order_lag_time_constant(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FirstOrderLagTimeConstant",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def include_in_torsional_stiffness_calculation(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeInTorsionalStiffnessCalculation"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @include_in_torsional_stiffness_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def include_in_torsional_stiffness_calculation(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "IncludeInTorsionalStiffnessCalculation", value
        )

    @property
    @exception_bridge
    def is_wheel_using_static_friction_initially(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IsWheelUsingStaticFrictionInitially"
        )

        if temp is None:
            return False

        return temp

    @is_wheel_using_static_friction_initially.setter
    @exception_bridge
    @enforce_parameter_types
    def is_wheel_using_static_friction_initially(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsWheelUsingStaticFrictionInitially",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def linear_resistance_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearResistanceCoefficient")

        if temp is None:
            return 0.0

        return temp

    @linear_resistance_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_resistance_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearResistanceCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def linear_resistance_coefficient_time_profile(
        self: "Self",
    ) -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearResistanceCoefficientTimeProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @linear_resistance_coefficient_time_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_resistance_coefficient_time_profile(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "LinearResistanceCoefficientTimeProfile", value.wrapped
        )

    @property
    @exception_bridge
    def maximum_throttle_in_drive_cycle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumThrottleInDriveCycle")

        if temp is None:
            return 0.0

        return temp

    @maximum_throttle_in_drive_cycle.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_throttle_in_drive_cycle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumThrottleInDriveCycle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def power(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Power")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @power.setter
    @exception_bridge
    @enforce_parameter_types
    def power(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Power", value)

    @property
    @exception_bridge
    def power_load_for_pid_control(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "PowerLoadForPIDControl")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @power_load_for_pid_control.setter
    @exception_bridge
    @enforce_parameter_types
    def power_load_for_pid_control(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "PowerLoadForPIDControl", value)

    @property
    @exception_bridge
    def proportion_of_vehicle_weight_carried(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ProportionOfVehicleWeightCarried")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @proportion_of_vehicle_weight_carried.setter
    @exception_bridge
    @enforce_parameter_types
    def proportion_of_vehicle_weight_carried(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ProportionOfVehicleWeightCarried", value)

    @property
    @exception_bridge
    def quadratic_resistance_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "QuadraticResistanceCoefficient")

        if temp is None:
            return 0.0

        return temp

    @quadratic_resistance_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def quadratic_resistance_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "QuadraticResistanceCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def quadratic_resistance_coefficient_time_profile(
        self: "Self",
    ) -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "QuadraticResistanceCoefficientTimeProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @quadratic_resistance_coefficient_time_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def quadratic_resistance_coefficient_time_profile(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "QuadraticResistanceCoefficientTimeProfile", value.wrapped
        )

    @property
    @exception_bridge
    def specified_angle_for_input_torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedAngleForInputTorque")

        if temp is None:
            return 0.0

        return temp

    @specified_angle_for_input_torque.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_angle_for_input_torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedAngleForInputTorque",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def specified_time_for_input_torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedTimeForInputTorque")

        if temp is None:
            return 0.0

        return temp

    @specified_time_for_input_torque.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_time_for_input_torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedTimeForInputTorque",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def speed(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @speed.setter
    @exception_bridge
    @enforce_parameter_types
    def speed(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Speed", value)

    @property
    @exception_bridge
    def speed_vs_time(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "SpeedVsTime")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @speed_vs_time.setter
    @exception_bridge
    @enforce_parameter_types
    def speed_vs_time(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "SpeedVsTime", value.wrapped)

    @property
    @exception_bridge
    def system_deflection_torque_also_applies_to_advanced_system_deflection(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SystemDeflectionTorqueAlsoAppliesToAdvancedSystemDeflection"
        )

        if temp is None:
            return False

        return temp

    @system_deflection_torque_also_applies_to_advanced_system_deflection.setter
    @exception_bridge
    @enforce_parameter_types
    def system_deflection_torque_also_applies_to_advanced_system_deflection(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SystemDeflectionTorqueAlsoAppliesToAdvancedSystemDeflection",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def system_deflection_torque_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.TorqueSpecificationForSystemDeflection]"""
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionTorqueMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @system_deflection_torque_method.setter
    @exception_bridge
    @enforce_parameter_types
    def system_deflection_torque_method(
        self: "Self", value: "_7849.TorqueSpecificationForSystemDeflection"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_TorqueSpecificationForSystemDeflection.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "SystemDeflectionTorqueMethod", value)

    @property
    @exception_bridge
    def target_engine_idle_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TargetEngineIdleSpeed")

        if temp is None:
            return 0.0

        return temp

    @target_engine_idle_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def target_engine_idle_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TargetEngineIdleSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def target_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TargetSpeed")

        if temp is None:
            return 0.0

        return temp

    @target_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def target_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TargetSpeed", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def target_speed_input_type(
        self: "Self",
    ) -> "_2429.PowerLoadPIDControlSpeedInputType":
        """mastapy.system_model.PowerLoadPIDControlSpeedInputType"""
        temp = pythonnet_property_get(self.wrapped, "TargetSpeedInputType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PowerLoadPIDControlSpeedInputType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model._2429", "PowerLoadPIDControlSpeedInputType"
        )(value)

    @target_speed_input_type.setter
    @exception_bridge
    @enforce_parameter_types
    def target_speed_input_type(
        self: "Self", value: "_2429.PowerLoadPIDControlSpeedInputType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PowerLoadPIDControlSpeedInputType"
        )
        pythonnet_property_set(self.wrapped, "TargetSpeedInputType", value)

    @property
    @exception_bridge
    def target_speed_vs_time(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "TargetSpeedVsTime")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @target_speed_vs_time.setter
    @exception_bridge
    @enforce_parameter_types
    def target_speed_vs_time(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "TargetSpeedVsTime", value.wrapped)

    @property
    @exception_bridge
    def torque(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Torque")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @torque.setter
    @exception_bridge
    @enforce_parameter_types
    def torque(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Torque", value)

    @property
    @exception_bridge
    def torque_input_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod":
        """EnumWithSelectedValue[mastapy.system_model.PowerLoadInputTorqueSpecificationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "TorqueInputMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @torque_input_method.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_input_method(
        self: "Self", value: "_2428.PowerLoadInputTorqueSpecificationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "TorqueInputMethod", value)

    @property
    @exception_bridge
    def torque_time_profile_repeats(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "TorqueTimeProfileRepeats")

        if temp is None:
            return False

        return temp

    @torque_time_profile_repeats.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_time_profile_repeats(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TorqueTimeProfileRepeats",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def torque_vs_angle(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "TorqueVsAngle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @torque_vs_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_vs_angle(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "TorqueVsAngle", value.wrapped)

    @property
    @exception_bridge
    def torque_vs_angle_and_speed(self: "Self") -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "TorqueVsAngleAndSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @torque_vs_angle_and_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_vs_angle_and_speed(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "TorqueVsAngleAndSpeed", value.wrapped)

    @property
    @exception_bridge
    def torque_vs_time(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "TorqueVsTime")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @torque_vs_time.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_vs_time(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "TorqueVsTime", value.wrapped)

    @property
    @exception_bridge
    def total_mean_rotor_x_force_over_all_nodes(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalMeanRotorXForceOverAllNodes")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_mean_rotor_y_force_over_all_nodes(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalMeanRotorYForceOverAllNodes")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def unbalanced_magnetic_pull_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UnbalancedMagneticPullStiffness")

        if temp is None:
            return 0.0

        return temp

    @unbalanced_magnetic_pull_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def unbalanced_magnetic_pull_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UnbalancedMagneticPullStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_engine_idle_speed_control(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseEngineIdleSpeedControl")

        if temp is None:
            return False

        return temp

    @use_engine_idle_speed_control.setter
    @exception_bridge
    @enforce_parameter_types
    def use_engine_idle_speed_control(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseEngineIdleSpeedControl",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_time_dependent_constant_resistance_coefficient(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseTimeDependentConstantResistanceCoefficient"
        )

        if temp is None:
            return False

        return temp

    @use_time_dependent_constant_resistance_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def use_time_dependent_constant_resistance_coefficient(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseTimeDependentConstantResistanceCoefficient",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_time_dependent_linear_resistance_coefficient(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseTimeDependentLinearResistanceCoefficient"
        )

        if temp is None:
            return False

        return temp

    @use_time_dependent_linear_resistance_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def use_time_dependent_linear_resistance_coefficient(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseTimeDependentLinearResistanceCoefficient",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_time_dependent_quadratic_resistance_coefficient(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseTimeDependentQuadraticResistanceCoefficient"
        )

        if temp is None:
            return False

        return temp

    @use_time_dependent_quadratic_resistance_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def use_time_dependent_quadratic_resistance_coefficient(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseTimeDependentQuadraticResistanceCoefficient",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_time_dependent_throttle(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseTimeDependentThrottle")

        if temp is None:
            return False

        return temp

    @use_time_dependent_throttle.setter
    @exception_bridge
    @enforce_parameter_types
    def use_time_dependent_throttle(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseTimeDependentThrottle",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def vehicle_speed_to_start_idle_control(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VehicleSpeedToStartIdleControl")

        if temp is None:
            return 0.0

        return temp

    @vehicle_speed_to_start_idle_control.setter
    @exception_bridge
    @enforce_parameter_types
    def vehicle_speed_to_start_idle_control(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VehicleSpeedToStartIdleControl",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def vehicle_speed_to_stop_idle_control(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VehicleSpeedToStopIdleControl")

        if temp is None:
            return 0.0

        return temp

    @vehicle_speed_to_stop_idle_control.setter
    @exception_bridge
    @enforce_parameter_types
    def vehicle_speed_to_stop_idle_control(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VehicleSpeedToStopIdleControl",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def velocity_first_order_lag_cutoff_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "VelocityFirstOrderLagCutoffFrequency"
        )

        if temp is None:
            return 0.0

        return temp

    @velocity_first_order_lag_cutoff_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def velocity_first_order_lag_cutoff_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VelocityFirstOrderLagCutoffFrequency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def velocity_first_order_lag_time_constant(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VelocityFirstOrderLagTimeConstant")

        if temp is None:
            return 0.0

        return temp

    @velocity_first_order_lag_time_constant.setter
    @exception_bridge
    @enforce_parameter_types
    def velocity_first_order_lag_time_constant(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VelocityFirstOrderLagTimeConstant",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_slip_model(self: "Self") -> "_5803.WheelSlipType":
        """mastapy.system_model.analyses_and_results.mbd_analyses.WheelSlipType"""
        temp = pythonnet_property_get(self.wrapped, "WheelSlipModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.WheelSlipType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5803",
            "WheelSlipType",
        )(value)

    @wheel_slip_model.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_slip_model(self: "Self", value: "_5803.WheelSlipType") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.WheelSlipType",
        )
        pythonnet_property_set(self.wrapped, "WheelSlipModel", value)

    @property
    @exception_bridge
    def wheel_static_to_dynamic_friction_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelStaticToDynamicFrictionRatio")

        if temp is None:
            return 0.0

        return temp

    @wheel_static_to_dynamic_friction_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_static_to_dynamic_friction_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelStaticToDynamicFrictionRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_to_vehicle_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelToVehicleStiffness")

        if temp is None:
            return 0.0

        return temp

    @wheel_to_vehicle_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_to_vehicle_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelToVehicleStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def coefficient_of_friction_with_ground(
        self: "Self",
    ) -> "_103.NonDimensionalInputComponent":
        """mastapy.nodal_analysis.varying_input_components.NonDimensionalInputComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFrictionWithGround")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2703.PowerLoad":
        """mastapy.system_model.part_model.PowerLoad

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def engine_idle_speed_control_pid_settings(
        self: "Self",
    ) -> "_1761.PIDControlSettings":
        """mastapy.math_utility.control.PIDControlSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EngineIdleSpeedControlPIDSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pid_control_settings(self: "Self") -> "_1761.PIDControlSettings":
        """mastapy.math_utility.control.PIDControlSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PIDControlSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def get_harmonic_load_data_for_import(
        self: "Self",
    ) -> "_7740.ElectricMachineHarmonicLoadData":
        """mastapy.system_model.analyses_and_results.static_loads.ElectricMachineHarmonicLoadData"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PowerLoadLoadCase":
        """Cast to another type.

        Returns:
            _Cast_PowerLoadLoadCase
        """
        return _Cast_PowerLoadLoadCase(self)
