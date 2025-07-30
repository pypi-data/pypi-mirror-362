"""AbstractShaftToMountableComponentConnectionPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4328

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "AbstractShaftToMountableComponentConnectionPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4317,
        _4337,
        _4338,
        _4381,
        _4397,
    )
    from mastapy._private.system_model.connections_and_sockets import _2486

    Self = TypeVar("Self", bound="AbstractShaftToMountableComponentConnectionPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionPowerFlow._Cast_AbstractShaftToMountableComponentConnectionPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionPowerFlow:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionPowerFlow to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionPowerFlow"

    @property
    def connection_power_flow(self: "CastSelf") -> "_4328.ConnectionPowerFlow":
        return self.__parent__._cast(_4328.ConnectionPowerFlow)

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
    def coaxial_connection_power_flow(
        self: "CastSelf",
    ) -> "_4317.CoaxialConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4317

        return self.__parent__._cast(_4317.CoaxialConnectionPowerFlow)

    @property
    def cycloidal_disc_central_bearing_connection_power_flow(
        self: "CastSelf",
    ) -> "_4337.CycloidalDiscCentralBearingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4337

        return self.__parent__._cast(
            _4337.CycloidalDiscCentralBearingConnectionPowerFlow
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_power_flow(
        self: "CastSelf",
    ) -> "_4338.CycloidalDiscPlanetaryBearingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4338

        return self.__parent__._cast(
            _4338.CycloidalDiscPlanetaryBearingConnectionPowerFlow
        )

    @property
    def planetary_connection_power_flow(
        self: "CastSelf",
    ) -> "_4381.PlanetaryConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4381

        return self.__parent__._cast(_4381.PlanetaryConnectionPowerFlow)

    @property
    def shaft_to_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4397.ShaftToMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4397

        return self.__parent__._cast(_4397.ShaftToMountableComponentConnectionPowerFlow)

    @property
    def abstract_shaft_to_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionPowerFlow":
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
class AbstractShaftToMountableComponentConnectionPowerFlow(_4328.ConnectionPowerFlow):
    """AbstractShaftToMountableComponentConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_POWER_FLOW
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
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionPowerFlow
        """
        return _Cast_AbstractShaftToMountableComponentConnectionPowerFlow(self)
