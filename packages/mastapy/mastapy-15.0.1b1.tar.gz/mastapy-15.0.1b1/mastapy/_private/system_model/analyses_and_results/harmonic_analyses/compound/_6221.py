"""ConnectorCompoundHarmonicAnalysis"""

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
    _6264,
)

_CONNECTOR_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ConnectorCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6006,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6193,
        _6210,
        _6265,
        _6266,
        _6283,
    )

    Self = TypeVar("Self", bound="ConnectorCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectorCompoundHarmonicAnalysis._Cast_ConnectorCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorCompoundHarmonicAnalysis:
    """Special nested class for casting ConnectorCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ConnectorCompoundHarmonicAnalysis"

    @property
    def mountable_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6264.MountableComponentCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6264.MountableComponentCompoundHarmonicAnalysis)

    @property
    def component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6210.ComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6210,
        )

        return self.__parent__._cast(_6210.ComponentCompoundHarmonicAnalysis)

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6266.PartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6266,
        )

        return self.__parent__._cast(_6266.PartCompoundHarmonicAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

        return self.__parent__._cast(_7888.PartCompoundAnalysis)

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
    def bearing_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6193.BearingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6193,
        )

        return self.__parent__._cast(_6193.BearingCompoundHarmonicAnalysis)

    @property
    def oil_seal_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6265.OilSealCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6265,
        )

        return self.__parent__._cast(_6265.OilSealCompoundHarmonicAnalysis)

    @property
    def shaft_hub_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6283.ShaftHubConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6283,
        )

        return self.__parent__._cast(_6283.ShaftHubConnectionCompoundHarmonicAnalysis)

    @property
    def connector_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ConnectorCompoundHarmonicAnalysis":
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
class ConnectorCompoundHarmonicAnalysis(
    _6264.MountableComponentCompoundHarmonicAnalysis
):
    """ConnectorCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6006.ConnectorHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConnectorHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6006.ConnectorHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConnectorHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectorCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectorCompoundHarmonicAnalysis
        """
        return _Cast_ConnectorCompoundHarmonicAnalysis(self)
