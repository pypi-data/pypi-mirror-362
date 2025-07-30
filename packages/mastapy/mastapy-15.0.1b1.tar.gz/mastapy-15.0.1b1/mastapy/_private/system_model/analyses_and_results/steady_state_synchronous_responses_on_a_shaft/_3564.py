"""KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
    _3561,
)

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7786
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3494,
        _3527,
        _3553,
        _3563,
        _3565,
        _3575,
        _3594,
    )
    from mastapy._private.system_model.part_model.gears import _2776

    Self = TypeVar(
        "Self",
        bound="KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft._Cast_KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: (
        "KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft"
    )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3561.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3561.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3527.ConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3527,
        )

        return self.__parent__._cast(
            _3527.ConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3553.GearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3553,
        )

        return self.__parent__._cast(
            _3553.GearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def specialised_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3594.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3594,
        )

        return self.__parent__._cast(
            _3594.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3494.AbstractAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3494,
        )

        return self.__parent__._cast(
            _3494.AbstractAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3575.PartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3575,
        )

        return self.__parent__._cast(_3575.PartSteadyStateSynchronousResponseOnAShaft)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft":
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
class KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft(
    _3561.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseOnAShaft
):
    """KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
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
    def klingelnberg_cyclo_palloid_conical_gears_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3565.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidConicalGearsSteadyStateSynchronousResponseOnAShaft",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_gears_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3565.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidHypoidGearsSteadyStateSynchronousResponseOnAShaft",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_conical_meshes_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3563.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidConicalMeshesSteadyStateSynchronousResponseOnAShaft",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_meshes_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3563.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidHypoidMeshesSteadyStateSynchronousResponseOnAShaft",
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
    ) -> "_Cast_KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft(
            self
        )
