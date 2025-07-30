"""ConnectionSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7882

_CONNECTION_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ConnectionSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials.efficiency import _391
    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4328
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2929,
        _2930,
        _2940,
        _2942,
        _2947,
        _2952,
        _2955,
        _2958,
        _2961,
        _2965,
        _2970,
        _2973,
        _2977,
        _2978,
        _2980,
        _2981,
        _2982,
        _2995,
        _3000,
        _3004,
        _3008,
        _3009,
        _3012,
        _3015,
        _3029,
        _3032,
        _3038,
        _3041,
        _3048,
        _3050,
        _3053,
        _3056,
        _3059,
        _3068,
        _3071,
        _3079,
        _3082,
    )
    from mastapy._private.system_model.connections_and_sockets import _2493

    Self = TypeVar("Self", bound="ConnectionSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectionSystemDeflection._Cast_ConnectionSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionSystemDeflection:
    """Special nested class for casting ConnectionSystemDeflection to subclasses."""

    __parent__: "ConnectionSystemDeflection"

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7882.ConnectionFEAnalysis":
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
    def abstract_shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2929.AbstractShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2929,
        )

        return self.__parent__._cast(
            _2929.AbstractShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2930.AGMAGleasonConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2930,
        )

        return self.__parent__._cast(_2930.AGMAGleasonConicalGearMeshSystemDeflection)

    @property
    def belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2940.BeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2940,
        )

        return self.__parent__._cast(_2940.BeltConnectionSystemDeflection)

    @property
    def bevel_differential_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2942.BevelDifferentialGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2942,
        )

        return self.__parent__._cast(_2942.BevelDifferentialGearMeshSystemDeflection)

    @property
    def bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2947.BevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2947,
        )

        return self.__parent__._cast(_2947.BevelGearMeshSystemDeflection)

    @property
    def clutch_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2952.ClutchConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2952,
        )

        return self.__parent__._cast(_2952.ClutchConnectionSystemDeflection)

    @property
    def coaxial_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2955.CoaxialConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2955,
        )

        return self.__parent__._cast(_2955.CoaxialConnectionSystemDeflection)

    @property
    def concept_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2958.ConceptCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2958,
        )

        return self.__parent__._cast(_2958.ConceptCouplingConnectionSystemDeflection)

    @property
    def concept_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2961.ConceptGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2961,
        )

        return self.__parent__._cast(_2961.ConceptGearMeshSystemDeflection)

    @property
    def conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2965.ConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2965,
        )

        return self.__parent__._cast(_2965.ConicalGearMeshSystemDeflection)

    @property
    def coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2970.CouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2970,
        )

        return self.__parent__._cast(_2970.CouplingConnectionSystemDeflection)

    @property
    def cvt_belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2973.CVTBeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2973,
        )

        return self.__parent__._cast(_2973.CVTBeltConnectionSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2977.CycloidalDiscCentralBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2977,
        )

        return self.__parent__._cast(
            _2977.CycloidalDiscCentralBearingConnectionSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2978.CycloidalDiscPlanetaryBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2978,
        )

        return self.__parent__._cast(
            _2978.CycloidalDiscPlanetaryBearingConnectionSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2980.CylindricalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2980,
        )

        return self.__parent__._cast(_2980.CylindricalGearMeshSystemDeflection)

    @property
    def cylindrical_gear_mesh_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2981.CylindricalGearMeshSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2981,
        )

        return self.__parent__._cast(_2981.CylindricalGearMeshSystemDeflectionTimestep)

    @property
    def cylindrical_gear_mesh_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2982.CylindricalGearMeshSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2982,
        )

        return self.__parent__._cast(
            _2982.CylindricalGearMeshSystemDeflectionWithLTCAResults
        )

    @property
    def face_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2995.FaceGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2995,
        )

        return self.__parent__._cast(_2995.FaceGearMeshSystemDeflection)

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3000.GearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3000,
        )

        return self.__parent__._cast(_3000.GearMeshSystemDeflection)

    @property
    def hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3004.HypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3004,
        )

        return self.__parent__._cast(_3004.HypoidGearMeshSystemDeflection)

    @property
    def inter_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3008.InterMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3008,
        )

        return self.__parent__._cast(
            _3008.InterMountableComponentConnectionSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3009.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3009,
        )

        return self.__parent__._cast(
            _3009.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3012.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3012,
        )

        return self.__parent__._cast(
            _3012.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3015.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3015,
        )

        return self.__parent__._cast(
            _3015.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3029.PartToPartShearCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3029,
        )

        return self.__parent__._cast(
            _3029.PartToPartShearCouplingConnectionSystemDeflection
        )

    @property
    def planetary_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3032.PlanetaryConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3032,
        )

        return self.__parent__._cast(_3032.PlanetaryConnectionSystemDeflection)

    @property
    def ring_pins_to_disc_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3038.RingPinsToDiscConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3038,
        )

        return self.__parent__._cast(_3038.RingPinsToDiscConnectionSystemDeflection)

    @property
    def rolling_ring_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3041.RollingRingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3041,
        )

        return self.__parent__._cast(_3041.RollingRingConnectionSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3048.ShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3048,
        )

        return self.__parent__._cast(
            _3048.ShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3050.SpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3050,
        )

        return self.__parent__._cast(_3050.SpiralBevelGearMeshSystemDeflection)

    @property
    def spring_damper_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3053.SpringDamperConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3053,
        )

        return self.__parent__._cast(_3053.SpringDamperConnectionSystemDeflection)

    @property
    def straight_bevel_diff_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3056.StraightBevelDiffGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3056,
        )

        return self.__parent__._cast(_3056.StraightBevelDiffGearMeshSystemDeflection)

    @property
    def straight_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3059.StraightBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3059,
        )

        return self.__parent__._cast(_3059.StraightBevelGearMeshSystemDeflection)

    @property
    def torque_converter_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3071.TorqueConverterConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3071,
        )

        return self.__parent__._cast(_3071.TorqueConverterConnectionSystemDeflection)

    @property
    def worm_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3079.WormGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3079,
        )

        return self.__parent__._cast(_3079.WormGearMeshSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3082.ZerolBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3082,
        )

        return self.__parent__._cast(_3082.ZerolBevelGearMeshSystemDeflection)

    @property
    def connection_system_deflection(self: "CastSelf") -> "ConnectionSystemDeflection":
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
class ConnectionSystemDeflection(_7882.ConnectionFEAnalysis):
    """ConnectionSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def convergence_status(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConvergenceStatus")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def efficiency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Efficiency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def energy_loss_during_load_case(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyLossDuringLoadCase")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def has_converged(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasConverged")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_loaded(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLoaded")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def largest_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LargestPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def percentage_of_iterations_converged(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PercentageOfIterationsConverged")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reason_for_non_convergence(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonForNonConvergence")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def relaxation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Relaxation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_a_planetary_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketAPlanetaryPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_a_planetary_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketAPlanetaryTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_a_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketAPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_a_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketATorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_a_total_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketATotalPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_b_planetary_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketBPlanetaryPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_b_planetary_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketBPlanetaryTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_b_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketBPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_b_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketBTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def socket_b_total_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketBTotalPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

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
    def connection_design(self: "Self") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

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
    def power_loss(self: "Self") -> "_391.PowerLoss":
        """mastapy.materials.efficiency.PowerLoss

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoss")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_deflection(self: "Self") -> "_3068.SystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.SystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def power_flow_results(self: "Self") -> "_4328.ConnectionPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.ConnectionPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConnectionSystemDeflection
        """
        return _Cast_ConnectionSystemDeflection(self)
