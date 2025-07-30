"""Connection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model import _2414

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2486,
        _2489,
        _2490,
        _2494,
        _2502,
        _2508,
        _2513,
        _2516,
        _2517,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2563,
        _2565,
        _2567,
        _2569,
        _2571,
        _2573,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2556,
        _2559,
        _2562,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2520,
        _2522,
        _2524,
        _2526,
        _2528,
        _2530,
        _2532,
        _2534,
        _2536,
        _2539,
        _2540,
        _2541,
        _2544,
        _2546,
        _2548,
        _2550,
        _2552,
    )
    from mastapy._private.system_model.part_model import _2670

    Self = TypeVar("Self", bound="Connection")
    CastSelf = TypeVar("CastSelf", bound="Connection._Cast_Connection")


__docformat__ = "restructuredtext en"
__all__ = ("Connection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Connection:
    """Special nested class for casting Connection to subclasses."""

    __parent__: "Connection"

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2486.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2486

        return self.__parent__._cast(_2486.AbstractShaftToMountableComponentConnection)

    @property
    def belt_connection(self: "CastSelf") -> "_2489.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2489

        return self.__parent__._cast(_2489.BeltConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2490.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2490

        return self.__parent__._cast(_2490.CoaxialConnection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2494.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2494

        return self.__parent__._cast(_2494.CVTBeltConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2502.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2502

        return self.__parent__._cast(_2502.InterMountableComponentConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2508.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2508

        return self.__parent__._cast(_2508.PlanetaryConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2513.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2513

        return self.__parent__._cast(_2513.RollingRingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2516.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2516

        return self.__parent__._cast(_2516.ShaftToMountableComponentConnection)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2520.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2520

        return self.__parent__._cast(_2520.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2522.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2522

        return self.__parent__._cast(_2522.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2524.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2524

        return self.__parent__._cast(_2524.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2526.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2526

        return self.__parent__._cast(_2526.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2528.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2528

        return self.__parent__._cast(_2528.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2530.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2530

        return self.__parent__._cast(_2530.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2532.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2532

        return self.__parent__._cast(_2532.FaceGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2534.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2534

        return self.__parent__._cast(_2534.GearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2536.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2536

        return self.__parent__._cast(_2536.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2539.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2539

        return self.__parent__._cast(_2539.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2540.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2540

        return self.__parent__._cast(_2540.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2541.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2541

        return self.__parent__._cast(_2541.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2544.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2544

        return self.__parent__._cast(_2544.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2546.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2546

        return self.__parent__._cast(_2546.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2548.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2548

        return self.__parent__._cast(_2548.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2550.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2550

        return self.__parent__._cast(_2550.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2552.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2552

        return self.__parent__._cast(_2552.ZerolBevelGearMesh)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2556.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2556,
        )

        return self.__parent__._cast(_2556.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2559.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2559,
        )

        return self.__parent__._cast(_2559.CycloidalDiscPlanetaryBearingConnection)

    @property
    def ring_pins_to_disc_connection(
        self: "CastSelf",
    ) -> "_2562.RingPinsToDiscConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2562,
        )

        return self.__parent__._cast(_2562.RingPinsToDiscConnection)

    @property
    def clutch_connection(self: "CastSelf") -> "_2563.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2563,
        )

        return self.__parent__._cast(_2563.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2565.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2565,
        )

        return self.__parent__._cast(_2565.ConceptCouplingConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "_2567.CouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2567,
        )

        return self.__parent__._cast(_2567.CouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2569.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2569,
        )

        return self.__parent__._cast(_2569.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2571.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2571,
        )

        return self.__parent__._cast(_2571.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2573.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2573,
        )

        return self.__parent__._cast(_2573.TorqueConverterConnection)

    @property
    def connection(self: "CastSelf") -> "Connection":
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
class Connection(_2414.DesignEntity):
    """Connection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionID")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def drawing_position(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "DrawingPosition")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @drawing_position.setter
    @exception_bridge
    @enforce_parameter_types
    def drawing_position(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DrawingPosition", value)

    @property
    @exception_bridge
    def full_name_without_root_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullNameWithoutRootName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def speed_ratio_from_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedRatioFromAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_ratio_from_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRatioFromAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def owner_a(self: "Self") -> "_2670.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OwnerA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def owner_b(self: "Self") -> "_2670.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OwnerB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def socket_a(self: "Self") -> "_2517.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def socket_b(self: "Self") -> "_2517.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def other_owner(self: "Self", component: "_2670.Component") -> "_2670.Component":
        """mastapy.system_model.part_model.Component

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "OtherOwner", component.wrapped if component else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def other_socket_for_component(
        self: "Self", component: "_2670.Component"
    ) -> "_2517.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "OtherSocket",
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
    def other_socket(self: "Self", socket: "_2517.Socket") -> "_2517.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "OtherSocket", [_SOCKET], socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def socket_for(self: "Self", component: "_2670.Component") -> "_2517.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "SocketFor", component.wrapped if component else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Connection":
        """Cast to another type.

        Returns:
            _Cast_Connection
        """
        return _Cast_Connection(self)
