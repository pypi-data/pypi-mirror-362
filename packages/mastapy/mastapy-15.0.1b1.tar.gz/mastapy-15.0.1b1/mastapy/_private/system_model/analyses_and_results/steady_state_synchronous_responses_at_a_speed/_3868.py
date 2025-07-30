"""StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3773,
)

_STRAIGHT_BEVEL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7834
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3761,
        _3789,
        _3792,
        _3815,
        _3822,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2548

    Self = TypeVar(
        "Self", bound="StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed._Cast_StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed"

    @property
    def bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3773.BevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3773.BevelGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3761.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3761,
        )

        return self.__parent__._cast(
            _3761.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3789.ConicalGearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3789,
        )

        return self.__parent__._cast(
            _3789.ConicalGearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3815.GearMeshSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3815,
        )

        return self.__parent__._cast(
            _3815.GearMeshSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3822.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3822,
        )

        return self.__parent__._cast(
            _3822.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3792.ConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3792,
        )

        return self.__parent__._cast(
            _3792.ConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

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
    def straight_bevel_gear_mesh_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
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
class StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed(
    _3773.BevelGearMeshSteadyStateSynchronousResponseAtASpeed
):
    """StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _STRAIGHT_BEVEL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2548.StraightBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_load_case(self: "Self") -> "_7834.StraightBevelGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed(self)
