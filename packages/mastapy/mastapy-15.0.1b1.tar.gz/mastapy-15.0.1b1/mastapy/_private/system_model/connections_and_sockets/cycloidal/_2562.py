"""RingPinsToDiscConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets import _2502

_RING_PINS_TO_DISC_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "RingPinsToDiscConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2493

    Self = TypeVar("Self", bound="RingPinsToDiscConnection")
    CastSelf = TypeVar(
        "CastSelf", bound="RingPinsToDiscConnection._Cast_RingPinsToDiscConnection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RingPinsToDiscConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPinsToDiscConnection:
    """Special nested class for casting RingPinsToDiscConnection to subclasses."""

    __parent__: "RingPinsToDiscConnection"

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2502.InterMountableComponentConnection":
        return self.__parent__._cast(_2502.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2493.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2493

        return self.__parent__._cast(_2493.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def ring_pins_to_disc_connection(self: "CastSelf") -> "RingPinsToDiscConnection":
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
class RingPinsToDiscConnection(_2502.InterMountableComponentConnection):
    """RingPinsToDiscConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_PINS_TO_DISC_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactStiffness")

        if temp is None:
            return 0.0

        return temp

    @contact_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ContactStiffness", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RingPinsToDiscConnection":
        """Cast to another type.

        Returns:
            _Cast_RingPinsToDiscConnection
        """
        return _Cast_RingPinsToDiscConnection(self)
