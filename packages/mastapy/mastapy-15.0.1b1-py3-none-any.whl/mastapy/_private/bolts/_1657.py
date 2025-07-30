"""BoltSection"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_BOLT_SECTION = python_net_import("SMT.MastaAPI.Bolts", "BoltSection")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BoltSection")
    CastSelf = TypeVar("CastSelf", bound="BoltSection._Cast_BoltSection")


__docformat__ = "restructuredtext en"
__all__ = ("BoltSection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BoltSection:
    """Special nested class for casting BoltSection to subclasses."""

    __parent__: "BoltSection"

    @property
    def bolt_section(self: "CastSelf") -> "BoltSection":
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
class BoltSection(_0.APIBase):
    """BoltSection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BOLT_SECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return temp

    @diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Diameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def inner_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @inner_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InnerDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BoltSection":
        """Cast to another type.

        Returns:
            _Cast_BoltSection
        """
        return _Cast_BoltSection(self)
