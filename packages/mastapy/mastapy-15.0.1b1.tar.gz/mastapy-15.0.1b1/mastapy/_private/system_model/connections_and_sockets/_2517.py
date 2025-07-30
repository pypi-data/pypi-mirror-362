"""Socket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2487,
        _2488,
        _2493,
        _2495,
        _2497,
        _2499,
        _2500,
        _2501,
        _2503,
        _2504,
        _2505,
        _2506,
        _2507,
        _2509,
        _2510,
        _2511,
        _2514,
        _2515,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2564,
        _2566,
        _2568,
        _2570,
        _2572,
        _2574,
        _2575,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2554,
        _2555,
        _2557,
        _2558,
        _2560,
        _2561,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2521,
        _2523,
        _2525,
        _2527,
        _2529,
        _2531,
        _2533,
        _2535,
        _2537,
        _2538,
        _2542,
        _2543,
        _2545,
        _2547,
        _2549,
        _2551,
        _2553,
    )
    from mastapy._private.system_model.part_model import _2670, _2671

    Self = TypeVar("Self", bound="Socket")
    CastSelf = TypeVar("CastSelf", bound="Socket._Cast_Socket")


__docformat__ = "restructuredtext en"
__all__ = ("Socket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Socket:
    """Special nested class for casting Socket to subclasses."""

    __parent__: "Socket"

    @property
    def bearing_inner_socket(self: "CastSelf") -> "_2487.BearingInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2487

        return self.__parent__._cast(_2487.BearingInnerSocket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2488.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2488

        return self.__parent__._cast(_2488.BearingOuterSocket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "_2495.CVTPulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2495

        return self.__parent__._cast(_2495.CVTPulleySocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2497.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2497

        return self.__parent__._cast(_2497.CylindricalSocket)

    @property
    def electric_machine_stator_socket(
        self: "CastSelf",
    ) -> "_2499.ElectricMachineStatorSocket":
        from mastapy._private.system_model.connections_and_sockets import _2499

        return self.__parent__._cast(_2499.ElectricMachineStatorSocket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2500.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2500

        return self.__parent__._cast(_2500.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2501.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2501

        return self.__parent__._cast(_2501.InnerShaftSocketBase)

    @property
    def mountable_component_inner_socket(
        self: "CastSelf",
    ) -> "_2503.MountableComponentInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2503

        return self.__parent__._cast(_2503.MountableComponentInnerSocket)

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "_2504.MountableComponentOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2504

        return self.__parent__._cast(_2504.MountableComponentOuterSocket)

    @property
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2505.MountableComponentSocket":
        from mastapy._private.system_model.connections_and_sockets import _2505

        return self.__parent__._cast(_2505.MountableComponentSocket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2506.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2506

        return self.__parent__._cast(_2506.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2507.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2507

        return self.__parent__._cast(_2507.OuterShaftSocketBase)

    @property
    def planetary_socket(self: "CastSelf") -> "_2509.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2509

        return self.__parent__._cast(_2509.PlanetarySocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2510.PlanetarySocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2510

        return self.__parent__._cast(_2510.PlanetarySocketBase)

    @property
    def pulley_socket(self: "CastSelf") -> "_2511.PulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2511

        return self.__parent__._cast(_2511.PulleySocket)

    @property
    def rolling_ring_socket(self: "CastSelf") -> "_2514.RollingRingSocket":
        from mastapy._private.system_model.connections_and_sockets import _2514

        return self.__parent__._cast(_2514.RollingRingSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "_2515.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2515

        return self.__parent__._cast(_2515.ShaftSocket)

    @property
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2521.AGMAGleasonConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2521

        return self.__parent__._cast(_2521.AGMAGleasonConicalGearTeethSocket)

    @property
    def bevel_differential_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2523.BevelDifferentialGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2523

        return self.__parent__._cast(_2523.BevelDifferentialGearTeethSocket)

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2525.BevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2525

        return self.__parent__._cast(_2525.BevelGearTeethSocket)

    @property
    def concept_gear_teeth_socket(self: "CastSelf") -> "_2527.ConceptGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2527

        return self.__parent__._cast(_2527.ConceptGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2529.ConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2529

        return self.__parent__._cast(_2529.ConicalGearTeethSocket)

    @property
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2531.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2531

        return self.__parent__._cast(_2531.CylindricalGearTeethSocket)

    @property
    def face_gear_teeth_socket(self: "CastSelf") -> "_2533.FaceGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2533

        return self.__parent__._cast(_2533.FaceGearTeethSocket)

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2535.GearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2535

        return self.__parent__._cast(_2535.GearTeethSocket)

    @property
    def hypoid_gear_teeth_socket(self: "CastSelf") -> "_2537.HypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2537

        return self.__parent__._cast(_2537.HypoidGearTeethSocket)

    @property
    def klingelnberg_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2538.KlingelnbergConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2538

        return self.__parent__._cast(_2538.KlingelnbergConicalGearTeethSocket)

    @property
    def klingelnberg_hypoid_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2542.KlingelnbergHypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2542

        return self.__parent__._cast(_2542.KlingelnbergHypoidGearTeethSocket)

    @property
    def klingelnberg_spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2543.KlingelnbergSpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2543

        return self.__parent__._cast(_2543.KlingelnbergSpiralBevelGearTeethSocket)

    @property
    def spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2545.SpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2545

        return self.__parent__._cast(_2545.SpiralBevelGearTeethSocket)

    @property
    def straight_bevel_diff_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2547.StraightBevelDiffGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2547

        return self.__parent__._cast(_2547.StraightBevelDiffGearTeethSocket)

    @property
    def straight_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2549.StraightBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2549

        return self.__parent__._cast(_2549.StraightBevelGearTeethSocket)

    @property
    def worm_gear_teeth_socket(self: "CastSelf") -> "_2551.WormGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2551

        return self.__parent__._cast(_2551.WormGearTeethSocket)

    @property
    def zerol_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2553.ZerolBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2553

        return self.__parent__._cast(_2553.ZerolBevelGearTeethSocket)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2554.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2554,
        )

        return self.__parent__._cast(_2554.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2555.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2555,
        )

        return self.__parent__._cast(_2555.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2557.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2557,
        )

        return self.__parent__._cast(_2557.CycloidalDiscInnerSocket)

    @property
    def cycloidal_disc_outer_socket(
        self: "CastSelf",
    ) -> "_2558.CycloidalDiscOuterSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2558,
        )

        return self.__parent__._cast(_2558.CycloidalDiscOuterSocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2560.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2560,
        )

        return self.__parent__._cast(_2560.CycloidalDiscPlanetaryBearingSocket)

    @property
    def ring_pins_socket(self: "CastSelf") -> "_2561.RingPinsSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2561,
        )

        return self.__parent__._cast(_2561.RingPinsSocket)

    @property
    def clutch_socket(self: "CastSelf") -> "_2564.ClutchSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2564,
        )

        return self.__parent__._cast(_2564.ClutchSocket)

    @property
    def concept_coupling_socket(self: "CastSelf") -> "_2566.ConceptCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2566,
        )

        return self.__parent__._cast(_2566.ConceptCouplingSocket)

    @property
    def coupling_socket(self: "CastSelf") -> "_2568.CouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2568,
        )

        return self.__parent__._cast(_2568.CouplingSocket)

    @property
    def part_to_part_shear_coupling_socket(
        self: "CastSelf",
    ) -> "_2570.PartToPartShearCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2570,
        )

        return self.__parent__._cast(_2570.PartToPartShearCouplingSocket)

    @property
    def spring_damper_socket(self: "CastSelf") -> "_2572.SpringDamperSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2572,
        )

        return self.__parent__._cast(_2572.SpringDamperSocket)

    @property
    def torque_converter_pump_socket(
        self: "CastSelf",
    ) -> "_2574.TorqueConverterPumpSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2574,
        )

        return self.__parent__._cast(_2574.TorqueConverterPumpSocket)

    @property
    def torque_converter_turbine_socket(
        self: "CastSelf",
    ) -> "_2575.TorqueConverterTurbineSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2575,
        )

        return self.__parent__._cast(_2575.TorqueConverterTurbineSocket)

    @property
    def socket(self: "CastSelf") -> "Socket":
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
class Socket(_0.APIBase):
    """Socket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def connected_components(self: "Self") -> "List[_2670.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connections(self: "Self") -> "List[_2493.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def owner(self: "Self") -> "_2670.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Owner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def connect_to(
        self: "Self", component: "_2670.Component"
    ) -> "_2671.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ConnectTo",
            [_COMPONENT],
            component.wrapped if component else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def connect_to_socket(
        self: "Self", socket: "Socket"
    ) -> "_2671.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "ConnectTo", [_SOCKET], socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def connection_to(self: "Self", socket: "Socket") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "ConnectionTo", socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_possible_sockets_to_connect_to(
        self: "Self", component_to_connect_to: "_2670.Component"
    ) -> "List[Socket]":
        """List[mastapy.system_model.connections_and_sockets.Socket]

        Args:
            component_to_connect_to (mastapy.system_model.part_model.Component)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped,
                "GetPossibleSocketsToConnectTo",
                component_to_connect_to.wrapped if component_to_connect_to else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Socket":
        """Cast to another type.

        Returns:
            _Cast_Socket
        """
        return _Cast_Socket(self)
