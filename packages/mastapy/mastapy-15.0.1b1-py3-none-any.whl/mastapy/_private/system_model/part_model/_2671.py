"""ComponentsConnectedResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_COMPONENTS_CONNECTED_RESULT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "ComponentsConnectedResult"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model import _2672

    Self = TypeVar("Self", bound="ComponentsConnectedResult")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentsConnectedResult._Cast_ComponentsConnectedResult"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentsConnectedResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentsConnectedResult:
    """Special nested class for casting ComponentsConnectedResult to subclasses."""

    __parent__: "ComponentsConnectedResult"

    @property
    def components_connected_result(self: "CastSelf") -> "ComponentsConnectedResult":
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
class ComponentsConnectedResult(_0.APIBase):
    """ComponentsConnectedResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENTS_CONNECTED_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_failed(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionFailed")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def failure_message(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FailureMessage")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def was_connection_created(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WasConnectionCreated")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def created_socket_connection(self: "Self") -> "_2672.ConnectedSockets":
        """mastapy.system_model.part_model.ConnectedSockets

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CreatedSocketConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentsConnectedResult":
        """Cast to another type.

        Returns:
            _Cast_ComponentsConnectedResult
        """
        return _Cast_ComponentsConnectedResult(self)
