"""StatusItemWrapper"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_STATUS_ITEM_WRAPPER = python_net_import(
    "SMT.MastaAPI.Utility.ModelValidation", "StatusItemWrapper"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.model_validation import _1989

    Self = TypeVar("Self", bound="StatusItemWrapper")
    CastSelf = TypeVar("CastSelf", bound="StatusItemWrapper._Cast_StatusItemWrapper")


__docformat__ = "restructuredtext en"
__all__ = ("StatusItemWrapper",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StatusItemWrapper:
    """Special nested class for casting StatusItemWrapper to subclasses."""

    __parent__: "StatusItemWrapper"

    @property
    def status_item_wrapper(self: "CastSelf") -> "StatusItemWrapper":
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
class StatusItemWrapper(_0.APIBase):
    """StatusItemWrapper

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATUS_ITEM_WRAPPER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def category(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Category")

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
    def id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def status_item(self: "Self") -> "_1989.StatusItem":
        """mastapy.utility.model_validation.StatusItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatusItem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StatusItemWrapper":
        """Cast to another type.

        Returns:
            _Cast_StatusItemWrapper
        """
        return _Cast_StatusItemWrapper(self)
