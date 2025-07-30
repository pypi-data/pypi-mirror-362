"""AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
    _3922,
)

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound",
    "AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3761,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
        _3901,
        _3906,
        _3924,
        _3948,
        _3952,
        _3954,
        _3991,
        _3997,
        _4000,
        _4018,
    )

    Self = TypeVar(
        "Self",
        bound="AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: (
        "AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    )

    @property
    def conical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3922.ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3922.ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3948.GearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3948,
        )

        return self.__parent__._cast(
            _3948.GearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def inter_mountable_component_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3954.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3954,
        )

        return self.__parent__._cast(
            _3954.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3924.ConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3924,
        )

        return self.__parent__._cast(
            _3924.ConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7881.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7881,
        )

        return self.__parent__._cast(_7881.ConnectionCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7885.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7885,
        )

        return self.__parent__._cast(_7885.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3901.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3901,
        )

        return self.__parent__._cast(
            _3901.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3906.BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3906,
        )

        return self.__parent__._cast(
            _3906.BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3952.HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3952,
        )

        return self.__parent__._cast(
            _3952.HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3991.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3991,
        )

        return self.__parent__._cast(
            _3991.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3997.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3997,
        )

        return self.__parent__._cast(
            _3997.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_4000.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _4000,
        )

        return self.__parent__._cast(
            _4000.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_4018.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _4018,
        )

        return self.__parent__._cast(
            _4018.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
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
class AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed(
    _3922.ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
):
    """AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3761.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3761.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> (
        "_Cast_AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed(
            self
        )
