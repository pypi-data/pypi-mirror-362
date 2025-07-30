"""AbstractShaftToMountableComponentConnectionSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.system_deflections import _2968

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "AbstractShaftToMountableComponentConnectionSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7882,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4296
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2955,
        _2977,
        _2978,
        _3032,
        _3048,
    )
    from mastapy._private.system_model.connections_and_sockets import _2486

    Self = TypeVar(
        "Self", bound="AbstractShaftToMountableComponentConnectionSystemDeflection"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionSystemDeflection._Cast_AbstractShaftToMountableComponentConnectionSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionSystemDeflection:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionSystemDeflection to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionSystemDeflection"

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2968.ConnectionSystemDeflection":
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
    def coaxial_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2955.CoaxialConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2955,
        )

        return self.__parent__._cast(_2955.CoaxialConnectionSystemDeflection)

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
    def cycloidal_disc_planetary_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2978.CycloidalDiscPlanetaryBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2978,
        )

        return self.__parent__._cast(
            _2978.CycloidalDiscPlanetaryBearingConnectionSystemDeflection
        )

    @property
    def planetary_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3032.PlanetaryConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3032,
        )

        return self.__parent__._cast(_3032.PlanetaryConnectionSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3048.ShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3048,
        )

        return self.__parent__._cast(
            _3048.ShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def abstract_shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionSystemDeflection":
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
class AbstractShaftToMountableComponentConnectionSystemDeflection(
    _2968.ConnectionSystemDeflection
):
    """AbstractShaftToMountableComponentConnectionSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_SYSTEM_DEFLECTION
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
    @exception_bridge
    def power_flow_results(
        self: "Self",
    ) -> "_4296.AbstractShaftToMountableComponentConnectionPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.AbstractShaftToMountableComponentConnectionPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionSystemDeflection
        """
        return _Cast_AbstractShaftToMountableComponentConnectionSystemDeflection(self)
