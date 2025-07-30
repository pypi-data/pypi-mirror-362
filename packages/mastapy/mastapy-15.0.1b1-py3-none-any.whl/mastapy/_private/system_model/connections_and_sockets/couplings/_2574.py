"""TorqueConverterPumpSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.couplings import _2568

_TORQUE_CONVERTER_PUMP_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "TorqueConverterPumpSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2497, _2517

    Self = TypeVar("Self", bound="TorqueConverterPumpSocket")
    CastSelf = TypeVar(
        "CastSelf", bound="TorqueConverterPumpSocket._Cast_TorqueConverterPumpSocket"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterPumpSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterPumpSocket:
    """Special nested class for casting TorqueConverterPumpSocket to subclasses."""

    __parent__: "TorqueConverterPumpSocket"

    @property
    def coupling_socket(self: "CastSelf") -> "_2568.CouplingSocket":
        return self.__parent__._cast(_2568.CouplingSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2497.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2497

        return self.__parent__._cast(_2497.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def torque_converter_pump_socket(self: "CastSelf") -> "TorqueConverterPumpSocket":
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
class TorqueConverterPumpSocket(_2568.CouplingSocket):
    """TorqueConverterPumpSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_PUMP_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TorqueConverterPumpSocket":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterPumpSocket
        """
        return _Cast_TorqueConverterPumpSocket(self)
