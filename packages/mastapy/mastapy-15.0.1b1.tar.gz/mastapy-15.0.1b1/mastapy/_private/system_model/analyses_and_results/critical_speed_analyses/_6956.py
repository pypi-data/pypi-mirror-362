"""RollingRingConnectionCriticalSpeedAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6927,
)

_ROLLING_RING_CONNECTION_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "RollingRingConnectionCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6894,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7817
    from mastapy._private.system_model.connections_and_sockets import _2513

    Self = TypeVar("Self", bound="RollingRingConnectionCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollingRingConnectionCriticalSpeedAnalysis._Cast_RollingRingConnectionCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingRingConnectionCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingRingConnectionCriticalSpeedAnalysis:
    """Special nested class for casting RollingRingConnectionCriticalSpeedAnalysis to subclasses."""

    __parent__: "RollingRingConnectionCriticalSpeedAnalysis"

    @property
    def inter_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6927.InterMountableComponentConnectionCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _6927.InterMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6894.ConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6894,
        )

        return self.__parent__._cast(_6894.ConnectionCriticalSpeedAnalysis)

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
    def rolling_ring_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "RollingRingConnectionCriticalSpeedAnalysis":
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
class RollingRingConnectionCriticalSpeedAnalysis(
    _6927.InterMountableComponentConnectionCriticalSpeedAnalysis
):
    """RollingRingConnectionCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_RING_CONNECTION_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2513.RollingRingConnection":
        """mastapy.system_model.connections_and_sockets.RollingRingConnection

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
    def connection_load_case(self: "Self") -> "_7817.RollingRingConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[RollingRingConnectionCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.RollingRingConnectionCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RollingRingConnectionCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_RollingRingConnectionCriticalSpeedAnalysis
        """
        return _Cast_RollingRingConnectionCriticalSpeedAnalysis(self)
