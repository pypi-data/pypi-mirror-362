"""AGMAGleasonConicalGearTeethSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2529

_AGMA_GLEASON_CONICAL_GEAR_TEETH_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "AGMAGleasonConicalGearTeethSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2517
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2523,
        _2525,
        _2535,
        _2537,
        _2545,
        _2547,
        _2549,
        _2553,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearTeethSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearTeethSocket._Cast_AGMAGleasonConicalGearTeethSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearTeethSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearTeethSocket:
    """Special nested class for casting AGMAGleasonConicalGearTeethSocket to subclasses."""

    __parent__: "AGMAGleasonConicalGearTeethSocket"

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2529.ConicalGearTeethSocket":
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
    def bevel_differential_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2523.BevelDifferentialGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2523

        return self.__parent__._cast(_2523.BevelDifferentialGearTeethSocket)

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2525.BevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2525

        return self.__parent__._cast(_2525.BevelGearTeethSocket)

    @property
    def hypoid_gear_teeth_socket(self: "CastSelf") -> "_2537.HypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2537

        return self.__parent__._cast(_2537.HypoidGearTeethSocket)

    @property
    def spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2545.SpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2545

        return self.__parent__._cast(_2545.SpiralBevelGearTeethSocket)

    @property
    def straight_bevel_diff_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2547.StraightBevelDiffGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2547

        return self.__parent__._cast(_2547.StraightBevelDiffGearTeethSocket)

    @property
    def straight_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2549.StraightBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2549

        return self.__parent__._cast(_2549.StraightBevelGearTeethSocket)

    @property
    def zerol_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2553.ZerolBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2553

        return self.__parent__._cast(_2553.ZerolBevelGearTeethSocket)

    @property
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearTeethSocket":
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
class AGMAGleasonConicalGearTeethSocket(_2529.ConicalGearTeethSocket):
    """AGMAGleasonConicalGearTeethSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_TEETH_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearTeethSocket":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearTeethSocket
        """
        return _Cast_AGMAGleasonConicalGearTeethSocket(self)
