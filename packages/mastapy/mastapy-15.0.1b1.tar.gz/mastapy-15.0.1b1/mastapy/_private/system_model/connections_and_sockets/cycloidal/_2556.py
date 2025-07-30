"""CycloidalDiscCentralBearingConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2490

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscCentralBearingConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import (
        _2486,
        _2493,
        _2516,
    )

    Self = TypeVar("Self", bound="CycloidalDiscCentralBearingConnection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnection._Cast_CycloidalDiscCentralBearingConnection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscCentralBearingConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnection:
    """Special nested class for casting CycloidalDiscCentralBearingConnection to subclasses."""

    __parent__: "CycloidalDiscCentralBearingConnection"

    @property
    def coaxial_connection(self: "CastSelf") -> "_2490.CoaxialConnection":
        return self.__parent__._cast(_2490.CoaxialConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2516.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2516

        return self.__parent__._cast(_2516.ShaftToMountableComponentConnection)

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2486.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2486

        return self.__parent__._cast(_2486.AbstractShaftToMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2493.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2493

        return self.__parent__._cast(_2493.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnection":
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
class CycloidalDiscCentralBearingConnection(_2490.CoaxialConnection):
    """CycloidalDiscCentralBearingConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscCentralBearingConnection":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnection
        """
        return _Cast_CycloidalDiscCentralBearingConnection(self)
