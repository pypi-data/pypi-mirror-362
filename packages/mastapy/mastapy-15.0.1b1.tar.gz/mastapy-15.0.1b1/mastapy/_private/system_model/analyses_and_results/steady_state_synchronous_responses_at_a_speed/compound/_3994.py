"""SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
    _3927,
)

_SPRING_DAMPER_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound",
    "SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3861,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
        _3924,
        _3954,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2571

    Self = TypeVar(
        "Self",
        bound="SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed"

    @property
    def coupling_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3927.CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3927.CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
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
    def spring_damper_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
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
class SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed(
    _3927.CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
):
    """SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SPRING_DAMPER_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2571.SpringDamperConnection":
        """mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2571.SpringDamperConnection":
        """mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection

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
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3861.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed]

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
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3861.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        """
        return (
            _Cast_SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed(
                self
            )
        )
