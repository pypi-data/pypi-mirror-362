"""StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _7010,
)

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6970,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6998,
        _7026,
        _7028,
        _7052,
        _7058,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2546

    Self = TypeVar(
        "Self", bound="StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis._Cast_StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis:
    """Special nested class for casting StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis"

    @property
    def bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7010.BevelGearMeshCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_7010.BevelGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6998.AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6998,
        )

        return self.__parent__._cast(
            _6998.AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7026.ConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7026,
        )

        return self.__parent__._cast(_7026.ConicalGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7052.GearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7052,
        )

        return self.__parent__._cast(_7052.GearMeshCompoundCriticalSpeedAnalysis)

    @property
    def inter_mountable_component_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7058.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7058,
        )

        return self.__parent__._cast(
            _7058.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7028.ConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7028,
        )

        return self.__parent__._cast(_7028.ConnectionCompoundCriticalSpeedAnalysis)

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
    def straight_bevel_diff_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis":
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
class StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis(
    _7010.BevelGearMeshCompoundCriticalSpeedAnalysis
):
    """StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2546.StraightBevelDiffGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh

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
    def connection_design(self: "Self") -> "_2546.StraightBevelDiffGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh

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
    ) -> "List[_6970.StraightBevelDiffGearMeshCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.StraightBevelDiffGearMeshCriticalSpeedAnalysis]

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
    ) -> "List[_6970.StraightBevelDiffGearMeshCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.StraightBevelDiffGearMeshCriticalSpeedAnalysis]

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
    ) -> "_Cast_StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis
        """
        return _Cast_StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis(self)
