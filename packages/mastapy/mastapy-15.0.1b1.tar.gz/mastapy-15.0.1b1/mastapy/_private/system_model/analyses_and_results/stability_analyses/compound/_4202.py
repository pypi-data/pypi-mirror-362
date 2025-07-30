"""CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4159,
)

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_STABILITY_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
        "CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4066,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4191,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2559

    Self = TypeVar(
        "Self", bound="CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis._Cast_CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis:
    """Special nested class for casting CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis to subclasses."""

    __parent__: "CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis"

    @property
    def abstract_shaft_to_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4159.AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis":
        return self.__parent__._cast(
            _4159.AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4191.ConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4191,
        )

        return self.__parent__._cast(_4191.ConnectionCompoundStabilityAnalysis)

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
    def cycloidal_disc_planetary_bearing_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis":
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
class CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis(
    _4159.AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis
):
    """CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_STABILITY_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(
        self: "Self",
    ) -> "_2559.CycloidalDiscPlanetaryBearingConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection

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
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4066.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis]

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
    ) -> "List[_4066.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis]

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
    ) -> "_Cast_CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis
        """
        return _Cast_CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis(
            self
        )
