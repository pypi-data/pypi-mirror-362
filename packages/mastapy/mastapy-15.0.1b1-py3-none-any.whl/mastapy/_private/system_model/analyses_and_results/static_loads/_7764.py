"""GearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7792, _7823

_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearSetLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7131,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5722
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7675,
        _7684,
        _7693,
        _7698,
        _7712,
        _7717,
        _7734,
        _7755,
        _7759,
        _7761,
        _7776,
        _7783,
        _7786,
        _7789,
        _7799,
        _7804,
        _7826,
        _7832,
        _7835,
        _7856,
        _7859,
    )
    from mastapy._private.system_model.part_model.gears import _2769

    Self = TypeVar("Self", bound="GearSetLoadCase")
    CastSelf = TypeVar("CastSelf", bound="GearSetLoadCase._Cast_GearSetLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("GearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetLoadCase:
    """Special nested class for casting GearSetLoadCase to subclasses."""

    __parent__: "GearSetLoadCase"

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7823.SpecialisedAssemblyLoadCase":
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
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7684.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7684,
        )

        return self.__parent__._cast(_7684.AGMAGleasonConicalGearSetLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7693.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7693,
        )

        return self.__parent__._cast(_7693.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_7698.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7698,
        )

        return self.__parent__._cast(_7698.BevelGearSetLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_7712.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConceptGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_7717.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7717,
        )

        return self.__parent__._cast(_7717.ConicalGearSetLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7734.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7734,
        )

        return self.__parent__._cast(_7734.CylindricalGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7755.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7755,
        )

        return self.__parent__._cast(_7755.FaceGearSetLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7776.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7776,
        )

        return self.__parent__._cast(_7776.HypoidGearSetLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7783.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7783,
        )

        return self.__parent__._cast(
            _7783.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7786,
        )

        return self.__parent__._cast(
            _7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7789,
        )

        return self.__parent__._cast(
            _7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        )

    @property
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7804.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7804,
        )

        return self.__parent__._cast(_7804.PlanetaryGearSetLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7826.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7826,
        )

        return self.__parent__._cast(_7826.SpiralBevelGearSetLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7832.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7832,
        )

        return self.__parent__._cast(_7832.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7835.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7835,
        )

        return self.__parent__._cast(_7835.StraightBevelGearSetLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7856.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7856,
        )

        return self.__parent__._cast(_7856.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7859.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7859,
        )

        return self.__parent__._cast(_7859.ZerolBevelGearSetLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "GearSetLoadCase":
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
class GearSetLoadCase(_7823.SpecialisedAssemblyLoadCase):
    """GearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def excitation_data_is_up_to_date(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationDataIsUpToDate")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def gear_mesh_stiffness_model(self: "Self") -> "_5722.GearMeshStiffnessModel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.GearMeshStiffnessModel"""
        temp = pythonnet_property_get(self.wrapped, "GearMeshStiffnessModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.GearMeshStiffnessModel",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5722",
            "GearMeshStiffnessModel",
        )(value)

    @gear_mesh_stiffness_model.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_mesh_stiffness_model(
        self: "Self", value: "_5722.GearMeshStiffnessModel"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.GearMeshStiffnessModel",
        )
        pythonnet_property_set(self.wrapped, "GearMeshStiffnessModel", value)

    @property
    @exception_bridge
    def include_microgeometry(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "IncludeMicrogeometry")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @include_microgeometry.setter
    @exception_bridge
    @enforce_parameter_types
    def include_microgeometry(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IncludeMicrogeometry", value)

    @property
    @exception_bridge
    def mesh_stiffness_source(
        self: "Self",
    ) -> "overridable.Overridable_MeshStiffnessSource":
        """Overridable[mastapy.system_model.analyses_and_results.static_loads.MeshStiffnessSource]"""
        temp = pythonnet_property_get(self.wrapped, "MeshStiffnessSource")

        if temp is None:
            return None

        value = overridable.Overridable_MeshStiffnessSource.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @mesh_stiffness_source.setter
    @exception_bridge
    @enforce_parameter_types
    def mesh_stiffness_source(
        self: "Self",
        value: "Union[_7792.MeshStiffnessSource, Tuple[_7792.MeshStiffnessSource, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_MeshStiffnessSource.wrapper_type()
        enclosed_type = overridable.Overridable_MeshStiffnessSource.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MeshStiffnessSource", value)

    @property
    @exception_bridge
    def override_mesh_efficiency_script(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideMeshEfficiencyScript")

        if temp is None:
            return False

        return temp

    @override_mesh_efficiency_script.setter
    @exception_bridge
    @enforce_parameter_types
    def override_mesh_efficiency_script(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideMeshEfficiencyScript",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_advanced_model_in_advanced_time_stepping_analysis_for_modulation(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseAdvancedModelInAdvancedTimeSteppingAnalysisForModulation"
        )

        if temp is None:
            return False

        return temp

    @use_advanced_model_in_advanced_time_stepping_analysis_for_modulation.setter
    @exception_bridge
    @enforce_parameter_types
    def use_advanced_model_in_advanced_time_stepping_analysis_for_modulation(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseAdvancedModelInAdvancedTimeSteppingAnalysisForModulation",
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
    def advanced_time_stepping_analysis_for_modulation_options(
        self: "Self",
    ) -> "_7131.AdvancedTimeSteppingAnalysisForModulationOptions":
        """mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.AdvancedTimeSteppingAnalysisForModulationOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AdvancedTimeSteppingAnalysisForModulationOptions"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2769.GearSet":
        """mastapy.system_model.part_model.gears.GearSet

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
    def gears_load_case(self: "Self") -> "List[_7759.GearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.GearLoadCase]

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
    def gears_without_clones(self: "Self") -> "List[_7759.GearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.GearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsWithoutClones")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_load_case(self: "Self") -> "List[_7761.GearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase]

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
    def meshes_without_planetary_duplicates(
        self: "Self",
    ) -> "List[_7761.GearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesWithoutPlanetaryDuplicates")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_GearSetLoadCase
        """
        return _Cast_GearSetLoadCase(self)
