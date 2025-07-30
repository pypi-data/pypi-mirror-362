"""SimpleShaftDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _2028

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_SIMPLE_SHAFT_DEFINITION = python_net_import(
    "SMT.MastaAPI.Shafts", "SimpleShaftDefinition"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.shafts import _9, _14, _22, _26, _30, _36, _44, _45

    Self = TypeVar("Self", bound="SimpleShaftDefinition")
    CastSelf = TypeVar(
        "CastSelf", bound="SimpleShaftDefinition._Cast_SimpleShaftDefinition"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SimpleShaftDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SimpleShaftDefinition:
    """Special nested class for casting SimpleShaftDefinition to subclasses."""

    __parent__: "SimpleShaftDefinition"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def simple_shaft_definition(self: "CastSelf") -> "SimpleShaftDefinition":
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
class SimpleShaftDefinition(_2028.NamedDatabaseItem):
    """SimpleShaftDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SIMPLE_SHAFT_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def default_fillet_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DefaultFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @default_fillet_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def default_fillet_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DefaultFilletRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def design_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def factor_for_gjl_material(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FactorForGJLMaterial")

        if temp is None:
            return 0.0

        return temp

    @factor_for_gjl_material.setter
    @exception_bridge
    @enforce_parameter_types
    def factor_for_gjl_material(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FactorForGJLMaterial",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "Material", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @material.setter
    @exception_bridge
    @enforce_parameter_types
    def material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "Material",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def override_default_shaft_material(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideDefaultShaftMaterial")

        if temp is None:
            return False

        return temp

    @override_default_shaft_material.setter
    @exception_bridge
    @enforce_parameter_types
    def override_default_shaft_material(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDefaultShaftMaterial",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def report_shaft_fatigue_warnings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ReportShaftFatigueWarnings")

        if temp is None:
            return False

        return temp

    @report_shaft_fatigue_warnings.setter
    @exception_bridge
    @enforce_parameter_types
    def report_shaft_fatigue_warnings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReportShaftFatigueWarnings",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def surface_treatment_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceTreatmentFactor")

        if temp is None:
            return 0.0

        return temp

    @surface_treatment_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def surface_treatment_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SurfaceTreatmentFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def default_surface_roughness(self: "Self") -> "_45.ShaftSurfaceRoughness":
        """mastapy.shafts.ShaftSurfaceRoughness

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DefaultSurfaceRoughness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_profile(self: "Self") -> "_30.ShaftProfile":
        """mastapy.shafts.ShaftProfile

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def outer_profile(self: "Self") -> "_30.ShaftProfile":
        """mastapy.shafts.ShaftProfile

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_material(self: "Self") -> "_26.ShaftMaterialForReports":
        """mastapy.shafts.ShaftMaterialForReports

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def design_shaft_sections(self: "Self") -> "List[_9.DesignShaftSection]":
        """List[mastapy.shafts.DesignShaftSection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignShaftSections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def generic_stress_concentration_factors(
        self: "Self",
    ) -> "List[_14.GenericStressConcentrationFactor]":
        """List[mastapy.shafts.GenericStressConcentrationFactor]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GenericStressConcentrationFactors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def grooves(self: "Self") -> "List[_22.ShaftGroove]":
        """List[mastapy.shafts.ShaftGroove]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Grooves")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def radial_holes(self: "Self") -> "List[_36.ShaftRadialHole]":
        """List[mastapy.shafts.ShaftRadialHole]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialHoles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def surface_finish_sections(self: "Self") -> "List[_44.ShaftSurfaceFinishSection]":
        """List[mastapy.shafts.ShaftSurfaceFinishSection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceFinishSections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def add_generic_stress_concentration_factor(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddGenericStressConcentrationFactor")

    @exception_bridge
    def add_generic_stress_concentration_factor_for_context_menu(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "AddGenericStressConcentrationFactorForContextMenu"
        )

    @exception_bridge
    def add_groove(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddGroove")

    @exception_bridge
    def add_groove_for_context_menu(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddGrooveForContextMenu")

    @exception_bridge
    def add_radial_hole(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddRadialHole")

    @exception_bridge
    def add_radial_hole_for_context_menu(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddRadialHoleForContextMenu")

    @exception_bridge
    def add_surface_finish_section(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddSurfaceFinishSection")

    @exception_bridge
    def add_surface_finish_section_for_context_menu(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddSurfaceFinishSectionForContextMenu")

    @property
    def cast_to(self: "Self") -> "_Cast_SimpleShaftDefinition":
        """Cast to another type.

        Returns:
            _Cast_SimpleShaftDefinition
        """
        return _Cast_SimpleShaftDefinition(self)
