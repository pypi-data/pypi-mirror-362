"""LicenceServerDetails"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_LICENCE_SERVER_DETAILS = python_net_import(
    "SMT.MastaAPIUtility.Licensing", "LicenceServerDetails"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LicenceServerDetails")
    CastSelf = TypeVar(
        "CastSelf", bound="LicenceServerDetails._Cast_LicenceServerDetails"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LicenceServerDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LicenceServerDetails:
    """Special nested class for casting LicenceServerDetails to subclasses."""

    __parent__: "LicenceServerDetails"

    @property
    def licence_server_details(self: "CastSelf") -> "LicenceServerDetails":
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
class LicenceServerDetails:
    """LicenceServerDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LICENCE_SERVER_DETAILS

    wrapped: "Any" = None

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if self.wrapped is None:
            object.__setattr__(self, "wrapped", LicenceServerDetails.TYPE())

        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ip(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Ip")

        if temp is None:
            return ""

        return temp

    @ip.setter
    @exception_bridge
    @enforce_parameter_types
    def ip(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Ip", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def port(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Port")

        if temp is None:
            return 0

        return temp

    @port.setter
    @exception_bridge
    @enforce_parameter_types
    def port(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Port", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def web_port(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "WebPort")

        if temp is None:
            return 0

        return temp

    @web_port.setter
    @exception_bridge
    @enforce_parameter_types
    def web_port(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "WebPort", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def licence_groups_ip(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "LicenceGroupsIp")

        if temp is None:
            return ""

        return temp

    @licence_groups_ip.setter
    @exception_bridge
    @enforce_parameter_types
    def licence_groups_ip(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "LicenceGroupsIp", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def licence_groups_port(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "LicenceGroupsPort")

        if temp is None:
            return 0

        return temp

    @licence_groups_port.setter
    @exception_bridge
    @enforce_parameter_types
    def licence_groups_port(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "LicenceGroupsPort", int(value) if value is not None else 0
        )

    @exception_bridge
    def has_ip(self: "Self") -> "bool":
        """bool"""
        method_result = pythonnet_method_call(self.wrapped, "HasIp")
        return method_result

    @exception_bridge
    def has_port(self: "Self") -> "bool":
        """bool"""
        method_result = pythonnet_method_call(self.wrapped, "HasPort")
        return method_result

    @exception_bridge
    def has_web_port(self: "Self") -> "bool":
        """bool"""
        method_result = pythonnet_method_call(self.wrapped, "HasWebPort")
        return method_result

    @exception_bridge
    def has_licence_groups_ip(self: "Self") -> "bool":
        """bool"""
        method_result = pythonnet_method_call(self.wrapped, "HasLicenceGroupsIp")
        return method_result

    @exception_bridge
    def has_licence_groups_port(self: "Self") -> "bool":
        """bool"""
        method_result = pythonnet_method_call(self.wrapped, "HasLicenceGroupsPort")
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_LicenceServerDetails":
        """Cast to another type.

        Returns:
            _Cast_LicenceServerDetails
        """
        return _Cast_LicenceServerDetails(self)
