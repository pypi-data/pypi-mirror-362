"""CylindricalGearCuttingOptions"""

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
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1160

_CYLINDRICAL_GEAR_CUTTING_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearCuttingOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1116, _1141
    from mastapy._private.gears.manufacturing.cylindrical import _715

    Self = TypeVar("Self", bound="CylindricalGearCuttingOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearCuttingOptions._Cast_CylindricalGearCuttingOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearCuttingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearCuttingOptions:
    """Special nested class for casting CylindricalGearCuttingOptions to subclasses."""

    __parent__: "CylindricalGearCuttingOptions"

    @property
    def cylindrical_gear_cutting_options(
        self: "CastSelf",
    ) -> "CylindricalGearCuttingOptions":
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
class CylindricalGearCuttingOptions(_0.APIBase):
    """CylindricalGearCuttingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_CUTTING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def geometry_specification_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_GeometrySpecificationType":
        """EnumWithSelectedValue[mastapy.gears.gear_designs.cylindrical.GeometrySpecificationType]"""
        temp = pythonnet_property_get(self.wrapped, "GeometrySpecificationType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_GeometrySpecificationType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @geometry_specification_type.setter
    @exception_bridge
    @enforce_parameter_types
    def geometry_specification_type(
        self: "Self", value: "_1160.GeometrySpecificationType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GeometrySpecificationType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "GeometrySpecificationType", value)

    @property
    @exception_bridge
    def thickness_for_analyses(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "ThicknessForAnalyses")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @thickness_for_analyses.setter
    @exception_bridge
    @enforce_parameter_types
    def thickness_for_analyses(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ThicknessForAnalyses", value)

    @property
    @exception_bridge
    def use_design_default_toleranced_measurement(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseDesignDefaultTolerancedMeasurement"
        )

        if temp is None:
            return False

        return temp

    @use_design_default_toleranced_measurement.setter
    @exception_bridge
    @enforce_parameter_types
    def use_design_default_toleranced_measurement(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDesignDefaultTolerancedMeasurement",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def cylindrical_gear_cutter(self: "Self") -> "_1116.CylindricalGearAbstractRack":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearAbstractRack

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearCutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def manufacturing_configuration(
        self: "Self",
    ) -> "_715.CylindricalGearManufacturingConfig":
        """mastapy.gears.manufacturing.cylindrical.CylindricalGearManufacturingConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ManufacturingConfiguration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def manufacturing_configuration_selection(
        self: "Self",
    ) -> "_1141.CylindricalGearSetManufacturingConfigurationSelection":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetManufacturingConfigurationSelection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ManufacturingConfigurationSelection"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearCuttingOptions":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearCuttingOptions
        """
        return _Cast_CylindricalGearCuttingOptions(self)
