"""AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis"""

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
    _6218,
)

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5974,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6197,
        _6202,
        _6220,
        _6244,
        _6248,
        _6250,
        _6287,
        _6293,
        _6296,
        _6314,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis._Cast_AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis"

    @property
    def conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6218.ConicalGearMeshCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6218.ConicalGearMeshCompoundHarmonicAnalysis)

    @property
    def gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6244.GearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6244,
        )

        return self.__parent__._cast(_6244.GearMeshCompoundHarmonicAnalysis)

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
    def bevel_differential_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6197.BevelDifferentialGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6197,
        )

        return self.__parent__._cast(
            _6197.BevelDifferentialGearMeshCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6202.BevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6202,
        )

        return self.__parent__._cast(_6202.BevelGearMeshCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6248.HypoidGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6248,
        )

        return self.__parent__._cast(_6248.HypoidGearMeshCompoundHarmonicAnalysis)

    @property
    def spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6287.SpiralBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6287,
        )

        return self.__parent__._cast(_6287.SpiralBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6293.StraightBevelDiffGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6293,
        )

        return self.__parent__._cast(
            _6293.StraightBevelDiffGearMeshCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6296.StraightBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6296,
        )

        return self.__parent__._cast(
            _6296.StraightBevelGearMeshCompoundHarmonicAnalysis
        )

    @property
    def zerol_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6314.ZerolBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6314,
        )

        return self.__parent__._cast(_6314.ZerolBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis":
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
class AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis(
    _6218.ConicalGearMeshCompoundHarmonicAnalysis
):
    """AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS

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
    ) -> "List[_5974.AGMAGleasonConicalGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.AGMAGleasonConicalGearMeshHarmonicAnalysis]

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
    ) -> "List[_5974.AGMAGleasonConicalGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.AGMAGleasonConicalGearMeshHarmonicAnalysis]

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
    ) -> "_Cast_AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis
        """
        return _Cast_AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis(self)
