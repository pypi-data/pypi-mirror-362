"""FaceGearTeethSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2535

_FACE_GEAR_TEETH_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "FaceGearTeethSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2517

    Self = TypeVar("Self", bound="FaceGearTeethSocket")
    CastSelf = TypeVar(
        "CastSelf", bound="FaceGearTeethSocket._Cast_FaceGearTeethSocket"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearTeethSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearTeethSocket:
    """Special nested class for casting FaceGearTeethSocket to subclasses."""

    __parent__: "FaceGearTeethSocket"

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2535.GearTeethSocket":
        return self.__parent__._cast(_2535.GearTeethSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def face_gear_teeth_socket(self: "CastSelf") -> "FaceGearTeethSocket":
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
class FaceGearTeethSocket(_2535.GearTeethSocket):
    """FaceGearTeethSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_TEETH_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearTeethSocket":
        """Cast to another type.

        Returns:
            _Cast_FaceGearTeethSocket
        """
        return _Cast_FaceGearTeethSocket(self)
