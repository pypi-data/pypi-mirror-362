"""ElectricMachineStatorSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2517

_ELECTRIC_MACHINE_STATOR_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "ElectricMachineStatorSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElectricMachineStatorSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineStatorSocket._Cast_ElectricMachineStatorSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineStatorSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineStatorSocket:
    """Special nested class for casting ElectricMachineStatorSocket to subclasses."""

    __parent__: "ElectricMachineStatorSocket"

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        return self.__parent__._cast(_2517.Socket)

    @property
    def electric_machine_stator_socket(
        self: "CastSelf",
    ) -> "ElectricMachineStatorSocket":
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
class ElectricMachineStatorSocket(_2517.Socket):
    """ElectricMachineStatorSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_STATOR_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineStatorSocket":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineStatorSocket
        """
        return _Cast_ElectricMachineStatorSocket(self)
