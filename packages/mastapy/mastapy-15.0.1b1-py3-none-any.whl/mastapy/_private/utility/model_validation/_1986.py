"""Fix"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_FIX = python_net_import("SMT.MastaAPI.Utility.ModelValidation", "Fix")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Fix")
    CastSelf = TypeVar("CastSelf", bound="Fix._Cast_Fix")


__docformat__ = "restructuredtext en"
__all__ = ("Fix",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Fix:
    """Special nested class for casting Fix to subclasses."""

    __parent__: "Fix"

    @property
    def fix(self: "CastSelf") -> "Fix":
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
class Fix(_0.APIBase):
    """Fix

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FIX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def fix_by(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "FixBy")

        if temp is None:
            return ""

        return temp

    @fix_by.setter
    @exception_bridge
    @enforce_parameter_types
    def fix_by(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "FixBy", str(value) if value is not None else ""
        )

    @exception_bridge
    def perform(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Perform")

    @property
    def cast_to(self: "Self") -> "_Cast_Fix":
        """Cast to another type.

        Returns:
            _Cast_Fix
        """
        return _Cast_Fix(self)
