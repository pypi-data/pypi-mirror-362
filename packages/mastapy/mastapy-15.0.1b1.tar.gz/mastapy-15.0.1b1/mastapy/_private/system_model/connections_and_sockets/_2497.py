"""CylindricalSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2517

_CYLINDRICAL_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2487,
        _2488,
        _2495,
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
    from mastapy._private.system_model.connections_and_sockets.gears import _2531

    Self = TypeVar("Self", bound="CylindricalSocket")
    CastSelf = TypeVar("CastSelf", bound="CylindricalSocket._Cast_CylindricalSocket")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSocket:
    """Special nested class for casting CylindricalSocket to subclasses."""

    __parent__: "CylindricalSocket"

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        return self.__parent__._cast(_2517.Socket)

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
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2531.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2531

        return self.__parent__._cast(_2531.CylindricalGearTeethSocket)

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
    def cylindrical_socket(self: "CastSelf") -> "CylindricalSocket":
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
class CylindricalSocket(_2517.Socket):
    """CylindricalSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSocket":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSocket
        """
        return _Cast_CylindricalSocket(self)
