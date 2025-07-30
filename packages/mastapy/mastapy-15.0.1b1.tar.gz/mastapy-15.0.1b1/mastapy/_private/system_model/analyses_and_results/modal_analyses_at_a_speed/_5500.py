"""SpiralBevelGearSetModalAnalysisAtASpeed"""

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
    _5414,
)

_SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "SpiralBevelGearSetModalAnalysisAtASpeed",
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
        _5430,
        _5456,
        _5478,
        _5497,
        _5498,
        _5499,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7826
    from mastapy._private.system_model.part_model.gears import _2782

    Self = TypeVar("Self", bound="SpiralBevelGearSetModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpiralBevelGearSetModalAnalysisAtASpeed._Cast_SpiralBevelGearSetModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearSetModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearSetModalAnalysisAtASpeed:
    """Special nested class for casting SpiralBevelGearSetModalAnalysisAtASpeed to subclasses."""

    __parent__: "SpiralBevelGearSetModalAnalysisAtASpeed"

    @property
    def bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5414.BevelGearSetModalAnalysisAtASpeed":
        return self.__parent__._cast(_5414.BevelGearSetModalAnalysisAtASpeed)

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
    def conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5430.ConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5430,
        )

        return self.__parent__._cast(_5430.ConicalGearSetModalAnalysisAtASpeed)

    @property
    def gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5456.GearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5456,
        )

        return self.__parent__._cast(_5456.GearSetModalAnalysisAtASpeed)

    @property
    def specialised_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5497.SpecialisedAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5497,
        )

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
    def spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "SpiralBevelGearSetModalAnalysisAtASpeed":
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
class SpiralBevelGearSetModalAnalysisAtASpeed(_5414.BevelGearSetModalAnalysisAtASpeed):
    """SpiralBevelGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2782.SpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.SpiralBevelGearSet

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
    def assembly_load_case(self: "Self") -> "_7826.SpiralBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase

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
    def bevel_gears_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5499.SpiralBevelGearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.SpiralBevelGearModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearsModalAnalysisAtASpeed")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spiral_bevel_gears_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5499.SpiralBevelGearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.SpiralBevelGearModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpiralBevelGearsModalAnalysisAtASpeed"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bevel_meshes_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5498.SpiralBevelGearMeshModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.SpiralBevelGearMeshModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelMeshesModalAnalysisAtASpeed")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spiral_bevel_meshes_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5498.SpiralBevelGearMeshModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.SpiralBevelGearMeshModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpiralBevelMeshesModalAnalysisAtASpeed"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearSetModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearSetModalAnalysisAtASpeed
        """
        return _Cast_SpiralBevelGearSetModalAnalysisAtASpeed(self)
