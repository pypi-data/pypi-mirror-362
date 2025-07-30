"""CycloidalDiscAxialRightSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2507

_CYCLOIDAL_DISC_AXIAL_RIGHT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscAxialRightSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2497,
        _2515,
        _2517,
    )

    Self = TypeVar("Self", bound="CycloidalDiscAxialRightSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscAxialRightSocket._Cast_CycloidalDiscAxialRightSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscAxialRightSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscAxialRightSocket:
    """Special nested class for casting CycloidalDiscAxialRightSocket to subclasses."""

    __parent__: "CycloidalDiscAxialRightSocket"

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2507.OuterShaftSocketBase":
        return self.__parent__._cast(_2507.OuterShaftSocketBase)

    @property
    def shaft_socket(self: "CastSelf") -> "_2515.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2515

        return self.__parent__._cast(_2515.ShaftSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2497.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2497

        return self.__parent__._cast(_2497.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "CycloidalDiscAxialRightSocket":
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
class CycloidalDiscAxialRightSocket(_2507.OuterShaftSocketBase):
    """CycloidalDiscAxialRightSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_AXIAL_RIGHT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscAxialRightSocket":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscAxialRightSocket
        """
        return _Cast_CycloidalDiscAxialRightSocket(self)
