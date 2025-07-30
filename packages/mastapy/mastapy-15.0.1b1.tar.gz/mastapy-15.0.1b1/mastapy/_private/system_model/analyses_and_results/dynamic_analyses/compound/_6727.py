"""AGMAGleasonConicalGearMeshCompoundDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6755,
)

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "AGMAGleasonConicalGearMeshCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6594,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6734,
        _6739,
        _6757,
        _6781,
        _6785,
        _6787,
        _6824,
        _6830,
        _6833,
        _6851,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshCompoundDynamicAnalysis._Cast_AGMAGleasonConicalGearMeshCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshCompoundDynamicAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearMeshCompoundDynamicAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshCompoundDynamicAnalysis"

    @property
    def conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6755.ConicalGearMeshCompoundDynamicAnalysis":
        return self.__parent__._cast(_6755.ConicalGearMeshCompoundDynamicAnalysis)

    @property
    def gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6781.GearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6781,
        )

        return self.__parent__._cast(_6781.GearMeshCompoundDynamicAnalysis)

    @property
    def inter_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6787.InterMountableComponentConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6787,
        )

        return self.__parent__._cast(
            _6787.InterMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6757.ConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6757,
        )

        return self.__parent__._cast(_6757.ConnectionCompoundDynamicAnalysis)

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
    def bevel_differential_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6734.BevelDifferentialGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6734,
        )

        return self.__parent__._cast(
            _6734.BevelDifferentialGearMeshCompoundDynamicAnalysis
        )

    @property
    def bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6739.BevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6739,
        )

        return self.__parent__._cast(_6739.BevelGearMeshCompoundDynamicAnalysis)

    @property
    def hypoid_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6785.HypoidGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6785,
        )

        return self.__parent__._cast(_6785.HypoidGearMeshCompoundDynamicAnalysis)

    @property
    def spiral_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6824.SpiralBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6824,
        )

        return self.__parent__._cast(_6824.SpiralBevelGearMeshCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6830.StraightBevelDiffGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6830,
        )

        return self.__parent__._cast(
            _6830.StraightBevelDiffGearMeshCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6833.StraightBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6833,
        )

        return self.__parent__._cast(_6833.StraightBevelGearMeshCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6851.ZerolBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6851,
        )

        return self.__parent__._cast(_6851.ZerolBevelGearMeshCompoundDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshCompoundDynamicAnalysis":
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
class AGMAGleasonConicalGearMeshCompoundDynamicAnalysis(
    _6755.ConicalGearMeshCompoundDynamicAnalysis
):
    """AGMAGleasonConicalGearMeshCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS

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
    ) -> "List[_6594.AGMAGleasonConicalGearMeshDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearMeshDynamicAnalysis]

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
    ) -> "List[_6594.AGMAGleasonConicalGearMeshDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearMeshDynamicAnalysis]

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
    ) -> "_Cast_AGMAGleasonConicalGearMeshCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshCompoundDynamicAnalysis
        """
        return _Cast_AGMAGleasonConicalGearMeshCompoundDynamicAnalysis(self)
