"""RingPinsSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2497

_RING_PINS_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal", "RingPinsSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2517

    Self = TypeVar("Self", bound="RingPinsSocket")
    CastSelf = TypeVar("CastSelf", bound="RingPinsSocket._Cast_RingPinsSocket")


__docformat__ = "restructuredtext en"
__all__ = ("RingPinsSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPinsSocket:
    """Special nested class for casting RingPinsSocket to subclasses."""

    __parent__: "RingPinsSocket"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2497.CylindricalSocket":
        return self.__parent__._cast(_2497.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def ring_pins_socket(self: "CastSelf") -> "RingPinsSocket":
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
class RingPinsSocket(_2497.CylindricalSocket):
    """RingPinsSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_PINS_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RingPinsSocket":
        """Cast to another type.

        Returns:
            _Cast_RingPinsSocket
        """
        return _Cast_RingPinsSocket(self)
