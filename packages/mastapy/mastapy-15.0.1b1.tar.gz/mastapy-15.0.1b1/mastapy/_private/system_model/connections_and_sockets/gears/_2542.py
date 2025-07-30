"""KlingelnbergHypoidGearTeethSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2538

_KLINGELNBERG_HYPOID_GEAR_TEETH_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergHypoidGearTeethSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2517
    from mastapy._private.system_model.connections_and_sockets.gears import _2529, _2535

    Self = TypeVar("Self", bound="KlingelnbergHypoidGearTeethSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergHypoidGearTeethSocket._Cast_KlingelnbergHypoidGearTeethSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergHypoidGearTeethSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergHypoidGearTeethSocket:
    """Special nested class for casting KlingelnbergHypoidGearTeethSocket to subclasses."""

    __parent__: "KlingelnbergHypoidGearTeethSocket"

    @property
    def klingelnberg_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2538.KlingelnbergConicalGearTeethSocket":
        return self.__parent__._cast(_2538.KlingelnbergConicalGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2529.ConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2529

        return self.__parent__._cast(_2529.ConicalGearTeethSocket)

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2535.GearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2535

        return self.__parent__._cast(_2535.GearTeethSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def klingelnberg_hypoid_gear_teeth_socket(
        self: "CastSelf",
    ) -> "KlingelnbergHypoidGearTeethSocket":
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
class KlingelnbergHypoidGearTeethSocket(_2538.KlingelnbergConicalGearTeethSocket):
    """KlingelnbergHypoidGearTeethSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_HYPOID_GEAR_TEETH_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergHypoidGearTeethSocket":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergHypoidGearTeethSocket
        """
        return _Cast_KlingelnbergHypoidGearTeethSocket(self)
