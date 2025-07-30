"""PlasticCylindricalGearMaterial"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
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
from mastapy._private.gears.materials import _684

_PLASTIC_CYLINDRICAL_GEAR_MATERIAL = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "PlasticCylindricalGearMaterial"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.materials import _688
    from mastapy._private.materials import _358
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="PlasticCylindricalGearMaterial")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlasticCylindricalGearMaterial._Cast_PlasticCylindricalGearMaterial",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlasticCylindricalGearMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlasticCylindricalGearMaterial:
    """Special nested class for casting PlasticCylindricalGearMaterial to subclasses."""

    __parent__: "PlasticCylindricalGearMaterial"

    @property
    def cylindrical_gear_material(self: "CastSelf") -> "_684.CylindricalGearMaterial":
        return self.__parent__._cast(_684.CylindricalGearMaterial)

    @property
    def gear_material(self: "CastSelf") -> "_688.GearMaterial":
        from mastapy._private.gears.materials import _688

        return self.__parent__._cast(_688.GearMaterial)

    @property
    def material(self: "CastSelf") -> "_358.Material":
        from mastapy._private.materials import _358

        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def plastic_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "PlasticCylindricalGearMaterial":
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
class PlasticCylindricalGearMaterial(_684.CylindricalGearMaterial):
    """PlasticCylindricalGearMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLASTIC_CYLINDRICAL_GEAR_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def glass_transition_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GlassTransitionTemperature")

        if temp is None:
            return 0.0

        return temp

    @glass_transition_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def glass_transition_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GlassTransitionTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def material_type(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "MaterialType")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @material_type.setter
    @exception_bridge
    @enforce_parameter_types
    def material_type(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "MaterialType", value)

    @property
    @exception_bridge
    def melting_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeltingTemperature")

        if temp is None:
            return 0.0

        return temp

    @melting_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def melting_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeltingTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def modulus_of_elasticity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ModulusOfElasticity")

        if temp is None:
            return 0.0

        return temp

    @modulus_of_elasticity.setter
    @exception_bridge
    @enforce_parameter_types
    def modulus_of_elasticity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModulusOfElasticity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def n0_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "N0Bending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def n0_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "N0Contact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_temperature_for_continuous_operation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleTemperatureForContinuousOperation"
        )

        if temp is None:
            return 0.0

        return temp

    @permissible_temperature_for_continuous_operation.setter
    @exception_bridge
    @enforce_parameter_types
    def permissible_temperature_for_continuous_operation(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PermissibleTemperatureForContinuousOperation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def permissible_temperature_for_intermittent_operation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleTemperatureForIntermittentOperation"
        )

        if temp is None:
            return 0.0

        return temp

    @permissible_temperature_for_intermittent_operation.setter
    @exception_bridge
    @enforce_parameter_types
    def permissible_temperature_for_intermittent_operation(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PermissibleTemperatureForIntermittentOperation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_custom_material_for_bending(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseCustomMaterialForBending")

        if temp is None:
            return False

        return temp

    @use_custom_material_for_bending.setter
    @exception_bridge
    @enforce_parameter_types
    def use_custom_material_for_bending(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseCustomMaterialForBending",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_custom_material_for_contact(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseCustomMaterialForContact")

        if temp is None:
            return False

        return temp

    @use_custom_material_for_contact.setter
    @exception_bridge
    @enforce_parameter_types
    def use_custom_material_for_contact(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseCustomMaterialForContact",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PlasticCylindricalGearMaterial":
        """Cast to another type.

        Returns:
            _Cast_PlasticCylindricalGearMaterial
        """
        return _Cast_PlasticCylindricalGearMaterial(self)
