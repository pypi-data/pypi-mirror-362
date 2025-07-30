"""SpiralBevelGearTeethSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2525

_SPIRAL_BEVEL_GEAR_TEETH_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "SpiralBevelGearTeethSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2517
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2521,
        _2529,
        _2535,
    )

    Self = TypeVar("Self", bound="SpiralBevelGearTeethSocket")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelGearTeethSocket._Cast_SpiralBevelGearTeethSocket"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearTeethSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearTeethSocket:
    """Special nested class for casting SpiralBevelGearTeethSocket to subclasses."""

    __parent__: "SpiralBevelGearTeethSocket"

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2525.BevelGearTeethSocket":
        return self.__parent__._cast(_2525.BevelGearTeethSocket)

    @property
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2521.AGMAGleasonConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2521

        return self.__parent__._cast(_2521.AGMAGleasonConicalGearTeethSocket)

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
    def spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "SpiralBevelGearTeethSocket":
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
class SpiralBevelGearTeethSocket(_2525.BevelGearTeethSocket):
    """SpiralBevelGearTeethSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_TEETH_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearTeethSocket":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearTeethSocket
        """
        return _Cast_SpiralBevelGearTeethSocket(self)
