"""BevelGearMeshStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses import _4024

_BEVEL_GEAR_MESH_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "BevelGearMeshStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4031,
        _4052,
        _4055,
        _4080,
        _4087,
        _4123,
        _4132,
        _4135,
        _4153,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2524

    Self = TypeVar("Self", bound="BevelGearMeshStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearMeshStabilityAnalysis._Cast_BevelGearMeshStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshStabilityAnalysis:
    """Special nested class for casting BevelGearMeshStabilityAnalysis to subclasses."""

    __parent__: "BevelGearMeshStabilityAnalysis"

    @property
    def agma_gleason_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4024.AGMAGleasonConicalGearMeshStabilityAnalysis":
        return self.__parent__._cast(_4024.AGMAGleasonConicalGearMeshStabilityAnalysis)

    @property
    def conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4052.ConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4052,
        )

        return self.__parent__._cast(_4052.ConicalGearMeshStabilityAnalysis)

    @property
    def gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4080.GearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4080,
        )

        return self.__parent__._cast(_4080.GearMeshStabilityAnalysis)

    @property
    def inter_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4087.InterMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4087,
        )

        return self.__parent__._cast(
            _4087.InterMountableComponentConnectionStabilityAnalysis
        )

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "_4055.ConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4055,
        )

        return self.__parent__._cast(_4055.ConnectionStabilityAnalysis)

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
    def bevel_differential_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4031.BevelDifferentialGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4031,
        )

        return self.__parent__._cast(_4031.BevelDifferentialGearMeshStabilityAnalysis)

    @property
    def spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4123.SpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4123,
        )

        return self.__parent__._cast(_4123.SpiralBevelGearMeshStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4132.StraightBevelDiffGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4132,
        )

        return self.__parent__._cast(_4132.StraightBevelDiffGearMeshStabilityAnalysis)

    @property
    def straight_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4135.StraightBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4135,
        )

        return self.__parent__._cast(_4135.StraightBevelGearMeshStabilityAnalysis)

    @property
    def zerol_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4153.ZerolBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4153,
        )

        return self.__parent__._cast(_4153.ZerolBevelGearMeshStabilityAnalysis)

    @property
    def bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "BevelGearMeshStabilityAnalysis":
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
class BevelGearMeshStabilityAnalysis(_4024.AGMAGleasonConicalGearMeshStabilityAnalysis):
    """BevelGearMeshStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH_STABILITY_ANALYSIS

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
    def cast_to(self: "Self") -> "_Cast_BevelGearMeshStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshStabilityAnalysis
        """
        return _Cast_BevelGearMeshStabilityAnalysis(self)
