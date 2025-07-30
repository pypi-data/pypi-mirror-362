"""MKLVersion"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MKL_VERSION = python_net_import("SMT.MastaAPI.Utility", "MKLVersion")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MKLVersion")
    CastSelf = TypeVar("CastSelf", bound="MKLVersion._Cast_MKLVersion")


__docformat__ = "restructuredtext en"
__all__ = ("MKLVersion",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MKLVersion:
    """Special nested class for casting MKLVersion to subclasses."""

    __parent__: "MKLVersion"

    @property
    def mkl_version(self: "CastSelf") -> "MKLVersion":
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
class MKLVersion(_0.APIBase):
    """MKLVersion

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MKL_VERSION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def build(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Build")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def instruction_set(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InstructionSet")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def platform(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Platform")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def processor(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Processor")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def product_status(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProductStatus")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def version(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Version")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_MKLVersion":
        """Cast to another type.

        Returns:
            _Cast_MKLVersion
        """
        return _Cast_MKLVersion(self)
