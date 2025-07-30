"""CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4180,
)

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_STABILITY_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
        "CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis",
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
        _4065,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4159,
        _4191,
        _4255,
    )

    Self = TypeVar(
        "Self", bound="CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis._Cast_CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis to subclasses."""

    __parent__: "CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis"

    @property
    def coaxial_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4180.CoaxialConnectionCompoundStabilityAnalysis":
        return self.__parent__._cast(_4180.CoaxialConnectionCompoundStabilityAnalysis)

    @property
    def shaft_to_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4255.ShaftToMountableComponentConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4255,
        )

        return self.__parent__._cast(
            _4255.ShaftToMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4159.AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4159,
        )

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
    def cycloidal_disc_central_bearing_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis":
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
class CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis(
    _4180.CoaxialConnectionCompoundStabilityAnalysis
):
    """CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_STABILITY_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4065.CycloidalDiscCentralBearingConnectionStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CycloidalDiscCentralBearingConnectionStabilityAnalysis]

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
    ) -> "List[_4065.CycloidalDiscCentralBearingConnectionStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CycloidalDiscCentralBearingConnectionStabilityAnalysis]

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
    ) -> "_Cast_CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis
        """
        return _Cast_CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis(
            self
        )
