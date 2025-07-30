"""CylindricalGearManufacturingConfig"""

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
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1341
from mastapy._private.gears.manufacturing.cylindrical import _726, _727

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CYLINDRICAL_GEAR_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "CylindricalGearManufacturingConfig"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.analysis import _1335, _1338
    from mastapy._private.gears.gear_designs.cylindrical import _1122
    from mastapy._private.gears.gear_designs.cylindrical.thickness_stock_and_backlash import (
        _1202,
    )
    from mastapy._private.gears.manufacturing.cylindrical import _714
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import (
        _836,
        _842,
        _845,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters import _816
    from mastapy._private.gears.manufacturing.cylindrical.process_simulation import _742

    Self = TypeVar("Self", bound="CylindricalGearManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearManufacturingConfig._Cast_CylindricalGearManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearManufacturingConfig:
    """Special nested class for casting CylindricalGearManufacturingConfig to subclasses."""

    __parent__: "CylindricalGearManufacturingConfig"

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1341.GearImplementationDetail":
        return self.__parent__._cast(_1341.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1338

        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def cylindrical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "CylindricalGearManufacturingConfig":
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
class CylindricalGearManufacturingConfig(_1341.GearImplementationDetail):
    """CylindricalGearManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def finish_cutter_database_selector(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "FinishCutterDatabaseSelector", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @finish_cutter_database_selector.setter
    @exception_bridge
    @enforce_parameter_types
    def finish_cutter_database_selector(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "FinishCutterDatabaseSelector",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def finishing_method(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods"
    ):
        """EnumWithSelectedValue[mastapy.gears.manufacturing.cylindrical.CylindricalMftFinishingMethods]"""
        temp = pythonnet_property_get(self.wrapped, "FinishingMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @finishing_method.setter
    @exception_bridge
    @enforce_parameter_types
    def finishing_method(
        self: "Self", value: "_726.CylindricalMftFinishingMethods"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FinishingMethod", value)

    @property
    @exception_bridge
    def limiting_finish_depth_radius_mean(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitingFinishDepthRadiusMean")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_finish_depth_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanFinishDepthRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_finish_cutter_gear_root_clearance_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumFinishCutterGearRootClearanceFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_finish_cutter_gear_root_clearance_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_finish_cutter_gear_root_clearance_factor(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumFinishCutterGearRootClearanceFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_finish_depth_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumFinishDepthRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_points_for_reporting_main_profile_finish_stock(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsForReportingMainProfileFinishStock"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_points_for_reporting_main_profile_finish_stock.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_for_reporting_main_profile_finish_stock(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfPointsForReportingMainProfileFinishStock", value
        )

    @property
    @exception_bridge
    def rough_cutter_database_selector(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "RoughCutterDatabaseSelector", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @rough_cutter_database_selector.setter
    @exception_bridge
    @enforce_parameter_types
    def rough_cutter_database_selector(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "RoughCutterDatabaseSelector",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def roughing_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods":
        """EnumWithSelectedValue[mastapy.gears.manufacturing.cylindrical.CylindricalMftRoughingMethods]"""
        temp = pythonnet_property_get(self.wrapped, "RoughingMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @roughing_method.setter
    @exception_bridge
    @enforce_parameter_types
    def roughing_method(
        self: "Self", value: "_727.CylindricalMftRoughingMethods"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "RoughingMethod", value)

    @property
    @exception_bridge
    def design(self: "Self") -> "_1122.CylindricalGearDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def finish_cutter(self: "Self") -> "_816.CylindricalGearRealCutterDesign":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearRealCutterDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishCutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def finish_cutter_simulation(self: "Self") -> "_842.GearCutterSimulation":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.GearCutterSimulation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishCutterSimulation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def finish_manufacturing_process_controls(
        self: "Self",
    ) -> "_845.ManufacturingProcessControls":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.ManufacturingProcessControls

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FinishManufacturingProcessControls"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def finish_process_simulation(self: "Self") -> "_742.CutterProcessSimulation":
        """mastapy.gears.manufacturing.cylindrical.process_simulation.CutterProcessSimulation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishProcessSimulation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def finish_stock_specification(self: "Self") -> "_1202.FinishStockSpecification":
        """mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash.FinishStockSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishStockSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def finished_gear_specification(
        self: "Self",
    ) -> "_836.CylindricalGearSpecification":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalGearSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishedGearSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_blank(self: "Self") -> "_714.CylindricalGearBlank":
        """mastapy.gears.manufacturing.cylindrical.CylindricalGearBlank

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rough_cutter(self: "Self") -> "_816.CylindricalGearRealCutterDesign":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearRealCutterDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughCutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rough_cutter_simulation(self: "Self") -> "_842.GearCutterSimulation":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.GearCutterSimulation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughCutterSimulation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rough_gear_specification(self: "Self") -> "_836.CylindricalGearSpecification":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.CylindricalGearSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughGearSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rough_manufacturing_process_controls(
        self: "Self",
    ) -> "_845.ManufacturingProcessControls":
        """mastapy.gears.manufacturing.cylindrical.cutter_simulation.ManufacturingProcessControls

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughManufacturingProcessControls")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rough_process_simulation(self: "Self") -> "_742.CutterProcessSimulation":
        """mastapy.gears.manufacturing.cylindrical.process_simulation.CutterProcessSimulation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughProcessSimulation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def create_new_finish_cutter_compatible_with_gear_in_design_mode(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "CreateNewFinishCutterCompatibleWithGearInDesignMode"
        )

    @exception_bridge
    def create_new_rough_cutter_compatible_with_gear_in_design_mode(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "CreateNewRoughCutterCompatibleWithGearInDesignMode"
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearManufacturingConfig
        """
        return _Cast_CylindricalGearManufacturingConfig(self)
