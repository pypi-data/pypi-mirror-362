"""GearSetModalAnalysisAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5497,
)

_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "GearSetModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5396,
        _5402,
        _5409,
        _5414,
        _5427,
        _5430,
        _5445,
        _5451,
        _5454,
        _5455,
        _5460,
        _5464,
        _5467,
        _5470,
        _5478,
        _5483,
        _5500,
        _5506,
        _5509,
        _5524,
        _5527,
    )
    from mastapy._private.system_model.part_model.gears import _2769

    Self = TypeVar("Self", bound="GearSetModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetModalAnalysisAtASpeed._Cast_GearSetModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetModalAnalysisAtASpeed:
    """Special nested class for casting GearSetModalAnalysisAtASpeed to subclasses."""

    __parent__: "GearSetModalAnalysisAtASpeed"

    @property
    def specialised_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5497.SpecialisedAssemblyModalAnalysisAtASpeed":
        return self.__parent__._cast(_5497.SpecialisedAssemblyModalAnalysisAtASpeed)

    @property
    def abstract_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5396.AbstractAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5396,
        )

        return self.__parent__._cast(_5396.AbstractAssemblyModalAnalysisAtASpeed)

    @property
    def part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5478.PartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5478,
        )

        return self.__parent__._cast(_5478.PartModalAnalysisAtASpeed)

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
    def agma_gleason_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5402.AGMAGleasonConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5402,
        )

        return self.__parent__._cast(
            _5402.AGMAGleasonConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5409.BevelDifferentialGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5409,
        )

        return self.__parent__._cast(
            _5409.BevelDifferentialGearSetModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5414.BevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5414,
        )

        return self.__parent__._cast(_5414.BevelGearSetModalAnalysisAtASpeed)

    @property
    def concept_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5427.ConceptGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5427,
        )

        return self.__parent__._cast(_5427.ConceptGearSetModalAnalysisAtASpeed)

    @property
    def conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5430.ConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5430,
        )

        return self.__parent__._cast(_5430.ConicalGearSetModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5445.CylindricalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5445,
        )

        return self.__parent__._cast(_5445.CylindricalGearSetModalAnalysisAtASpeed)

    @property
    def face_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5451.FaceGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5451,
        )

        return self.__parent__._cast(_5451.FaceGearSetModalAnalysisAtASpeed)

    @property
    def hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5460.HypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5460,
        )

        return self.__parent__._cast(_5460.HypoidGearSetModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5464.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5464,
        )

        return self.__parent__._cast(
            _5464.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5467.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5467,
        )

        return self.__parent__._cast(
            _5467.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5470.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5470,
        )

        return self.__parent__._cast(
            _5470.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed
        )

    @property
    def planetary_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5483.PlanetaryGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5483,
        )

        return self.__parent__._cast(_5483.PlanetaryGearSetModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5500.SpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5500,
        )

        return self.__parent__._cast(_5500.SpiralBevelGearSetModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5506.StraightBevelDiffGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5506,
        )

        return self.__parent__._cast(
            _5506.StraightBevelDiffGearSetModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5509.StraightBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5509,
        )

        return self.__parent__._cast(_5509.StraightBevelGearSetModalAnalysisAtASpeed)

    @property
    def worm_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5524.WormGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5524,
        )

        return self.__parent__._cast(_5524.WormGearSetModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5527.ZerolBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5527,
        )

        return self.__parent__._cast(_5527.ZerolBevelGearSetModalAnalysisAtASpeed)

    @property
    def gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "GearSetModalAnalysisAtASpeed":
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
class GearSetModalAnalysisAtASpeed(_5497.SpecialisedAssemblyModalAnalysisAtASpeed):
    """GearSetModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def gears_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5455.GearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.GearModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsModalAnalysisAtASpeed")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5454.GearMeshModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.GearMeshModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesModalAnalysisAtASpeed")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_GearSetModalAnalysisAtASpeed
        """
        return _Cast_GearSetModalAnalysisAtASpeed(self)
