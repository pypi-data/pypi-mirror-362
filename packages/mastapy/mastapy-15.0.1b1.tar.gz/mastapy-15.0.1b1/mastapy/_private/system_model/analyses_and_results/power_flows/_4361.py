"""InterMountableComponentConnectionPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4328

_INTER_MOUNTABLE_COMPONENT_CONNECTION_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "InterMountableComponentConnectionPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4297,
        _4302,
        _4304,
        _4309,
        _4314,
        _4319,
        _4322,
        _4325,
        _4330,
        _4333,
        _4341,
        _4347,
        _4354,
        _4358,
        _4362,
        _4365,
        _4368,
        _4378,
        _4390,
        _4392,
        _4399,
        _4402,
        _4405,
        _4408,
        _4418,
        _4424,
        _4427,
    )
    from mastapy._private.system_model.connections_and_sockets import _2502

    Self = TypeVar("Self", bound="InterMountableComponentConnectionPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionPowerFlow:
    """Special nested class for casting InterMountableComponentConnectionPowerFlow to subclasses."""

    __parent__: "InterMountableComponentConnectionPowerFlow"

    @property
    def connection_power_flow(self: "CastSelf") -> "_4328.ConnectionPowerFlow":
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
    def agma_gleason_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4297.AGMAGleasonConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4297

        return self.__parent__._cast(_4297.AGMAGleasonConicalGearMeshPowerFlow)

    @property
    def belt_connection_power_flow(self: "CastSelf") -> "_4302.BeltConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4302

        return self.__parent__._cast(_4302.BeltConnectionPowerFlow)

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
    def clutch_connection_power_flow(
        self: "CastSelf",
    ) -> "_4314.ClutchConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4314

        return self.__parent__._cast(_4314.ClutchConnectionPowerFlow)

    @property
    def concept_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4319.ConceptCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4319

        return self.__parent__._cast(_4319.ConceptCouplingConnectionPowerFlow)

    @property
    def concept_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4322.ConceptGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4322

        return self.__parent__._cast(_4322.ConceptGearMeshPowerFlow)

    @property
    def conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4325.ConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4325

        return self.__parent__._cast(_4325.ConicalGearMeshPowerFlow)

    @property
    def coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4330.CouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4330

        return self.__parent__._cast(_4330.CouplingConnectionPowerFlow)

    @property
    def cvt_belt_connection_power_flow(
        self: "CastSelf",
    ) -> "_4333.CVTBeltConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4333

        return self.__parent__._cast(_4333.CVTBeltConnectionPowerFlow)

    @property
    def cylindrical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4341.CylindricalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4341

        return self.__parent__._cast(_4341.CylindricalGearMeshPowerFlow)

    @property
    def face_gear_mesh_power_flow(self: "CastSelf") -> "_4347.FaceGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4347

        return self.__parent__._cast(_4347.FaceGearMeshPowerFlow)

    @property
    def gear_mesh_power_flow(self: "CastSelf") -> "_4354.GearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4354

        return self.__parent__._cast(_4354.GearMeshPowerFlow)

    @property
    def hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4358.HypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4358

        return self.__parent__._cast(_4358.HypoidGearMeshPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4362.KlingelnbergCycloPalloidConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4362

        return self.__parent__._cast(
            _4362.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4365.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4365

        return self.__parent__._cast(
            _4365.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4368.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4368

        return self.__parent__._cast(
            _4368.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        )

    @property
    def part_to_part_shear_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4378.PartToPartShearCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4378

        return self.__parent__._cast(_4378.PartToPartShearCouplingConnectionPowerFlow)

    @property
    def ring_pins_to_disc_connection_power_flow(
        self: "CastSelf",
    ) -> "_4390.RingPinsToDiscConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4390

        return self.__parent__._cast(_4390.RingPinsToDiscConnectionPowerFlow)

    @property
    def rolling_ring_connection_power_flow(
        self: "CastSelf",
    ) -> "_4392.RollingRingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4392

        return self.__parent__._cast(_4392.RollingRingConnectionPowerFlow)

    @property
    def spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4399.SpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4399

        return self.__parent__._cast(_4399.SpiralBevelGearMeshPowerFlow)

    @property
    def spring_damper_connection_power_flow(
        self: "CastSelf",
    ) -> "_4402.SpringDamperConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4402

        return self.__parent__._cast(_4402.SpringDamperConnectionPowerFlow)

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
    def torque_converter_connection_power_flow(
        self: "CastSelf",
    ) -> "_4418.TorqueConverterConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4418

        return self.__parent__._cast(_4418.TorqueConverterConnectionPowerFlow)

    @property
    def worm_gear_mesh_power_flow(self: "CastSelf") -> "_4424.WormGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4424

        return self.__parent__._cast(_4424.WormGearMeshPowerFlow)

    @property
    def zerol_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4427.ZerolBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4427

        return self.__parent__._cast(_4427.ZerolBevelGearMeshPowerFlow)

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionPowerFlow":
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
class InterMountableComponentConnectionPowerFlow(_4328.ConnectionPowerFlow):
    """InterMountableComponentConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2502.InterMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.InterMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_InterMountableComponentConnectionPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionPowerFlow
        """
        return _Cast_InterMountableComponentConnectionPowerFlow(self)
