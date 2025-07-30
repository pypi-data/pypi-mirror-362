"""ShaftSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2497

_SHAFT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "ShaftSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2500,
        _2501,
        _2506,
        _2507,
        _2517,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2554,
        _2555,
        _2557,
    )

    Self = TypeVar("Self", bound="ShaftSocket")
    CastSelf = TypeVar("CastSelf", bound="ShaftSocket._Cast_ShaftSocket")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSocket:
    """Special nested class for casting ShaftSocket to subclasses."""

    __parent__: "ShaftSocket"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2497.CylindricalSocket":
        return self.__parent__._cast(_2497.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2500.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2500

        return self.__parent__._cast(_2500.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2501.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2501

        return self.__parent__._cast(_2501.InnerShaftSocketBase)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2506.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2506

        return self.__parent__._cast(_2506.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2507.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2507

        return self.__parent__._cast(_2507.OuterShaftSocketBase)

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
    def shaft_socket(self: "CastSelf") -> "ShaftSocket":
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
class ShaftSocket(_2497.CylindricalSocket):
    """ShaftSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSocket":
        """Cast to another type.

        Returns:
            _Cast_ShaftSocket
        """
        return _Cast_ShaftSocket(self)
