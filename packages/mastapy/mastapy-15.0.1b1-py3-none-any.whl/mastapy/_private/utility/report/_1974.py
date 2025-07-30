"""CustomSubReport"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
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
from mastapy._private.utility.report import _1955

_CUSTOM_SUB_REPORT = python_net_import("SMT.MastaAPI.Utility.Report", "CustomSubReport")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1958, _1966

    Self = TypeVar("Self", bound="CustomSubReport")
    CastSelf = TypeVar("CastSelf", bound="CustomSubReport._Cast_CustomSubReport")


__docformat__ = "restructuredtext en"
__all__ = ("CustomSubReport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomSubReport:
    """Special nested class for casting CustomSubReport to subclasses."""

    __parent__: "CustomSubReport"

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1955.CustomReportDefinitionItem":
        return self.__parent__._cast(_1955.CustomReportDefinitionItem)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        from mastapy._private.utility.report import _1966

        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def custom_sub_report(self: "CastSelf") -> "CustomSubReport":
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
class CustomSubReport(_1955.CustomReportDefinitionItem):
    """CustomSubReport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_SUB_REPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def create_new_page(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CreateNewPage")

        if temp is None:
            return False

        return temp

    @create_new_page.setter
    @exception_bridge
    @enforce_parameter_types
    def create_new_page(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CreateNewPage", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def is_main_report_item(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsMainReportItem")

        if temp is None:
            return False

        return temp

    @is_main_report_item.setter
    @exception_bridge
    @enforce_parameter_types
    def is_main_report_item(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsMainReportItem",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_read_only_in_editor(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsReadOnlyInEditor")

        if temp is None:
            return False

        return temp

    @is_read_only_in_editor.setter
    @exception_bridge
    @enforce_parameter_types
    def is_read_only_in_editor(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsReadOnlyInEditor",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def scale(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Scale")

        if temp is None:
            return 0.0

        return temp

    @scale.setter
    @exception_bridge
    @enforce_parameter_types
    def scale(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Scale", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def show_report_edit_toolbar(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowReportEditToolbar")

        if temp is None:
            return False

        return temp

    @show_report_edit_toolbar.setter
    @exception_bridge
    @enforce_parameter_types
    def show_report_edit_toolbar(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowReportEditToolbar",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_table_of_contents(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowTableOfContents")

        if temp is None:
            return False

        return temp

    @show_table_of_contents.setter
    @exception_bridge
    @enforce_parameter_types
    def show_table_of_contents(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowTableOfContents",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_as_report_in_the_editor(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAsReportInTheEditor")

        if temp is None:
            return False

        return temp

    @show_as_report_in_the_editor.setter
    @exception_bridge
    @enforce_parameter_types
    def show_as_report_in_the_editor(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowAsReportInTheEditor",
            bool(value) if value is not None else False,
        )

    @exception_bridge
    def report_source(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ReportSource")

    @property
    def cast_to(self: "Self") -> "_Cast_CustomSubReport":
        """Cast to another type.

        Returns:
            _Cast_CustomSubReport
        """
        return _Cast_CustomSubReport(self)
