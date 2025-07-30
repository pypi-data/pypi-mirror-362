"""CycloidalDiscPlanetaryBearingConnectionLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7678

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalDiscPlanetaryBearingConnectionLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.static_loads import _7718
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2559

    Self = TypeVar("Self", bound="CycloidalDiscPlanetaryBearingConnectionLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscPlanetaryBearingConnectionLoadCase._Cast_CycloidalDiscPlanetaryBearingConnectionLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscPlanetaryBearingConnectionLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscPlanetaryBearingConnectionLoadCase:
    """Special nested class for casting CycloidalDiscPlanetaryBearingConnectionLoadCase to subclasses."""

    __parent__: "CycloidalDiscPlanetaryBearingConnectionLoadCase"

    @property
    def abstract_shaft_to_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7678.AbstractShaftToMountableComponentConnectionLoadCase":
        return self.__parent__._cast(
            _7678.AbstractShaftToMountableComponentConnectionLoadCase
        )

    @property
    def connection_load_case(self: "CastSelf") -> "_7718.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7718,
        )

        return self.__parent__._cast(_7718.ConnectionLoadCase)

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
    def cycloidal_disc_planetary_bearing_connection_load_case(
        self: "CastSelf",
    ) -> "CycloidalDiscPlanetaryBearingConnectionLoadCase":
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
class CycloidalDiscPlanetaryBearingConnectionLoadCase(
    _7678.AbstractShaftToMountableComponentConnectionLoadCase
):
    """CycloidalDiscPlanetaryBearingConnectionLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE

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
    ) -> "_2559.CycloidalDiscPlanetaryBearingConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection

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
    ) -> "_Cast_CycloidalDiscPlanetaryBearingConnectionLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscPlanetaryBearingConnectionLoadCase
        """
        return _Cast_CycloidalDiscPlanetaryBearingConnectionLoadCase(self)
