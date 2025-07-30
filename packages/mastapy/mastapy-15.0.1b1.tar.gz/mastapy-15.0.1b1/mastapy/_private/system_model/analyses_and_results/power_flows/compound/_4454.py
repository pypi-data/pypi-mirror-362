"""CoaxialConnectionCompoundPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4529,
)

_COAXIAL_CONNECTION_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "CoaxialConnectionCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4317
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4433,
        _4465,
        _4474,
    )
    from mastapy._private.system_model.connections_and_sockets import _2490

    Self = TypeVar("Self", bound="CoaxialConnectionCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoaxialConnectionCompoundPowerFlow._Cast_CoaxialConnectionCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoaxialConnectionCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoaxialConnectionCompoundPowerFlow:
    """Special nested class for casting CoaxialConnectionCompoundPowerFlow to subclasses."""

    __parent__: "CoaxialConnectionCompoundPowerFlow"

    @property
    def shaft_to_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4529.ShaftToMountableComponentConnectionCompoundPowerFlow":
        return self.__parent__._cast(
            _4529.ShaftToMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4433.AbstractShaftToMountableComponentConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4433,
        )

        return self.__parent__._cast(
            _4433.AbstractShaftToMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4465.ConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4465,
        )

        return self.__parent__._cast(_4465.ConnectionCompoundPowerFlow)

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
    def cycloidal_disc_central_bearing_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4474.CycloidalDiscCentralBearingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4474,
        )

        return self.__parent__._cast(
            _4474.CycloidalDiscCentralBearingConnectionCompoundPowerFlow
        )

    @property
    def coaxial_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "CoaxialConnectionCompoundPowerFlow":
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
class CoaxialConnectionCompoundPowerFlow(
    _4529.ShaftToMountableComponentConnectionCompoundPowerFlow
):
    """CoaxialConnectionCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COAXIAL_CONNECTION_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2490.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

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
    def connection_design(self: "Self") -> "_2490.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

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
    ) -> "List[_4317.CoaxialConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CoaxialConnectionPowerFlow]

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
    ) -> "List[_4317.CoaxialConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CoaxialConnectionPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_CoaxialConnectionCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_CoaxialConnectionCompoundPowerFlow
        """
        return _Cast_CoaxialConnectionCompoundPowerFlow(self)
