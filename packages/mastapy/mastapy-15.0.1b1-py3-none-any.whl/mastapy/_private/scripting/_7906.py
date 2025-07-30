"""ApiVersion"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_API_VERSION = python_net_import("SMT.MastaAPIUtility.Scripting", "ApiVersion")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ApiVersion")
    CastSelf = TypeVar("CastSelf", bound="ApiVersion._Cast_ApiVersion")


__docformat__ = "restructuredtext en"
__all__ = ("ApiVersion",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ApiVersion:
    """Special nested class for casting ApiVersion to subclasses."""

    __parent__: "ApiVersion"

    @property
    def api_version(self: "CastSelf") -> "ApiVersion":
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
class ApiVersion:
    """ApiVersion

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _API_VERSION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def file_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FileName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def assembly_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def assembly_name_without_version(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyNameWithoutVersion")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def file_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilePath")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def customer_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CustomerName")

        if temp is None:
            return ""

        return temp

    @exception_bridge
    @enforce_parameter_types
    def compare_to(self: "Self", other: "ApiVersion") -> "int":
        """int

        Args:
            other (mastapy.scripting.ApiVersion)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "CompareTo", other.wrapped if other else None
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ApiVersion":
        """Cast to another type.

        Returns:
            _Cast_ApiVersion
        """
        return _Cast_ApiVersion(self)
