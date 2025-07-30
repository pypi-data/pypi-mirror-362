"""SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation"""

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
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7146,
)

_SPIRAL_BEVEL_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7133,
        _7162,
        _7164,
        _7188,
        _7195,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7825
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3050,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2544

    Self = TypeVar(
        "Self", bound="SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation._Cast_SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation"

    @property
    def bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7146.BevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7146.BevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7133.AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7133,
        )

        return self.__parent__._cast(
            _7133.AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7162.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7162,
        )

        return self.__parent__._cast(
            _7162.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7188.GearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7188,
        )

        return self.__parent__._cast(
            _7188.GearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def inter_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7195.InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7195,
        )

        return self.__parent__._cast(
            _7195.InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7164.ConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7164,
        )

        return self.__parent__._cast(
            _7164.ConnectionAdvancedTimeSteppingAnalysisForModulation
        )

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
    def spiral_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
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
class SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation(
    _7146.BevelGearMeshAdvancedTimeSteppingAnalysisForModulation
):
    """SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SPIRAL_BEVEL_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2544.SpiralBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh

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
    def connection_load_case(self: "Self") -> "_7825.SpiralBevelGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_deflection_results(
        self: "Self",
    ) -> "_3050.SpiralBevelGearMeshSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.SpiralBevelGearMeshSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation(self)
