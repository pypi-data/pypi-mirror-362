"""AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed"""

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
    _3792,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3781,
        _3801,
        _3802,
        _3842,
        _3856,
    )
    from mastapy._private.system_model.connections_and_sockets import _2486

    Self = TypeVar(
        "Self",
        bound="AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed._Cast_AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed"

    @property
    def connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3792.ConnectionSteadyStateSynchronousResponseAtASpeed":
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
    def coaxial_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3781.CoaxialConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3781,
        )

        return self.__parent__._cast(
            _3781.CoaxialConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3801.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3801,
        )

        return self.__parent__._cast(
            _3801.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3802.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3802,
        )

        return self.__parent__._cast(
            _3802.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def planetary_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3842.PlanetaryConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3842,
        )

        return self.__parent__._cast(
            _3842.PlanetaryConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3856.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3856,
        )

        return self.__parent__._cast(
            _3856.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed":
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
class AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed(
    _3792.ConnectionSteadyStateSynchronousResponseAtASpeed
):
    """AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(
        self: "Self",
    ) -> "_2486.AbstractShaftToMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed(
            self
        )
