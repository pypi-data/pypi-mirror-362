"""CVTPulleySocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2511

_CVT_PULLEY_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CVTPulleySocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2497, _2517

    Self = TypeVar("Self", bound="CVTPulleySocket")
    CastSelf = TypeVar("CastSelf", bound="CVTPulleySocket._Cast_CVTPulleySocket")


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleySocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTPulleySocket:
    """Special nested class for casting CVTPulleySocket to subclasses."""

    __parent__: "CVTPulleySocket"

    @property
    def pulley_socket(self: "CastSelf") -> "_2511.PulleySocket":
        return self.__parent__._cast(_2511.PulleySocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2497.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2497

        return self.__parent__._cast(_2497.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "CVTPulleySocket":
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
class CVTPulleySocket(_2511.PulleySocket):
    """CVTPulleySocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_PULLEY_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CVTPulleySocket":
        """Cast to another type.

        Returns:
            _Cast_CVTPulleySocket
        """
        return _Cast_CVTPulleySocket(self)
