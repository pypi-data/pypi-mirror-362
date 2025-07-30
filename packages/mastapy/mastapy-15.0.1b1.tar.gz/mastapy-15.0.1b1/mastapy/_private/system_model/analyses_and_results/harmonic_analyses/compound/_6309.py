"""VirtualComponentCompoundHarmonicAnalysis"""

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

_VIRTUAL_COMPONENT_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "VirtualComponentCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6133,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6210,
        _6260,
        _6261,
        _6266,
        _6273,
        _6274,
        _6308,
    )

    Self = TypeVar("Self", bound="VirtualComponentCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentCompoundHarmonicAnalysis._Cast_VirtualComponentCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentCompoundHarmonicAnalysis:
    """Special nested class for casting VirtualComponentCompoundHarmonicAnalysis to subclasses."""

    __parent__: "VirtualComponentCompoundHarmonicAnalysis"

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
    def mass_disc_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6260.MassDiscCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6260,
        )

        return self.__parent__._cast(_6260.MassDiscCompoundHarmonicAnalysis)

    @property
    def measurement_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6261.MeasurementComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6261,
        )

        return self.__parent__._cast(_6261.MeasurementComponentCompoundHarmonicAnalysis)

    @property
    def point_load_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6273.PointLoadCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6273,
        )

        return self.__parent__._cast(_6273.PointLoadCompoundHarmonicAnalysis)

    @property
    def power_load_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6274.PowerLoadCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6274,
        )

        return self.__parent__._cast(_6274.PowerLoadCompoundHarmonicAnalysis)

    @property
    def unbalanced_mass_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6308.UnbalancedMassCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6308,
        )

        return self.__parent__._cast(_6308.UnbalancedMassCompoundHarmonicAnalysis)

    @property
    def virtual_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "VirtualComponentCompoundHarmonicAnalysis":
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
class VirtualComponentCompoundHarmonicAnalysis(
    _6264.MountableComponentCompoundHarmonicAnalysis
):
    """VirtualComponentCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_COMPOUND_HARMONIC_ANALYSIS

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
    ) -> "List[_6133.VirtualComponentHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.VirtualComponentHarmonicAnalysis]

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
    ) -> "List[_6133.VirtualComponentHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.VirtualComponentHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_VirtualComponentCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentCompoundHarmonicAnalysis
        """
        return _Cast_VirtualComponentCompoundHarmonicAnalysis(self)
