"""FileHistoryItem"""

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

_FILE_HISTORY_ITEM = python_net_import("SMT.MastaAPI.Utility", "FileHistoryItem")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FileHistoryItem")
    CastSelf = TypeVar("CastSelf", bound="FileHistoryItem._Cast_FileHistoryItem")


__docformat__ = "restructuredtext en"
__all__ = ("FileHistoryItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FileHistoryItem:
    """Special nested class for casting FileHistoryItem to subclasses."""

    __parent__: "FileHistoryItem"

    @property
    def file_history_item(self: "CastSelf") -> "FileHistoryItem":
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
class FileHistoryItem(_0.APIBase):
    """FileHistoryItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FILE_HISTORY_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def comment(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def hash_code(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HashCode")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def licence_id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LicenceID")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def save_date(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SaveDate")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def save_date_and_age(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SaveDateAndAge")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def user_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserName")

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
    def cast_to(self: "Self") -> "_Cast_FileHistoryItem":
        """Cast to another type.

        Returns:
            _Cast_FileHistoryItem
        """
        return _Cast_FileHistoryItem(self)
