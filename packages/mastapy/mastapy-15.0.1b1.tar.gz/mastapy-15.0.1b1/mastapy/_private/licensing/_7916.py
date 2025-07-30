"""ModuleDetails"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MODULE_DETAILS = python_net_import("SMT.MastaAPIUtility.Licensing", "ModuleDetails")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ModuleDetails")
    CastSelf = TypeVar("CastSelf", bound="ModuleDetails._Cast_ModuleDetails")


__docformat__ = "restructuredtext en"
__all__ = ("ModuleDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModuleDetails:
    """Special nested class for casting ModuleDetails to subclasses."""

    __parent__: "ModuleDetails"

    @property
    def module_details(self: "CastSelf") -> "ModuleDetails":
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
class ModuleDetails:
    """ModuleDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODULE_DETAILS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def is_licensed(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLicensed")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def expiry_date(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExpiryDate")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def user_count(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserCount")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def maximum_users(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumUsers")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def code(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Code")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def description(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Description")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def scope(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Scope")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ModuleDetails":
        """Cast to another type.

        Returns:
            _Cast_ModuleDetails
        """
        return _Cast_ModuleDetails(self)
