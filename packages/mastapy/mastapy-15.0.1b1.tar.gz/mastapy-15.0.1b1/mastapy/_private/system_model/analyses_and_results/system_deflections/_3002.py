"""GearSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _3025

_GEAR_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "GearSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1744
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7889,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4355
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2932,
        _2944,
        _2945,
        _2946,
        _2949,
        _2956,
        _2963,
        _2967,
        _2986,
        _2987,
        _2988,
        _2991,
        _2997,
        _3001,
        _3006,
        _3011,
        _3014,
        _3017,
        _3028,
        _3052,
        _3058,
        _3061,
        _3062,
        _3063,
        _3081,
        _3084,
    )
    from mastapy._private.system_model.part_model.gears import _2767

    Self = TypeVar("Self", bound="GearSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSystemDeflection._Cast_GearSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSystemDeflection:
    """Special nested class for casting GearSystemDeflection to subclasses."""

    __parent__: "GearSystemDeflection"

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_3025.MountableComponentSystemDeflection":
        return self.__parent__._cast(_3025.MountableComponentSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2956.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2956,
        )

        return self.__parent__._cast(_2956.ComponentSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_3028.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3028,
        )

        return self.__parent__._cast(_3028.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7889.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7889,
        )

        return self.__parent__._cast(_7889.PartFEAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7890,
        )

        return self.__parent__._cast(_7890.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.PartAnalysisCase)

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
    def agma_gleason_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2932.AGMAGleasonConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2932,
        )

        return self.__parent__._cast(_2932.AGMAGleasonConicalGearSystemDeflection)

    @property
    def bevel_differential_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2944.BevelDifferentialGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2944,
        )

        return self.__parent__._cast(_2944.BevelDifferentialGearSystemDeflection)

    @property
    def bevel_differential_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2945.BevelDifferentialPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2945,
        )

        return self.__parent__._cast(_2945.BevelDifferentialPlanetGearSystemDeflection)

    @property
    def bevel_differential_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2946.BevelDifferentialSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2946,
        )

        return self.__parent__._cast(_2946.BevelDifferentialSunGearSystemDeflection)

    @property
    def bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2949.BevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2949,
        )

        return self.__parent__._cast(_2949.BevelGearSystemDeflection)

    @property
    def concept_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2963.ConceptGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2963,
        )

        return self.__parent__._cast(_2963.ConceptGearSystemDeflection)

    @property
    def conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2967.ConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2967,
        )

        return self.__parent__._cast(_2967.ConicalGearSystemDeflection)

    @property
    def cylindrical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2986.CylindricalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2986,
        )

        return self.__parent__._cast(_2986.CylindricalGearSystemDeflection)

    @property
    def cylindrical_gear_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2987.CylindricalGearSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2987,
        )

        return self.__parent__._cast(_2987.CylindricalGearSystemDeflectionTimestep)

    @property
    def cylindrical_gear_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2988.CylindricalGearSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2988,
        )

        return self.__parent__._cast(
            _2988.CylindricalGearSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2991.CylindricalPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2991,
        )

        return self.__parent__._cast(_2991.CylindricalPlanetGearSystemDeflection)

    @property
    def face_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2997.FaceGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2997,
        )

        return self.__parent__._cast(_2997.FaceGearSystemDeflection)

    @property
    def hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3006.HypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3006,
        )

        return self.__parent__._cast(_3006.HypoidGearSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3011.KlingelnbergCycloPalloidConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3011,
        )

        return self.__parent__._cast(
            _3011.KlingelnbergCycloPalloidConicalGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3014.KlingelnbergCycloPalloidHypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3014,
        )

        return self.__parent__._cast(
            _3014.KlingelnbergCycloPalloidHypoidGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3017.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3017,
        )

        return self.__parent__._cast(
            _3017.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
        )

    @property
    def spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3052.SpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3052,
        )

        return self.__parent__._cast(_3052.SpiralBevelGearSystemDeflection)

    @property
    def straight_bevel_diff_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3058.StraightBevelDiffGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3058,
        )

        return self.__parent__._cast(_3058.StraightBevelDiffGearSystemDeflection)

    @property
    def straight_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3061.StraightBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3061,
        )

        return self.__parent__._cast(_3061.StraightBevelGearSystemDeflection)

    @property
    def straight_bevel_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3062.StraightBevelPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3062,
        )

        return self.__parent__._cast(_3062.StraightBevelPlanetGearSystemDeflection)

    @property
    def straight_bevel_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3063.StraightBevelSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3063,
        )

        return self.__parent__._cast(_3063.StraightBevelSunGearSystemDeflection)

    @property
    def worm_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3081.WormGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3081,
        )

        return self.__parent__._cast(_3081.WormGearSystemDeflection)

    @property
    def zerol_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_3084.ZerolBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3084,
        )

        return self.__parent__._cast(_3084.ZerolBevelGearSystemDeflection)

    @property
    def gear_system_deflection(self: "CastSelf") -> "GearSystemDeflection":
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
class GearSystemDeflection(_3025.MountableComponentSystemDeflection):
    """GearSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def is_loaded(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLoaded")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2767.Gear":
        """mastapy.system_model.part_model.gears.Gear

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
    def mesh_point_results_in_wcs(
        self: "Self",
    ) -> "List[_1744.ForceAndDisplacementResults]":
        """List[mastapy.math_utility.measured_vectors.ForceAndDisplacementResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshPointResultsInWCS")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_set(self: "Self") -> "_3001.GearSetSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.GearSetSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def power_flow_results(self: "Self") -> "_4355.GearPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.GearPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_GearSystemDeflection
        """
        return _Cast_GearSystemDeflection(self)
