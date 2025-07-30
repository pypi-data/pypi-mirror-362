"""PowerLoad"""

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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1387
from mastapy._private.system_model import _2430
from mastapy._private.system_model.part_model import _2711

_POWER_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.materials.efficiency import _387
    from mastapy._private.math_utility.measured_data import _1749
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import (
        _2670,
        _2676,
        _2693,
        _2698,
        _2713,
    )

    Self = TypeVar("Self", bound="PowerLoad")
    CastSelf = TypeVar("CastSelf", bound="PowerLoad._Cast_PowerLoad")


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PowerLoad:
    """Special nested class for casting PowerLoad to subclasses."""

    __parent__: "PowerLoad"

    @property
    def virtual_component(self: "CastSelf") -> "_2711.VirtualComponent":
        return self.__parent__._cast(_2711.VirtualComponent)

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        from mastapy._private.system_model.part_model import _2693

        return self.__parent__._cast(_2693.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        from mastapy._private.system_model.part_model import _2670

        return self.__parent__._cast(_2670.Component)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def power_load(self: "CastSelf") -> "PowerLoad":
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
class PowerLoad(_2711.VirtualComponent):
    """PowerLoad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POWER_LOAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def effective_length_of_stator(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EffectiveLengthOfStator")

        if temp is None:
            return 0.0

        return temp

    @effective_length_of_stator.setter
    @exception_bridge
    @enforce_parameter_types
    def effective_length_of_stator(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EffectiveLengthOfStator",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def electric_machine_detail_selector(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ElectricMachineDetail":
        """ListWithSelectedItem[mastapy.electric_machines.ElectricMachineDetail]"""
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDetailSelector")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ElectricMachineDetail",
        )(temp)

    @electric_machine_detail_selector.setter
    @exception_bridge
    @enforce_parameter_types
    def electric_machine_detail_selector(
        self: "Self", value: "_1387.ElectricMachineDetail"
    ) -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_ElectricMachineDetail.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ElectricMachineDetailSelector", value)

    @property
    @exception_bridge
    def electric_machine_search_region_specification_method(
        self: "Self",
    ) -> "_2676.ElectricMachineSearchRegionSpecificationMethod":
        """mastapy.system_model.part_model.ElectricMachineSearchRegionSpecificationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "ElectricMachineSearchRegionSpecificationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.PartModel.ElectricMachineSearchRegionSpecificationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model._2676",
            "ElectricMachineSearchRegionSpecificationMethod",
        )(value)

    @electric_machine_search_region_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def electric_machine_search_region_specification_method(
        self: "Self", value: "_2676.ElectricMachineSearchRegionSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.PartModel.ElectricMachineSearchRegionSpecificationMethod",
        )
        pythonnet_property_set(
            self.wrapped, "ElectricMachineSearchRegionSpecificationMethod", value
        )

    @property
    @exception_bridge
    def engine_fuel_consumption_grid(self: "Self") -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "EngineFuelConsumptionGrid")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @engine_fuel_consumption_grid.setter
    @exception_bridge
    @enforce_parameter_types
    def engine_fuel_consumption_grid(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "EngineFuelConsumptionGrid", value.wrapped)

    @property
    @exception_bridge
    def engine_torque_grid(self: "Self") -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "EngineTorqueGrid")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @engine_torque_grid.setter
    @exception_bridge
    @enforce_parameter_types
    def engine_torque_grid(self: "Self", value: "_1749.GriddedSurfaceAccessor") -> None:
        pythonnet_property_set(self.wrapped, "EngineTorqueGrid", value.wrapped)

    @property
    @exception_bridge
    def include_in_torsional_stiffness_calculation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeInTorsionalStiffnessCalculation"
        )

        if temp is None:
            return False

        return temp

    @include_in_torsional_stiffness_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def include_in_torsional_stiffness_calculation(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeInTorsionalStiffnessCalculation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def inner_diameter_of_stator_teeth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerDiameterOfStatorTeeth")

        if temp is None:
            return 0.0

        return temp

    @inner_diameter_of_stator_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_diameter_of_stator_teeth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerDiameterOfStatorTeeth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_wheels(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfWheels")

        if temp is None:
            return 0

        return temp

    @number_of_wheels.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_wheels(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfWheels", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_blades(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfBlades")

        if temp is None:
            return 0

        return temp

    @number_of_blades.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_blades(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfBlades", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_slots(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlots")

        if temp is None:
            return 0

        return temp

    @number_of_slots.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_slots(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSlots", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def positive_is_forwards(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PositiveIsForwards")

        if temp is None:
            return False

        return temp

    @positive_is_forwards.setter
    @exception_bridge
    @enforce_parameter_types
    def positive_is_forwards(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PositiveIsForwards",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def power_load_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_PowerLoadType":
        """EnumWithSelectedValue[mastapy.system_model.PowerLoadType]"""
        temp = pythonnet_property_get(self.wrapped, "PowerLoadType")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @power_load_type.setter
    @exception_bridge
    @enforce_parameter_types
    def power_load_type(self: "Self", value: "_2430.PowerLoadType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "PowerLoadType", value)

    @property
    @exception_bridge
    def torsional_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorsionalStiffness")

        if temp is None:
            return 0.0

        return temp

    @torsional_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TorsionalStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tyre_rolling_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TyreRollingRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tyre_rolling_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def tyre_rolling_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TyreRollingRadius", value)

    @property
    @exception_bridge
    def width_for_drawing(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "WidthForDrawing")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @width_for_drawing.setter
    @exception_bridge
    @enforce_parameter_types
    def width_for_drawing(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "WidthForDrawing", value)

    @property
    @exception_bridge
    def electric_machine_detail(self: "Self") -> "_1387.ElectricMachineDetail":
        """mastapy.electric_machines.ElectricMachineDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def oil_pump_detail(self: "Self") -> "_387.OilPumpDetail":
        """mastapy.materials.efficiency.OilPumpDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilPumpDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def single_blade_details(self: "Self") -> "_2713.WindTurbineSingleBladeDetails":
        """mastapy.system_model.part_model.WindTurbineSingleBladeDetails

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SingleBladeDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PowerLoad":
        """Cast to another type.

        Returns:
            _Cast_PowerLoad
        """
        return _Cast_PowerLoad(self)
