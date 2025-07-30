"""AxisSettings"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_AXIS_SETTINGS = python_net_import("SMT.MastaAPI.Utility.Report", "AxisSettings")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="AxisSettings")
    CastSelf = TypeVar("CastSelf", bound="AxisSettings._Cast_AxisSettings")


__docformat__ = "restructuredtext en"
__all__ = ("AxisSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AxisSettings:
    """Special nested class for casting AxisSettings to subclasses."""

    __parent__: "AxisSettings"

    @property
    def axis_settings(self: "CastSelf") -> "AxisSettings":
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
class AxisSettings(_0.APIBase):
    """AxisSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AXIS_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def end_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndValue")

        if temp is None:
            return 0.0

        return temp

    @end_value.setter
    @exception_bridge
    @enforce_parameter_types
    def end_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EndValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def hide_grid_lines(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HideGridLines")

        if temp is None:
            return False

        return temp

    @hide_grid_lines.setter
    @exception_bridge
    @enforce_parameter_types
    def hide_grid_lines(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HideGridLines", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_title(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowTitle")

        if temp is None:
            return False

        return temp

    @show_title.setter
    @exception_bridge
    @enforce_parameter_types
    def show_title(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowTitle", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def specify_range(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyRange")

        if temp is None:
            return False

        return temp

    @specify_range.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_range(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SpecifyRange", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def start_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartValue")

        if temp is None:
            return 0.0

        return temp

    @start_value.setter
    @exception_bridge
    @enforce_parameter_types
    def start_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StartValue", float(value) if value is not None else 0.0
        )

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
    @exception_bridge
    def unit(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Unit")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def custom_labels(self: "Self") -> "List[str]":
        """List[str]"""
        temp = pythonnet_property_get(self.wrapped, "CustomLabels")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @custom_labels.setter
    @exception_bridge
    @enforce_parameter_types
    def custom_labels(self: "Self", value: "List[str]") -> None:
        value = conversion.mp_to_pn_objects_in_list(value)
        pythonnet_property_set(self.wrapped, "CustomLabels", value)

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
    def cast_to(self: "Self") -> "_Cast_AxisSettings":
        """Cast to another type.

        Returns:
            _Cast_AxisSettings
        """
        return _Cast_AxisSettings(self)
