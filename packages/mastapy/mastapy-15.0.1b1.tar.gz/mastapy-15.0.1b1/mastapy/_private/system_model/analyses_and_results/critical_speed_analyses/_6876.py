"""BevelGearMeshCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6864,
)

_BEVEL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "BevelGearMeshCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6871,
        _6892,
        _6894,
        _6921,
        _6927,
        _6964,
        _6970,
        _6973,
        _6991,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2524

    Self = TypeVar("Self", bound="BevelGearMeshCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearMeshCriticalSpeedAnalysis._Cast_BevelGearMeshCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshCriticalSpeedAnalysis:
    """Special nested class for casting BevelGearMeshCriticalSpeedAnalysis to subclasses."""

    __parent__: "BevelGearMeshCriticalSpeedAnalysis"

    @property
    def agma_gleason_conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6864.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _6864.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis
        )

    @property
    def conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6892.ConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6892,
        )

        return self.__parent__._cast(_6892.ConicalGearMeshCriticalSpeedAnalysis)

    @property
    def gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6921.GearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6921,
        )

        return self.__parent__._cast(_6921.GearMeshCriticalSpeedAnalysis)

    @property
    def inter_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6927.InterMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6927,
        )

        return self.__parent__._cast(
            _6927.InterMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6894.ConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6894,
        )

        return self.__parent__._cast(_6894.ConnectionCriticalSpeedAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def bevel_differential_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6871.BevelDifferentialGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6871,
        )

        return self.__parent__._cast(
            _6871.BevelDifferentialGearMeshCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6964.SpiralBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6964,
        )

        return self.__parent__._cast(_6964.SpiralBevelGearMeshCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6970.StraightBevelDiffGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6970,
        )

        return self.__parent__._cast(
            _6970.StraightBevelDiffGearMeshCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6973.StraightBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6973,
        )

        return self.__parent__._cast(_6973.StraightBevelGearMeshCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6991.ZerolBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6991,
        )

        return self.__parent__._cast(_6991.ZerolBevelGearMeshCriticalSpeedAnalysis)

    @property
    def bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "BevelGearMeshCriticalSpeedAnalysis":
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
class BevelGearMeshCriticalSpeedAnalysis(
    _6864.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis
):
    """BevelGearMeshCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2524.BevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.BevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearMeshCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshCriticalSpeedAnalysis
        """
        return _Cast_BevelGearMeshCriticalSpeedAnalysis(self)
