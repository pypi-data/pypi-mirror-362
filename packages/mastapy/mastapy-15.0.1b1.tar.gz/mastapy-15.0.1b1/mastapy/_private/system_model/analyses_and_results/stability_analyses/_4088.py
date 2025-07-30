"""KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses import _4052

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4055,
        _4080,
        _4087,
        _4091,
        _4094,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2539

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis._Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"

    @property
    def conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4052.ConicalGearMeshStabilityAnalysis":
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
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4091.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4091,
        )

        return self.__parent__._cast(
            _4091.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_4094.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4094,
        )

        return self.__parent__._cast(
            _4094.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis":
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
class KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis(
    _4052.ConicalGearMeshStabilityAnalysis
):
    """KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_STABILITY_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(
        self: "Self",
    ) -> "_2539.KlingelnbergCycloPalloidConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis(self)
