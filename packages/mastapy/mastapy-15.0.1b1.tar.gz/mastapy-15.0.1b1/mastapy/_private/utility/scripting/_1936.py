"""UserSpecifiedData"""

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
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_USER_SPECIFIED_DATA = python_net_import(
    "SMT.MastaAPI.Utility.Scripting", "UserSpecifiedData"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="UserSpecifiedData")
    CastSelf = TypeVar("CastSelf", bound="UserSpecifiedData._Cast_UserSpecifiedData")


__docformat__ = "restructuredtext en"
__all__ = ("UserSpecifiedData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UserSpecifiedData:
    """Special nested class for casting UserSpecifiedData to subclasses."""

    __parent__: "UserSpecifiedData"

    @property
    def user_specified_data(self: "CastSelf") -> "UserSpecifiedData":
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
class UserSpecifiedData(_0.APIBase):
    """UserSpecifiedData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _USER_SPECIFIED_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def clear(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Clear")

    @exception_bridge
    @enforce_parameter_types
    def get_bool(self: "Self", key: "str") -> "bool":
        """bool

        Args:
            key (str)
        """
        key = str(key)
        method_result = pythonnet_method_call(
            self.wrapped, "GetBool", key if key else ""
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def get_double(self: "Self", key: "str") -> "float":
        """float

        Args:
            key (str)
        """
        key = str(key)
        method_result = pythonnet_method_call(
            self.wrapped, "GetDouble", key if key else ""
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def get_string(self: "Self", key: "str") -> "str":
        """str

        Args:
            key (str)
        """
        key = str(key)
        method_result = pythonnet_method_call(
            self.wrapped, "GetString", key if key else ""
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def has_bool(self: "Self", key: "str") -> "bool":
        """bool

        Args:
            key (str)
        """
        key = str(key)
        method_result = pythonnet_method_call(
            self.wrapped, "HasBool", key if key else ""
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def has_double(self: "Self", key: "str") -> "bool":
        """bool

        Args:
            key (str)
        """
        key = str(key)
        method_result = pythonnet_method_call(
            self.wrapped, "HasDouble", key if key else ""
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def has_string(self: "Self", key: "str") -> "bool":
        """bool

        Args:
            key (str)
        """
        key = str(key)
        method_result = pythonnet_method_call(
            self.wrapped, "HasString", key if key else ""
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def set_bool(self: "Self", key: "str", value: "bool") -> None:
        """Method does not return.

        Args:
            key (str)
            value (bool)
        """
        key = str(key)
        value = bool(value)
        pythonnet_method_call(
            self.wrapped, "SetBool", key if key else "", value if value else False
        )

    @exception_bridge
    @enforce_parameter_types
    def set_double(self: "Self", key: "str", value: "float") -> None:
        """Method does not return.

        Args:
            key (str)
            value (float)
        """
        key = str(key)
        value = float(value)
        pythonnet_method_call(
            self.wrapped, "SetDouble", key if key else "", value if value else 0.0
        )

    @exception_bridge
    @enforce_parameter_types
    def set_string(self: "Self", key: "str", value: "str") -> None:
        """Method does not return.

        Args:
            key (str)
            value (str)
        """
        key = str(key)
        value = str(value)
        pythonnet_method_call(
            self.wrapped, "SetString", key if key else "", value if value else ""
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
    def cast_to(self: "Self") -> "_Cast_UserSpecifiedData":
        """Cast to another type.

        Returns:
            _Cast_UserSpecifiedData
        """
        return _Cast_UserSpecifiedData(self)
