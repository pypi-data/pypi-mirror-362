"""IncludeDutyCycleOption"""

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

_INCLUDE_DUTY_CYCLE_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel", "IncludeDutyCycleOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="IncludeDutyCycleOption")
    CastSelf = TypeVar(
        "CastSelf", bound="IncludeDutyCycleOption._Cast_IncludeDutyCycleOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("IncludeDutyCycleOption",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IncludeDutyCycleOption:
    """Special nested class for casting IncludeDutyCycleOption to subclasses."""

    __parent__: "IncludeDutyCycleOption"

    @property
    def include_duty_cycle_option(self: "CastSelf") -> "IncludeDutyCycleOption":
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
class IncludeDutyCycleOption(_0.APIBase):
    """IncludeDutyCycleOption

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INCLUDE_DUTY_CYCLE_OPTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def import_(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Import")

        if temp is None:
            return False

        return temp

    @import_.setter
    @exception_bridge
    @enforce_parameter_types
    def import_(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Import", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_IncludeDutyCycleOption":
        """Cast to another type.

        Returns:
            _Cast_IncludeDutyCycleOption
        """
        return _Cast_IncludeDutyCycleOption(self)
