"""GearManufacturingConfigSetupViewModel"""

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
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical import _726, _727

_GEAR_MANUFACTURING_CONFIG_SETUP_VIEW_MODEL = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "GearManufacturingConfigSetupViewModel",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="GearManufacturingConfigSetupViewModel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearManufacturingConfigSetupViewModel._Cast_GearManufacturingConfigSetupViewModel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearManufacturingConfigSetupViewModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearManufacturingConfigSetupViewModel:
    """Special nested class for casting GearManufacturingConfigSetupViewModel to subclasses."""

    __parent__: "GearManufacturingConfigSetupViewModel"

    @property
    def gear_manufacturing_config_setup_view_model(
        self: "CastSelf",
    ) -> "GearManufacturingConfigSetupViewModel":
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
class GearManufacturingConfigSetupViewModel(_0.APIBase):
    """GearManufacturingConfigSetupViewModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MANUFACTURING_CONFIG_SETUP_VIEW_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def create_new_suitable_cutters(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CreateNewSuitableCutters")

        if temp is None:
            return False

        return temp

    @create_new_suitable_cutters.setter
    @exception_bridge
    @enforce_parameter_types
    def create_new_suitable_cutters(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CreateNewSuitableCutters",
            bool(value) if value is not None else False,
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
    def gear_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def rough_pressure_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RoughPressureAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rough_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def rough_pressure_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RoughPressureAngle", value)

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
    def use_as_design_mode_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseAsDesignModeGeometry")

        if temp is None:
            return False

        return temp

    @use_as_design_mode_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def use_as_design_mode_geometry(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseAsDesignModeGeometry",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearManufacturingConfigSetupViewModel":
        """Cast to another type.

        Returns:
            _Cast_GearManufacturingConfigSetupViewModel
        """
        return _Cast_GearManufacturingConfigSetupViewModel(self)
