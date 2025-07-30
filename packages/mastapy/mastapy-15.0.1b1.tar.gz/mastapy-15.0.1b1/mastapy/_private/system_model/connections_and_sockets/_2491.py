"""ComponentConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.connections_and_sockets import _2492

_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "ComponentConnection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2496
    from mastapy._private.system_model.part_model import _2670

    Self = TypeVar("Self", bound="ComponentConnection")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentConnection._Cast_ComponentConnection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentConnection:
    """Special nested class for casting ComponentConnection to subclasses."""

    __parent__: "ComponentConnection"

    @property
    def component_measurer(self: "CastSelf") -> "_2492.ComponentMeasurer":
        return self.__parent__._cast(_2492.ComponentMeasurer)

    @property
    def cylindrical_component_connection(
        self: "CastSelf",
    ) -> "_2496.CylindricalComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2496

        return self.__parent__._cast(_2496.CylindricalComponentConnection)

    @property
    def component_connection(self: "CastSelf") -> "ComponentConnection":
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
class ComponentConnection(_2492.ComponentMeasurer):
    """ComponentConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connected_components_socket(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponentsSocket")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def detail_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DetailView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def socket(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Socket")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def connected_component(self: "Self") -> "_2670.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @exception_bridge
    def swap(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Swap")

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentConnection":
        """Cast to another type.

        Returns:
            _Cast_ComponentConnection
        """
        return _Cast_ComponentConnection(self)
