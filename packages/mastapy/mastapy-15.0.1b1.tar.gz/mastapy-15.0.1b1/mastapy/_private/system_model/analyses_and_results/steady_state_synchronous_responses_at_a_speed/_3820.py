"""HypoidGearSetSteadyStateSynchronousResponseAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3762,
)

_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "HypoidGearSetSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7776
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3757,
        _3790,
        _3816,
        _3819,
        _3821,
        _3838,
        _3857,
    )
    from mastapy._private.system_model.part_model.gears import _2772

    Self = TypeVar("Self", bound="HypoidGearSetSteadyStateSynchronousResponseAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HypoidGearSetSteadyStateSynchronousResponseAtASpeed._Cast_HypoidGearSetSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearSetSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearSetSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting HypoidGearSetSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "HypoidGearSetSteadyStateSynchronousResponseAtASpeed"

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3762.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3762.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3790.ConicalGearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3790,
        )

        return self.__parent__._cast(
            _3790.ConicalGearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3816.GearSetSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3816,
        )

        return self.__parent__._cast(
            _3816.GearSetSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def specialised_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3857.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3857,
        )

        return self.__parent__._cast(
            _3857.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_assembly_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3757.AbstractAssemblySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3757,
        )

        return self.__parent__._cast(
            _3757.AbstractAssemblySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3838.PartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3838,
        )

        return self.__parent__._cast(_3838.PartSteadyStateSynchronousResponseAtASpeed)

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
    def hypoid_gear_set_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "HypoidGearSetSteadyStateSynchronousResponseAtASpeed":
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
class HypoidGearSetSteadyStateSynchronousResponseAtASpeed(
    _3762.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed
):
    """HypoidGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2772.HypoidGearSet":
        """mastapy.system_model.part_model.gears.HypoidGearSet

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
    def assembly_load_case(self: "Self") -> "_7776.HypoidGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase

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
    def agma_gleason_conical_gears_steady_state_synchronous_response_at_a_speed(
        self: "Self",
    ) -> "List[_3821.HypoidGearSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.HypoidGearSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AGMAGleasonConicalGearsSteadyStateSynchronousResponseAtASpeed",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def hypoid_gears_steady_state_synchronous_response_at_a_speed(
        self: "Self",
    ) -> "List[_3821.HypoidGearSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.HypoidGearSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HypoidGearsSteadyStateSynchronousResponseAtASpeed"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def agma_gleason_conical_meshes_steady_state_synchronous_response_at_a_speed(
        self: "Self",
    ) -> "List[_3819.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AGMAGleasonConicalMeshesSteadyStateSynchronousResponseAtASpeed",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def hypoid_meshes_steady_state_synchronous_response_at_a_speed(
        self: "Self",
    ) -> "List[_3819.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.HypoidGearMeshSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HypoidMeshesSteadyStateSynchronousResponseAtASpeed"
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
    ) -> "_Cast_HypoidGearSetSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearSetSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_HypoidGearSetSteadyStateSynchronousResponseAtASpeed(self)
