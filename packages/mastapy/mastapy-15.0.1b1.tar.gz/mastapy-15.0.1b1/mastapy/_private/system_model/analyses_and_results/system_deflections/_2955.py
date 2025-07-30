"""CoaxialConnectionSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.system_deflections import _3048

_COAXIAL_CONNECTION_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CoaxialConnectionSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7882,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4317
    from mastapy._private.system_model.analyses_and_results.static_loads import _7705
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2929,
        _2968,
        _2977,
    )
    from mastapy._private.system_model.connections_and_sockets import _2490

    Self = TypeVar("Self", bound="CoaxialConnectionSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoaxialConnectionSystemDeflection._Cast_CoaxialConnectionSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoaxialConnectionSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoaxialConnectionSystemDeflection:
    """Special nested class for casting CoaxialConnectionSystemDeflection to subclasses."""

    __parent__: "CoaxialConnectionSystemDeflection"

    @property
    def shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3048.ShaftToMountableComponentConnectionSystemDeflection":
        return self.__parent__._cast(
            _3048.ShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def abstract_shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2929.AbstractShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2929,
        )

        return self.__parent__._cast(
            _2929.AbstractShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2968.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2968,
        )

        return self.__parent__._cast(_2968.ConnectionSystemDeflection)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7882.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7882,
        )

        return self.__parent__._cast(_7882.ConnectionFEAnalysis)

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
    def cycloidal_disc_central_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2977.CycloidalDiscCentralBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2977,
        )

        return self.__parent__._cast(
            _2977.CycloidalDiscCentralBearingConnectionSystemDeflection
        )

    @property
    def coaxial_connection_system_deflection(
        self: "CastSelf",
    ) -> "CoaxialConnectionSystemDeflection":
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
class CoaxialConnectionSystemDeflection(
    _3048.ShaftToMountableComponentConnectionSystemDeflection
):
    """CoaxialConnectionSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COAXIAL_CONNECTION_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def connection_load_case(self: "Self") -> "_7705.CoaxialConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase

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
    def power_flow_results(self: "Self") -> "_4317.CoaxialConnectionPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.CoaxialConnectionPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CoaxialConnectionSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CoaxialConnectionSystemDeflection
        """
        return _Cast_CoaxialConnectionSystemDeflection(self)
