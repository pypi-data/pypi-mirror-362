"""ShaftToMountableComponentConnectionCompoundHarmonicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6188,
)

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ShaftToMountableComponentConnectionCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6104,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6209,
        _6220,
        _6229,
        _6270,
    )

    Self = TypeVar(
        "Self", bound="ShaftToMountableComponentConnectionCompoundHarmonicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftToMountableComponentConnectionCompoundHarmonicAnalysis._Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnectionCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis:
    """Special nested class for casting ShaftToMountableComponentConnectionCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ShaftToMountableComponentConnectionCompoundHarmonicAnalysis"

    @property
    def abstract_shaft_to_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6188.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
        return self.__parent__._cast(
            _6188.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6220.ConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6220,
        )

        return self.__parent__._cast(_6220.ConnectionCompoundHarmonicAnalysis)

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
    def coaxial_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6209.CoaxialConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6209,
        )

        return self.__parent__._cast(_6209.CoaxialConnectionCompoundHarmonicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6229.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6229,
        )

        return self.__parent__._cast(
            _6229.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis
        )

    @property
    def planetary_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6270.PlanetaryConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6270,
        )

        return self.__parent__._cast(_6270.PlanetaryConnectionCompoundHarmonicAnalysis)

    @property
    def shaft_to_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
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
class ShaftToMountableComponentConnectionCompoundHarmonicAnalysis(
    _6188.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis
):
    """ShaftToMountableComponentConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6104.ShaftToMountableComponentConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ShaftToMountableComponentConnectionHarmonicAnalysis]

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
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6104.ShaftToMountableComponentConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ShaftToMountableComponentConnectionHarmonicAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis
        """
        return _Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis(self)
