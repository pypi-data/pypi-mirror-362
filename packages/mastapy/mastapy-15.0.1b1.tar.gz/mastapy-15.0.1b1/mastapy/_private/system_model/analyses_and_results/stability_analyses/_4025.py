"""AGMAGleasonConicalGearSetStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses import _4053

_AGMA_GLEASON_CONICAL_GEAR_SET_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "AGMAGleasonConicalGearSetStabilityAnalysis",
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
        _4024,
        _4026,
        _4032,
        _4037,
        _4081,
        _4085,
        _4103,
        _4122,
        _4124,
        _4133,
        _4136,
        _4154,
    )
    from mastapy._private.system_model.part_model.gears import _2751

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSetStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearSetStabilityAnalysis._Cast_AGMAGleasonConicalGearSetStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSetStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSetStabilityAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearSetStabilityAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearSetStabilityAnalysis"

    @property
    def conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4053.ConicalGearSetStabilityAnalysis":
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
    def bevel_differential_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4032.BevelDifferentialGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4032,
        )

        return self.__parent__._cast(_4032.BevelDifferentialGearSetStabilityAnalysis)

    @property
    def bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4037.BevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4037,
        )

        return self.__parent__._cast(_4037.BevelGearSetStabilityAnalysis)

    @property
    def hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4085.HypoidGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4085,
        )

        return self.__parent__._cast(_4085.HypoidGearSetStabilityAnalysis)

    @property
    def spiral_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4124.SpiralBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4124,
        )

        return self.__parent__._cast(_4124.SpiralBevelGearSetStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4133.StraightBevelDiffGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4133,
        )

        return self.__parent__._cast(_4133.StraightBevelDiffGearSetStabilityAnalysis)

    @property
    def straight_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4136.StraightBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4136,
        )

        return self.__parent__._cast(_4136.StraightBevelGearSetStabilityAnalysis)

    @property
    def zerol_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4154.ZerolBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4154,
        )

        return self.__parent__._cast(_4154.ZerolBevelGearSetStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearSetStabilityAnalysis":
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
class AGMAGleasonConicalGearSetStabilityAnalysis(_4053.ConicalGearSetStabilityAnalysis):
    """AGMAGleasonConicalGearSetStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_SET_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2751.AGMAGleasonConicalGearSet":
        """mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet

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
    def conical_gears_stability_analysis(
        self: "Self",
    ) -> "List[_4026.AGMAGleasonConicalGearStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AGMAGleasonConicalGearStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearsStabilityAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def agma_gleason_conical_gears_stability_analysis(
        self: "Self",
    ) -> "List[_4026.AGMAGleasonConicalGearStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AGMAGleasonConicalGearStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalGearsStabilityAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def conical_meshes_stability_analysis(
        self: "Self",
    ) -> "List[_4024.AGMAGleasonConicalGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AGMAGleasonConicalGearMeshStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshesStabilityAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def agma_gleason_conical_meshes_stability_analysis(
        self: "Self",
    ) -> "List[_4024.AGMAGleasonConicalGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AGMAGleasonConicalGearMeshStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalMeshesStabilityAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearSetStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSetStabilityAnalysis
        """
        return _Cast_AGMAGleasonConicalGearSetStabilityAnalysis(self)
