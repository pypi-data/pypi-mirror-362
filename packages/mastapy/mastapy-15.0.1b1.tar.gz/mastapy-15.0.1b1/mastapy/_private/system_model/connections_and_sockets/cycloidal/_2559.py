"""CycloidalDiscPlanetaryBearingConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2486

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscPlanetaryBearingConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2493

    Self = TypeVar("Self", bound="CycloidalDiscPlanetaryBearingConnection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscPlanetaryBearingConnection._Cast_CycloidalDiscPlanetaryBearingConnection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscPlanetaryBearingConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscPlanetaryBearingConnection:
    """Special nested class for casting CycloidalDiscPlanetaryBearingConnection to subclasses."""

    __parent__: "CycloidalDiscPlanetaryBearingConnection"

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2486.AbstractShaftToMountableComponentConnection":
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
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "CycloidalDiscPlanetaryBearingConnection":
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
class CycloidalDiscPlanetaryBearingConnection(
    _2486.AbstractShaftToMountableComponentConnection
):
    """CycloidalDiscPlanetaryBearingConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscPlanetaryBearingConnection":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscPlanetaryBearingConnection
        """
        return _Cast_CycloidalDiscPlanetaryBearingConnection(self)
