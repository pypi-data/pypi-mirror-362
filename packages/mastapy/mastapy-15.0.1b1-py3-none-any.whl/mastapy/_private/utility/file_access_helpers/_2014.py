"""ColumnTitle"""

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

_COLUMN_TITLE = python_net_import(
    "SMT.MastaAPI.Utility.FileAccessHelpers", "ColumnTitle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ColumnTitle")
    CastSelf = TypeVar("CastSelf", bound="ColumnTitle._Cast_ColumnTitle")


__docformat__ = "restructuredtext en"
__all__ = ("ColumnTitle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ColumnTitle:
    """Special nested class for casting ColumnTitle to subclasses."""

    __parent__: "ColumnTitle"

    @property
    def column_title(self: "CastSelf") -> "ColumnTitle":
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
class ColumnTitle(_0.APIBase):
    """ColumnTitle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COLUMN_TITLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def column_number(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ColumnNumber")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def title(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Title")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ColumnTitle":
        """Cast to another type.

        Returns:
            _Cast_ColumnTitle
        """
        return _Cast_ColumnTitle(self)
