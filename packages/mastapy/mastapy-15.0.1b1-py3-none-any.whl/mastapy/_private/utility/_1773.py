"""EnvironmentSummary"""

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

_ENVIRONMENT_SUMMARY = python_net_import("SMT.MastaAPI.Utility", "EnvironmentSummary")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.utility import _1772, _1785

    Self = TypeVar("Self", bound="EnvironmentSummary")
    CastSelf = TypeVar("CastSelf", bound="EnvironmentSummary._Cast_EnvironmentSummary")


__docformat__ = "restructuredtext en"
__all__ = ("EnvironmentSummary",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EnvironmentSummary:
    """Special nested class for casting EnvironmentSummary to subclasses."""

    __parent__: "EnvironmentSummary"

    @property
    def environment_summary(self: "CastSelf") -> "EnvironmentSummary":
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
class EnvironmentSummary(_0.APIBase):
    """EnvironmentSummary

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ENVIRONMENT_SUMMARY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def build_date(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BuildDate")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def build_date_and_age(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BuildDateAndAge")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def command_line(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CommandLine")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def core_feature_code_in_use(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoreFeatureCodeInUse")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def core_feature_expiry(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoreFeatureExpiry")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def current_net_framework_version(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentNETFrameworkVersion")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def current_culture_system_locale(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentCultureSystemLocale")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def current_ui_culture_system_locale(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentUICultureSystemLocale")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def date_time_iso8601(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DateTimeISO8601")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def date_time_local_format(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DateTimeLocalFormat")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def dispatcher_information(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DispatcherInformation")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def entry_assembly(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EntryAssembly")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def executable_directory(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExecutableDirectory")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def executable_directory_is_network_path(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExecutableDirectoryIsNetworkPath")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def installed_video_controllers(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InstalledVideoControllers")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def licence_key(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LicenceKey")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def masta_version(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MASTAVersion")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def machine_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MachineName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def open_gl_renderer(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OpenGLRenderer")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def open_gl_vendor(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OpenGLVendor")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def open_gl_version(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OpenGLVersion")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def operating_system(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingSystem")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def prerequisites(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Prerequisites")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def process_render_mode(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProcessRenderMode")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def processor(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Processor")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def ram(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RAM")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def remote_desktop_information(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RemoteDesktopInformation")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def start_date_time_and_age(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StartDateTimeAndAge")

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
    def video_controller_in_use(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VideoControllerInUse")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def current_culture(self: "Self") -> "_1785.NumberFormatInfoSummary":
        """mastapy.utility.NumberFormatInfoSummary

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentCulture")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def dispatchers(self: "Self") -> "List[_1772.DispatcherHelper]":
        """List[mastapy.utility.DispatcherHelper]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Dispatchers")

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
    def __copy__(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Copy")

    @exception_bridge
    def __deepcopy__(self: "Self", memo) -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Copy")

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
    def cast_to(self: "Self") -> "_Cast_EnvironmentSummary":
        """Cast to another type.

        Returns:
            _Cast_EnvironmentSummary
        """
        return _Cast_EnvironmentSummary(self)
