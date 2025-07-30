"""CycloidalDiscOuterSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2497

_CYCLOIDAL_DISC_OUTER_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscOuterSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2517

    Self = TypeVar("Self", bound="CycloidalDiscOuterSocket")
    CastSelf = TypeVar(
        "CastSelf", bound="CycloidalDiscOuterSocket._Cast_CycloidalDiscOuterSocket"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscOuterSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscOuterSocket:
    """Special nested class for casting CycloidalDiscOuterSocket to subclasses."""

    __parent__: "CycloidalDiscOuterSocket"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2497.CylindricalSocket":
        return self.__parent__._cast(_2497.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def cycloidal_disc_outer_socket(self: "CastSelf") -> "CycloidalDiscOuterSocket":
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
class CycloidalDiscOuterSocket(_2497.CylindricalSocket):
    """CycloidalDiscOuterSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_OUTER_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscOuterSocket":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscOuterSocket
        """
        return _Cast_CycloidalDiscOuterSocket(self)
