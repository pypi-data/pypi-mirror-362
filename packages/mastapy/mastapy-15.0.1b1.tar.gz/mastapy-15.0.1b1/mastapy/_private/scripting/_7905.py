"""ApiEnumForAttribute"""

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

_API_ENUM_FOR_ATTRIBUTE = python_net_import(
    "SMT.MastaAPIUtility.Scripting", "ApiEnumForAttribute"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ApiEnumForAttribute")
    CastSelf = TypeVar(
        "CastSelf", bound="ApiEnumForAttribute._Cast_ApiEnumForAttribute"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ApiEnumForAttribute",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ApiEnumForAttribute:
    """Special nested class for casting ApiEnumForAttribute to subclasses."""

    __parent__: "ApiEnumForAttribute"

    @property
    def api_enum_for_attribute(self: "CastSelf") -> "ApiEnumForAttribute":
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
class ApiEnumForAttribute:
    """ApiEnumForAttribute

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _API_ENUM_FOR_ATTRIBUTE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def wrapped_enum(self: "Self") -> "type":
        """type

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WrappedEnum")

        if temp is None:
            return None

        return temp

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def get_wrapped_enum_from(api_enum_type: "type") -> "type":
        """type

        Args:
            api_enum_type (type)
        """
        method_result = pythonnet_method_call(
            ApiEnumForAttribute.TYPE, "GetWrappedEnumFrom", api_enum_type
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ApiEnumForAttribute":
        """Cast to another type.

        Returns:
            _Cast_ApiEnumForAttribute
        """
        return _Cast_ApiEnumForAttribute(self)
