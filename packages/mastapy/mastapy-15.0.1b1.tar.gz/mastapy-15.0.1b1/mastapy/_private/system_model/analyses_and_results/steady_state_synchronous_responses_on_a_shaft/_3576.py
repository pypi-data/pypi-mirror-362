"""PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft"""

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
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
    _3531,
)

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7800
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3529,
        _3559,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2569

    Self = TypeVar(
        "Self",
        bound="PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft._Cast_PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: (
        "PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft"
    )

    @property
    def coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3531.CouplingConnectionSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3531.CouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3559.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3559,
        )

        return self.__parent__._cast(
            _3559.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3529.ConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3529,
        )

        return self.__parent__._cast(
            _3529.ConnectionSteadyStateSynchronousResponseOnAShaft
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
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft":
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
class PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft(
    _3531.CouplingConnectionSteadyStateSynchronousResponseOnAShaft
):
    """PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _PART_TO_PART_SHEAR_COUPLING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2569.PartToPartShearCouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection

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
    def connection_load_case(
        self: "Self",
    ) -> "_7800.PartToPartShearCouplingConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase

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
    ) -> (
        "_Cast_PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        """Cast to another type.

        Returns:
            _Cast_PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft(
            self
        )
