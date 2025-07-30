"""ZerolBevelGearMeshDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6606

_ZEROL_BEVEL_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "ZerolBevelGearMeshDynamicAnalysis",
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
        _6594,
        _6622,
        _6624,
        _6650,
        _6656,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7858
    from mastapy._private.system_model.connections_and_sockets.gears import _2552

    Self = TypeVar("Self", bound="ZerolBevelGearMeshDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGearMeshDynamicAnalysis._Cast_ZerolBevelGearMeshDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearMeshDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearMeshDynamicAnalysis:
    """Special nested class for casting ZerolBevelGearMeshDynamicAnalysis to subclasses."""

    __parent__: "ZerolBevelGearMeshDynamicAnalysis"

    @property
    def bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6606.BevelGearMeshDynamicAnalysis":
        return self.__parent__._cast(_6606.BevelGearMeshDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6594.AGMAGleasonConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6594,
        )

        return self.__parent__._cast(_6594.AGMAGleasonConicalGearMeshDynamicAnalysis)

    @property
    def conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6622.ConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6622,
        )

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
    def zerol_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "ZerolBevelGearMeshDynamicAnalysis":
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
class ZerolBevelGearMeshDynamicAnalysis(_6606.BevelGearMeshDynamicAnalysis):
    """ZerolBevelGearMeshDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_MESH_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2552.ZerolBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh

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
    def connection_load_case(self: "Self") -> "_7858.ZerolBevelGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearMeshDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearMeshDynamicAnalysis
        """
        return _Cast_ZerolBevelGearMeshDynamicAnalysis(self)
