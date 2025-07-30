"""AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5431,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_SPEED = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
        "AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5420,
        _5440,
        _5442,
        _5482,
        _5496,
    )
    from mastapy._private.system_model.connections_and_sockets import _2486

    Self = TypeVar(
        "Self", bound="AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed._Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed"

    @property
    def connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5431.ConnectionModalAnalysisAtASpeed":
        return self.__parent__._cast(_5431.ConnectionModalAnalysisAtASpeed)

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
    def coaxial_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5420.CoaxialConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5420,
        )

        return self.__parent__._cast(_5420.CoaxialConnectionModalAnalysisAtASpeed)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5440.CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5440,
        )

        return self.__parent__._cast(
            _5440.CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5442.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5442,
        )

        return self.__parent__._cast(
            _5442.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed
        )

    @property
    def planetary_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5482.PlanetaryConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5482,
        )

        return self.__parent__._cast(_5482.PlanetaryConnectionModalAnalysisAtASpeed)

    @property
    def shaft_to_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5496.ShaftToMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5496,
        )

        return self.__parent__._cast(
            _5496.ShaftToMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed":
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
class AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed(
    _5431.ConnectionModalAnalysisAtASpeed
):
    """AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_SPEED
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
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed
        """
        return _Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed(
            self
        )
