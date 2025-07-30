"""NetworkDatabaseConnectionSettingsItem"""

from __future__ import annotations

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

_NETWORK_DATABASE_CONNECTION_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "NetworkDatabaseConnectionSettingsItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.utility.databases import _2022

    Self = TypeVar("Self", bound="NetworkDatabaseConnectionSettingsItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NetworkDatabaseConnectionSettingsItem._Cast_NetworkDatabaseConnectionSettingsItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("NetworkDatabaseConnectionSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NetworkDatabaseConnectionSettingsItem:
    """Special nested class for casting NetworkDatabaseConnectionSettingsItem to subclasses."""

    __parent__: "NetworkDatabaseConnectionSettingsItem"

    @property
    def network_database_connection_settings_item(
        self: "CastSelf",
    ) -> "NetworkDatabaseConnectionSettingsItem":
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
class NetworkDatabaseConnectionSettingsItem(_0.APIBase):
    """NetworkDatabaseConnectionSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NETWORK_DATABASE_CONNECTION_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_string(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionString")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def connection_timeout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConnectionTimeout")

        if temp is None:
            return 0.0

        return temp

    @connection_timeout.setter
    @exception_bridge
    @enforce_parameter_types
    def connection_timeout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ConnectionTimeout",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def database_name(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "DatabaseName")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @database_name.setter
    @exception_bridge
    @enforce_parameter_types
    def database_name(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DatabaseName", value)

    @property
    @exception_bridge
    def database_name_reportable(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DatabaseNameReportable")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def database_name_specified(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DatabaseNameSpecified")

        if temp is None:
            return ""

        return temp

    @database_name_specified.setter
    @exception_bridge
    @enforce_parameter_types
    def database_name_specified(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DatabaseNameSpecified",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def enabled(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Enabled")

        if temp is None:
            return False

        return temp

    @enabled.setter
    @exception_bridge
    @enforce_parameter_types
    def enabled(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Enabled", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def is_origin_database(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsOriginDatabase")

        if temp is None:
            return False

        return temp

    @is_origin_database.setter
    @exception_bridge
    @enforce_parameter_types
    def is_origin_database(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsOriginDatabase",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def password(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Password")

        if temp is None:
            return ""

        return temp

    @password.setter
    @exception_bridge
    @enforce_parameter_types
    def password(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Password", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def server_name(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "ServerName")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @server_name.setter
    @exception_bridge
    @enforce_parameter_types
    def server_name(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ServerName", value)

    @property
    @exception_bridge
    def server_name_reportable(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ServerNameReportable")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def server_name_specified(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "ServerNameSpecified")

        if temp is None:
            return ""

        return temp

    @server_name_specified.setter
    @exception_bridge
    @enforce_parameter_types
    def server_name_specified(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "ServerNameSpecified", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def specify_server_name(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyServerName")

        if temp is None:
            return False

        return temp

    @specify_server_name.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_server_name(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyServerName",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def state(self: "Self") -> "_2022.ConnectionState":
        """mastapy.utility.databases.ConnectionState

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "State")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Databases.ConnectionState"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.databases._2022", "ConnectionState"
        )(value)

    @property
    @exception_bridge
    def use_windows_credentials_for_authentication(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseWindowsCredentialsForAuthentication"
        )

        if temp is None:
            return False

        return temp

    @use_windows_credentials_for_authentication.setter
    @exception_bridge
    @enforce_parameter_types
    def use_windows_credentials_for_authentication(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseWindowsCredentialsForAuthentication",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def username(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Username")

        if temp is None:
            return ""

        return temp

    @username.setter
    @exception_bridge
    @enforce_parameter_types
    def username(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Username", str(value) if value is not None else ""
        )

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
    def update_database_list(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "UpdateDatabaseList")

    @exception_bridge
    def update_server_list(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "UpdateServerList")

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
    def cast_to(self: "Self") -> "_Cast_NetworkDatabaseConnectionSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_NetworkDatabaseConnectionSettingsItem
        """
        return _Cast_NetworkDatabaseConnectionSettingsItem(self)
