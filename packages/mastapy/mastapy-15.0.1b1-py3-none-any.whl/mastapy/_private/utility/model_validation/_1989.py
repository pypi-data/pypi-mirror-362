"""StatusItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)

_STATUS_ITEM = python_net_import("SMT.MastaAPI.Utility.ModelValidation", "StatusItem")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.model_validation import _1986

    Self = TypeVar("Self", bound="StatusItem")
    CastSelf = TypeVar("CastSelf", bound="StatusItem._Cast_StatusItem")


__docformat__ = "restructuredtext en"
__all__ = ("StatusItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StatusItem:
    """Special nested class for casting StatusItem to subclasses."""

    __parent__: "StatusItem"

    @property
    def status_item(self: "CastSelf") -> "StatusItem":
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
class StatusItem(_0.APIBase):
    """StatusItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATUS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def can_fix(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CanFix")

        if temp is None:
            return False

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
    def fixes(self: "Self") -> "List[_1986.Fix]":
        """List[mastapy.utility.model_validation.Fix]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Fixes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def apply_first_fix(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ApplyFirstFix")

    @property
    def cast_to(self: "Self") -> "_Cast_StatusItem":
        """Cast to another type.

        Returns:
            _Cast_StatusItem
        """
        return _Cast_StatusItem(self)
