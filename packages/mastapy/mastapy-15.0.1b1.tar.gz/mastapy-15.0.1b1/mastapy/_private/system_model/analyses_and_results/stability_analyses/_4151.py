"""WormGearSetStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses import _4081

_WORM_GEAR_SET_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "WormGearSetStabilityAnalysis",
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
        _4103,
        _4122,
        _4150,
        _4152,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7856
    from mastapy._private.system_model.part_model.gears import _2790

    Self = TypeVar("Self", bound="WormGearSetStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGearSetStabilityAnalysis._Cast_WormGearSetStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGearSetStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearSetStabilityAnalysis:
    """Special nested class for casting WormGearSetStabilityAnalysis to subclasses."""

    __parent__: "WormGearSetStabilityAnalysis"

    @property
    def gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4081.GearSetStabilityAnalysis":
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
    def worm_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "WormGearSetStabilityAnalysis":
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
class WormGearSetStabilityAnalysis(_4081.GearSetStabilityAnalysis):
    """WormGearSetStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_SET_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2790.WormGearSet":
        """mastapy.system_model.part_model.gears.WormGearSet

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
    def assembly_load_case(self: "Self") -> "_7856.WormGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase

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
    def gears_stability_analysis(
        self: "Self",
    ) -> "List[_4152.WormGearStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.WormGearStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsStabilityAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def worm_gears_stability_analysis(
        self: "Self",
    ) -> "List[_4152.WormGearStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.WormGearStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearsStabilityAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_stability_analysis(
        self: "Self",
    ) -> "List[_4150.WormGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.WormGearMeshStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesStabilityAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def worm_meshes_stability_analysis(
        self: "Self",
    ) -> "List[_4150.WormGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.WormGearMeshStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormMeshesStabilityAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearSetStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_WormGearSetStabilityAnalysis
        """
        return _Cast_WormGearSetStabilityAnalysis(self)
