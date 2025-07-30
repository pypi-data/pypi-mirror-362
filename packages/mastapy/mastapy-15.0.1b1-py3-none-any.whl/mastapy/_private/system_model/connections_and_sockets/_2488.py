"""BearingOuterSocket"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2504

_BEARING_OUTER_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "BearingOuterSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2497,
        _2505,
        _2517,
    )

    Self = TypeVar("Self", bound="BearingOuterSocket")
    CastSelf = TypeVar("CastSelf", bound="BearingOuterSocket._Cast_BearingOuterSocket")


__docformat__ = "restructuredtext en"
__all__ = ("BearingOuterSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingOuterSocket:
    """Special nested class for casting BearingOuterSocket to subclasses."""

    __parent__: "BearingOuterSocket"

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "_2504.MountableComponentOuterSocket":
        return self.__parent__._cast(_2504.MountableComponentOuterSocket)

    @property
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2505.MountableComponentSocket":
        from mastapy._private.system_model.connections_and_sockets import _2505

        return self.__parent__._cast(_2505.MountableComponentSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2497.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2497

        return self.__parent__._cast(_2497.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "BearingOuterSocket":
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
class BearingOuterSocket(_2504.MountableComponentOuterSocket):
    """BearingOuterSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_OUTER_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BearingOuterSocket":
        """Cast to another type.

        Returns:
            _Cast_BearingOuterSocket
        """
        return _Cast_BearingOuterSocket(self)
