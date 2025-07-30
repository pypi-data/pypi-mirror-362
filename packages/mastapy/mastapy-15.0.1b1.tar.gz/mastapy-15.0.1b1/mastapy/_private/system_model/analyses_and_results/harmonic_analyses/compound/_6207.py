"""ClutchConnectionCompoundHarmonicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6223,
)

_CLUTCH_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ClutchConnectionCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5990,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6220,
        _6250,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2563

    Self = TypeVar("Self", bound="ClutchConnectionCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ClutchConnectionCompoundHarmonicAnalysis._Cast_ClutchConnectionCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ClutchConnectionCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClutchConnectionCompoundHarmonicAnalysis:
    """Special nested class for casting ClutchConnectionCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ClutchConnectionCompoundHarmonicAnalysis"

    @property
    def coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6223.CouplingConnectionCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6223.CouplingConnectionCompoundHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6250.InterMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6250,
        )

        return self.__parent__._cast(
            _6250.InterMountableComponentConnectionCompoundHarmonicAnalysis
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
    def clutch_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ClutchConnectionCompoundHarmonicAnalysis":
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
class ClutchConnectionCompoundHarmonicAnalysis(
    _6223.CouplingConnectionCompoundHarmonicAnalysis
):
    """ClutchConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH_CONNECTION_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2563.ClutchConnection":
        """mastapy.system_model.connections_and_sockets.couplings.ClutchConnection

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
    def connection_design(self: "Self") -> "_2563.ClutchConnection":
        """mastapy.system_model.connections_and_sockets.couplings.ClutchConnection

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
    ) -> "List[_5990.ClutchConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ClutchConnectionHarmonicAnalysis]

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
    ) -> "List[_5990.ClutchConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ClutchConnectionHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ClutchConnectionCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ClutchConnectionCompoundHarmonicAnalysis
        """
        return _Cast_ClutchConnectionCompoundHarmonicAnalysis(self)
