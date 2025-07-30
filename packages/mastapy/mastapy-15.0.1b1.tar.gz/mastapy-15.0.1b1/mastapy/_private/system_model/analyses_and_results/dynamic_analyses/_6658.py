"""KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6622

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7882,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6624,
        _6650,
        _6656,
        _6661,
        _6664,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2539

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis._Cast_KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis"

    @property
    def conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6622.ConicalGearMeshDynamicAnalysis":
        return self.__parent__._cast(_6622.ConicalGearMeshDynamicAnalysis)

    @property
    def gear_mesh_dynamic_analysis(self: "CastSelf") -> "_6650.GearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6650,
        )

        return self.__parent__._cast(_6650.GearMeshDynamicAnalysis)

    @property
    def inter_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6656.InterMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6656,
        )

        return self.__parent__._cast(
            _6656.InterMountableComponentConnectionDynamicAnalysis
        )

    @property
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6624.ConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6624,
        )

        return self.__parent__._cast(_6624.ConnectionDynamicAnalysis)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7882.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7882,
        )

        return self.__parent__._cast(_7882.ConnectionFEAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6661.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6661,
        )

        return self.__parent__._cast(
            _6661.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6664.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6664,
        )

        return self.__parent__._cast(
            _6664.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis":
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
class KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis(
    _6622.ConicalGearMeshDynamicAnalysis
):
    """KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_DYNAMIC_ANALYSIS
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
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis(self)
