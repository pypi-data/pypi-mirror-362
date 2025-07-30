"""InnerShaftSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2501

_INNER_SHAFT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "InnerShaftSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2497,
        _2515,
        _2517,
    )

    Self = TypeVar("Self", bound="InnerShaftSocket")
    CastSelf = TypeVar("CastSelf", bound="InnerShaftSocket._Cast_InnerShaftSocket")


__docformat__ = "restructuredtext en"
__all__ = ("InnerShaftSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InnerShaftSocket:
    """Special nested class for casting InnerShaftSocket to subclasses."""

    __parent__: "InnerShaftSocket"

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2501.InnerShaftSocketBase":
        return self.__parent__._cast(_2501.InnerShaftSocketBase)

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
    def inner_shaft_socket(self: "CastSelf") -> "InnerShaftSocket":
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
class InnerShaftSocket(_2501.InnerShaftSocketBase):
    """InnerShaftSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INNER_SHAFT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_InnerShaftSocket":
        """Cast to another type.

        Returns:
            _Cast_InnerShaftSocket
        """
        return _Cast_InnerShaftSocket(self)
