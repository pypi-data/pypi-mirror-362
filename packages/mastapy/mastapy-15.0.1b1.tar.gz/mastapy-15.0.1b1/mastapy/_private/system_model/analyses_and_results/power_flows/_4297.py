"""AGMAGleasonConicalGearMeshPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4325

_AGMA_GLEASON_CONICAL_GEAR_MESH_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "AGMAGleasonConicalGearMeshPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4304,
        _4309,
        _4328,
        _4354,
        _4358,
        _4361,
        _4399,
        _4405,
        _4408,
        _4427,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2520

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshPowerFlow._Cast_AGMAGleasonConicalGearMeshPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshPowerFlow:
    """Special nested class for casting AGMAGleasonConicalGearMeshPowerFlow to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshPowerFlow"

    @property
    def conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4325.ConicalGearMeshPowerFlow":
        return self.__parent__._cast(_4325.ConicalGearMeshPowerFlow)

    @property
    def gear_mesh_power_flow(self: "CastSelf") -> "_4354.GearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4354

        return self.__parent__._cast(_4354.GearMeshPowerFlow)

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4361.InterMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4361

        return self.__parent__._cast(_4361.InterMountableComponentConnectionPowerFlow)

    @property
    def connection_power_flow(self: "CastSelf") -> "_4328.ConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4328

        return self.__parent__._cast(_4328.ConnectionPowerFlow)

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
    def bevel_differential_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4304.BevelDifferentialGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4304

        return self.__parent__._cast(_4304.BevelDifferentialGearMeshPowerFlow)

    @property
    def bevel_gear_mesh_power_flow(self: "CastSelf") -> "_4309.BevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4309

        return self.__parent__._cast(_4309.BevelGearMeshPowerFlow)

    @property
    def hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4358.HypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4358

        return self.__parent__._cast(_4358.HypoidGearMeshPowerFlow)

    @property
    def spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4399.SpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4399

        return self.__parent__._cast(_4399.SpiralBevelGearMeshPowerFlow)

    @property
    def straight_bevel_diff_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4405.StraightBevelDiffGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4405

        return self.__parent__._cast(_4405.StraightBevelDiffGearMeshPowerFlow)

    @property
    def straight_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4408.StraightBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4408

        return self.__parent__._cast(_4408.StraightBevelGearMeshPowerFlow)

    @property
    def zerol_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4427.ZerolBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4427

        return self.__parent__._cast(_4427.ZerolBevelGearMeshPowerFlow)

    @property
    def agma_gleason_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshPowerFlow":
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
class AGMAGleasonConicalGearMeshPowerFlow(_4325.ConicalGearMeshPowerFlow):
    """AGMAGleasonConicalGearMeshPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2520.AGMAGleasonConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearMeshPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshPowerFlow
        """
        return _Cast_AGMAGleasonConicalGearMeshPowerFlow(self)
