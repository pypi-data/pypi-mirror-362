"""ClutchConnectionSteadyStateSynchronousResponse"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3265,
)

_CLUTCH_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "ClutchConnectionSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7701
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3263,
        _3294,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2563

    Self = TypeVar("Self", bound="ClutchConnectionSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ClutchConnectionSteadyStateSynchronousResponse._Cast_ClutchConnectionSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ClutchConnectionSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClutchConnectionSteadyStateSynchronousResponse:
    """Special nested class for casting ClutchConnectionSteadyStateSynchronousResponse to subclasses."""

    __parent__: "ClutchConnectionSteadyStateSynchronousResponse"

    @property
    def coupling_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3265.CouplingConnectionSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3265.CouplingConnectionSteadyStateSynchronousResponse
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3294.InterMountableComponentConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3294,
        )

        return self.__parent__._cast(
            _3294.InterMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3263.ConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3263,
        )

        return self.__parent__._cast(_3263.ConnectionSteadyStateSynchronousResponse)

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
    def clutch_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "ClutchConnectionSteadyStateSynchronousResponse":
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
class ClutchConnectionSteadyStateSynchronousResponse(
    _3265.CouplingConnectionSteadyStateSynchronousResponse
):
    """ClutchConnectionSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2563.ClutchConnection":
        """mastapy.system_model.connections_and_sockets.couplings.ClutchConnection

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
    def connection_load_case(self: "Self") -> "_7701.ClutchConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ClutchConnectionSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_ClutchConnectionSteadyStateSynchronousResponse
        """
        return _Cast_ClutchConnectionSteadyStateSynchronousResponse(self)
