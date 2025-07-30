"""AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
    _6484,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6319,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
        _6473,
        _6493,
        _6495,
        _6534,
        _6548,
    )

    Self = TypeVar(
        "Self",
        bound="AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation._Cast_AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation"

    @property
    def connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6484.ConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(
            _6484.ConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

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
    def coaxial_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6473.CoaxialConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6473,
        )

        return self.__parent__._cast(
            _6473.CoaxialConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6493.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6493,
        )

        return self.__parent__._cast(
            _6493.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6495.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6495,
        )

        return self.__parent__._cast(
            _6495.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planetary_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6534.PlanetaryConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6534,
        )

        return self.__parent__._cast(
            _6534.PlanetaryConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_to_mountable_component_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6548.ShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6548,
        )

        return self.__parent__._cast(
            _6548.ShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
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
class AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation(
    _6484.ConnectionCompoundHarmonicAnalysisOfSingleExcitation
):
    """AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
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
    ) -> "List[_6319.AbstractShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.AbstractShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation]

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
    ) -> "List[_6319.AbstractShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.AbstractShaftToMountableComponentConnectionHarmonicAnalysisOfSingleExcitation]

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
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation(
            self
        )
