"""KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses import _4089

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4020,
        _4053,
        _4081,
        _4091,
        _4093,
        _4103,
        _4122,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7786
    from mastapy._private.system_model.part_model.gears import _2776

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4089.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis":
        return self.__parent__._cast(
            _4089.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis
        )

    @property
    def conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4053.ConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4053,
        )

        return self.__parent__._cast(_4053.ConicalGearSetStabilityAnalysis)

    @property
    def gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4081.GearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4081,
        )

        return self.__parent__._cast(_4081.GearSetStabilityAnalysis)

    @property
    def specialised_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_4122.SpecialisedAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4122,
        )

        return self.__parent__._cast(_4122.SpecialisedAssemblyStabilityAnalysis)

    @property
    def abstract_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_4020.AbstractAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4020,
        )

        return self.__parent__._cast(_4020.AbstractAssemblyStabilityAnalysis)

    @property
    def part_stability_analysis(self: "CastSelf") -> "_4103.PartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4103,
        )

        return self.__parent__._cast(_4103.PartStabilityAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis":
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
class KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis(
    _4089.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis
):
    """KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STABILITY_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2776.KlingelnbergCycloPalloidHypoidGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet

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
    def assembly_load_case(
        self: "Self",
    ) -> "_7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_conical_gears_stability_analysis(
        self: "Self",
    ) -> "List[_4093.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalGearsStabilityAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_gears_stability_analysis(
        self: "Self",
    ) -> "List[_4093.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearsStabilityAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_conical_meshes_stability_analysis(
        self: "Self",
    ) -> "List[_4091.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalMeshesStabilityAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_meshes_stability_analysis(
        self: "Self",
    ) -> "List[_4091.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidMeshesStabilityAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis(self)
