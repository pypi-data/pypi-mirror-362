"""CylindricalGearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears import _408, _427, _431
from mastapy._private.gears.rating import _450
from mastapy._private.system_model.analyses_and_results.static_loads import _7764

_CYLINDRICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CylindricalGearSetLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1169
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1220
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7675,
        _7730,
        _7732,
        _7733,
        _7799,
        _7804,
        _7812,
        _7823,
    )
    from mastapy._private.system_model.part_model.gears import _2763

    Self = TypeVar("Self", bound="CylindricalGearSetLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearSetLoadCase._Cast_CylindricalGearSetLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetLoadCase:
    """Special nested class for casting CylindricalGearSetLoadCase to subclasses."""

    __parent__: "CylindricalGearSetLoadCase"

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7764.GearSetLoadCase":
        return self.__parent__._cast(_7764.GearSetLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7823.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7823,
        )

        return self.__parent__._cast(_7823.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_7675.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7675,
        )

        return self.__parent__._cast(_7675.AbstractAssemblyLoadCase)

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
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7804.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7804,
        )

        return self.__parent__._cast(_7804.PlanetaryGearSetLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "CylindricalGearSetLoadCase":
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
class CylindricalGearSetLoadCase(_7764.GearSetLoadCase):
    """CylindricalGearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def boost_pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BoostPressure")

        if temp is None:
            return 0.0

        return temp

    @boost_pressure.setter
    @exception_bridge
    @enforce_parameter_types
    def boost_pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BoostPressure", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def coefficient_of_friction_calculation_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod":
        """EnumWithSelectedValue[mastapy.gears.CoefficientOfFrictionCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionCalculationMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @coefficient_of_friction_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_calculation_method(
        self: "Self", value: "_408.CoefficientOfFrictionCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "CoefficientOfFrictionCalculationMethod", value
        )

    @property
    @exception_bridge
    def dynamic_load_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DynamicLoadFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_load_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_load_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DynamicLoadFactor", value)

    @property
    @exception_bridge
    def efficiency_rating_method(
        self: "Self",
    ) -> "overridable.Overridable_GearMeshEfficiencyRatingMethod":
        """Overridable[mastapy.gears.rating.GearMeshEfficiencyRatingMethod]"""
        temp = pythonnet_property_get(self.wrapped, "EfficiencyRatingMethod")

        if temp is None:
            return None

        value = overridable.Overridable_GearMeshEfficiencyRatingMethod.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @efficiency_rating_method.setter
    @exception_bridge
    @enforce_parameter_types
    def efficiency_rating_method(
        self: "Self",
        value: "Union[_450.GearMeshEfficiencyRatingMethod, Tuple[_450.GearMeshEfficiencyRatingMethod, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_GearMeshEfficiencyRatingMethod.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_GearMeshEfficiencyRatingMethod.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EfficiencyRatingMethod", value)

    @property
    @exception_bridge
    def micro_geometry_model_for_simple_mesh_stiffness(
        self: "Self",
    ) -> "overridable.Overridable_MicroGeometryModel":
        """Overridable[mastapy.gears.MicroGeometryModel]"""
        temp = pythonnet_property_get(
            self.wrapped, "MicroGeometryModelForSimpleMeshStiffness"
        )

        if temp is None:
            return None

        value = overridable.Overridable_MicroGeometryModel.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @micro_geometry_model_for_simple_mesh_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def micro_geometry_model_for_simple_mesh_stiffness(
        self: "Self",
        value: "Union[_427.MicroGeometryModel, Tuple[_427.MicroGeometryModel, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_MicroGeometryModel.wrapper_type()
        enclosed_type = overridable.Overridable_MicroGeometryModel.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MicroGeometryModelForSimpleMeshStiffness", value
        )

    @property
    @exception_bridge
    def override_micro_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideMicroGeometry")

        if temp is None:
            return False

        return temp

    @override_micro_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def override_micro_geometry(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideMicroGeometry",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def planetary_rating_load_sharing_method(
        self: "Self",
    ) -> "overridable.Overridable_PlanetaryRatingLoadSharingOption":
        """Overridable[mastapy.gears.PlanetaryRatingLoadSharingOption]"""
        temp = pythonnet_property_get(self.wrapped, "PlanetaryRatingLoadSharingMethod")

        if temp is None:
            return None

        value = overridable.Overridable_PlanetaryRatingLoadSharingOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @planetary_rating_load_sharing_method.setter
    @exception_bridge
    @enforce_parameter_types
    def planetary_rating_load_sharing_method(
        self: "Self",
        value: "Union[_431.PlanetaryRatingLoadSharingOption, Tuple[_431.PlanetaryRatingLoadSharingOption, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_PlanetaryRatingLoadSharingOption.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_PlanetaryRatingLoadSharingOption.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PlanetaryRatingLoadSharingMethod", value)

    @property
    @exception_bridge
    def reset_micro_geometry(self: "Self") -> "_7812.ResetMicroGeometryOptions":
        """mastapy.system_model.analyses_and_results.static_loads.ResetMicroGeometryOptions"""
        temp = pythonnet_property_get(self.wrapped, "ResetMicroGeometry")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.ResetMicroGeometryOptions",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads._7812",
            "ResetMicroGeometryOptions",
        )(value)

    @reset_micro_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def reset_micro_geometry(
        self: "Self", value: "_7812.ResetMicroGeometryOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.ResetMicroGeometryOptions",
        )
        pythonnet_property_set(self.wrapped, "ResetMicroGeometry", value)

    @property
    @exception_bridge
    def use_design_coefficient_of_friction_calculation_method(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseDesignCoefficientOfFrictionCalculationMethod"
        )

        if temp is None:
            return False

        return temp

    @use_design_coefficient_of_friction_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def use_design_coefficient_of_friction_calculation_method(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDesignCoefficientOfFrictionCalculationMethod",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_design_default_ltca_settings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDesignDefaultLTCASettings")

        if temp is None:
            return False

        return temp

    @use_design_default_ltca_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def use_design_default_ltca_settings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDesignDefaultLTCASettings",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_script_to_provide_mesh_efficiency(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "UseScriptToProvideMeshEfficiency")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_script_to_provide_mesh_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def use_script_to_provide_mesh_efficiency(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UseScriptToProvideMeshEfficiency", value)

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2763.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ltca(self: "Self") -> "_1169.LTCALoadCaseModifiableSettings":
        """mastapy.gears.gear_designs.cylindrical.LTCALoadCaseModifiableSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LTCA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def overridable_micro_geometry(
        self: "Self",
    ) -> "_1220.CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverridableMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gears_load_case(self: "Self") -> "List[_7730.CylindricalGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_gears_load_case(
        self: "Self",
    ) -> "List[_7730.CylindricalGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_load_case(self: "Self") -> "List[_7732.CylindricalGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_meshes_load_case(
        self: "Self",
    ) -> "List[_7732.CylindricalGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def get_harmonic_load_data_for_import(
        self: "Self",
    ) -> "_7733.CylindricalGearSetHarmonicLoadData":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetHarmonicLoadData"""
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
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetLoadCase
        """
        return _Cast_CylindricalGearSetLoadCase(self)
