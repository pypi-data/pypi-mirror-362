"""ConnectedSockets"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CONNECTED_SOCKETS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "ConnectedSockets"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2493, _2517

    Self = TypeVar("Self", bound="ConnectedSockets")
    CastSelf = TypeVar("CastSelf", bound="ConnectedSockets._Cast_ConnectedSockets")


__docformat__ = "restructuredtext en"
__all__ = ("ConnectedSockets",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectedSockets:
    """Special nested class for casting ConnectedSockets to subclasses."""

    __parent__: "ConnectedSockets"

    @property
    def connected_sockets(self: "CastSelf") -> "ConnectedSockets":
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
class ConnectedSockets(_0.APIBase):
    """ConnectedSockets

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTED_SOCKETS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection(self: "Self") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connection")

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

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectedSockets":
        """Cast to another type.

        Returns:
            _Cast_ConnectedSockets
        """
        return _Cast_ConnectedSockets(self)
