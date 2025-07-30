"""SystemDirectoryPopulator"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1792

_SYSTEM_DIRECTORY_POPULATOR = python_net_import(
    "SMT.MastaAPI.Utility", "SystemDirectoryPopulator"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="SystemDirectoryPopulator")
    CastSelf = TypeVar(
        "CastSelf", bound="SystemDirectoryPopulator._Cast_SystemDirectoryPopulator"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SystemDirectoryPopulator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SystemDirectoryPopulator:
    """Special nested class for casting SystemDirectoryPopulator to subclasses."""

    __parent__: "SystemDirectoryPopulator"

    @property
    def system_directory_populator(self: "CastSelf") -> "SystemDirectoryPopulator":
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
class SystemDirectoryPopulator(_0.APIBase):
    """SystemDirectoryPopulator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYSTEM_DIRECTORY_POPULATOR

    class SetupFrom(Enum):
        """SetupFrom is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _SYSTEM_DIRECTORY_POPULATOR.SetupFrom

        DONT_COPY = 0
        LATEST_VERSION = 1
        SPECIFIED_VERSION = 2

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    SetupFrom.__setattr__ = __enum_setattr
    SetupFrom.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def copy_from(self: "Self") -> "SystemDirectoryPopulator.SetupFrom":
        """mastapy.utility.SystemDirectoryPopulator.SetupFrom"""
        temp = pythonnet_property_get(self.wrapped, "CopyFrom")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.SystemDirectoryPopulator+SetupFrom"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.SystemDirectoryPopulator.SystemDirectoryPopulator",
            "SetupFrom",
        )(value)

    @copy_from.setter
    @exception_bridge
    @enforce_parameter_types
    def copy_from(self: "Self", value: "SystemDirectoryPopulator.SetupFrom") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.SystemDirectoryPopulator+SetupFrom"
        )
        pythonnet_property_set(self.wrapped, "CopyFrom", value)

    @property
    @exception_bridge
    def selected_version(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_SystemDirectory":
        """ListWithSelectedItem[mastapy.utility.SystemDirectory]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedVersion")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_SystemDirectory",
        )(temp)

    @selected_version.setter
    @exception_bridge
    @enforce_parameter_types
    def selected_version(self: "Self", value: "_1792.SystemDirectory") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_SystemDirectory.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "SelectedVersion", value)

    @property
    @exception_bridge
    def current_version(self: "Self") -> "_1792.SystemDirectory":
        """mastapy.utility.SystemDirectory

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentVersion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def version_to_copy(self: "Self") -> "_1792.SystemDirectory":
        """mastapy.utility.SystemDirectory

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VersionToCopy")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_SystemDirectoryPopulator":
        """Cast to another type.

        Returns:
            _Cast_SystemDirectoryPopulator
        """
        return _Cast_SystemDirectoryPopulator(self)
