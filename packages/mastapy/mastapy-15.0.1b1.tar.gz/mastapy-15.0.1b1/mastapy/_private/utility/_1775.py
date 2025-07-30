"""FileHistory"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FILE_HISTORY = python_net_import("SMT.MastaAPI.Utility", "FileHistory")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.utility import _1776

    Self = TypeVar("Self", bound="FileHistory")
    CastSelf = TypeVar("CastSelf", bound="FileHistory._Cast_FileHistory")


__docformat__ = "restructuredtext en"
__all__ = ("FileHistory",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FileHistory:
    """Special nested class for casting FileHistory to subclasses."""

    __parent__: "FileHistory"

    @property
    def file_history(self: "CastSelf") -> "FileHistory":
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
class FileHistory(_0.APIBase):
    """FileHistory

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FILE_HISTORY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_history_items(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfHistoryItems")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def items(self: "Self") -> "List[_1776.FileHistoryItem]":
        """List[mastapy.utility.FileHistoryItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Items")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    def clear_history(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearHistory")

    @exception_bridge
    @enforce_parameter_types
    def add_file_history_item(self: "Self", item: "_1776.FileHistoryItem") -> None:
        """Method does not return.

        Args:
            item (mastapy.utility.FileHistoryItem)
        """
        pythonnet_method_call(
            self.wrapped, "AddFileHistoryItem", item.wrapped if item else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_history_item(self: "Self", user_name: "str", comment: "str") -> None:
        """Method does not return.

        Args:
            user_name (str)
            comment (str)
        """
        user_name = str(user_name)
        comment = str(comment)
        pythonnet_method_call(
            self.wrapped,
            "AddHistoryItem",
            user_name if user_name else "",
            comment if comment else "",
        )

    @exception_bridge
    @enforce_parameter_types
    def create_history_item(
        self: "Self", user_name: "str", comment: "str"
    ) -> "_1776.FileHistoryItem":
        """mastapy.utility.FileHistoryItem

        Args:
            user_name (str)
            comment (str)
        """
        user_name = str(user_name)
        comment = str(comment)
        method_result = pythonnet_method_call(
            self.wrapped,
            "CreateHistoryItem",
            user_name if user_name else "",
            comment if comment else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_FileHistory":
        """Cast to another type.

        Returns:
            _Cast_FileHistory
        """
        return _Cast_FileHistory(self)
