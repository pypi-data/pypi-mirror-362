"""CustomReport"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1940, _1959

_CUSTOM_REPORT = python_net_import("SMT.MastaAPI.Utility.Report", "CustomReport")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1941, _1942, _1958, _1976

    Self = TypeVar("Self", bound="CustomReport")
    CastSelf = TypeVar("CastSelf", bound="CustomReport._Cast_CustomReport")


__docformat__ = "restructuredtext en"
__all__ = ("CustomReport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReport:
    """Special nested class for casting CustomReport to subclasses."""

    __parent__: "CustomReport"

    @property
    def custom_report_item_container(
        self: "CastSelf",
    ) -> "_1959.CustomReportItemContainer":
        return self.__parent__._cast(_1959.CustomReportItemContainer)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def custom_report(self: "CastSelf") -> "CustomReport":
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
class CustomReport(_1959.CustomReportItemContainer):
    """CustomReport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cad_table_border_style(self: "Self") -> "_1942.CadTableBorderType":
        """mastapy.utility.report.CadTableBorderType"""
        temp = pythonnet_property_get(self.wrapped, "CADTableBorderStyle")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Report.CadTableBorderType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.report._1942", "CadTableBorderType"
        )(value)

    @cad_table_border_style.setter
    @exception_bridge
    @enforce_parameter_types
    def cad_table_border_style(self: "Self", value: "_1942.CadTableBorderType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Report.CadTableBorderType"
        )
        pythonnet_property_set(self.wrapped, "CADTableBorderStyle", value)

    @property
    @exception_bridge
    def font_height_for_cad_tables(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FontHeightForCADTables")

        if temp is None:
            return 0.0

        return temp

    @font_height_for_cad_tables.setter
    @exception_bridge
    @enforce_parameter_types
    def font_height_for_cad_tables(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FontHeightForCADTables",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def hide_cad_table_borders(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HideCADTableBorders")

        if temp is None:
            return False

        return temp

    @hide_cad_table_borders.setter
    @exception_bridge
    @enforce_parameter_types
    def hide_cad_table_borders(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HideCADTableBorders",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_report_check(self: "Self") -> "_1976.DefinitionBooleanCheckOptions":
        """mastapy.utility.report.DefinitionBooleanCheckOptions"""
        temp = pythonnet_property_get(self.wrapped, "IncludeReportCheck")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Report.DefinitionBooleanCheckOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.report._1976", "DefinitionBooleanCheckOptions"
        )(value)

    @include_report_check.setter
    @exception_bridge
    @enforce_parameter_types
    def include_report_check(
        self: "Self", value: "_1976.DefinitionBooleanCheckOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Report.DefinitionBooleanCheckOptions"
        )
        pythonnet_property_set(self.wrapped, "IncludeReportCheck", value)

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def page_height_for_cad_export(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PageHeightForCADExport")

        if temp is None:
            return 0.0

        return temp

    @page_height_for_cad_export.setter
    @exception_bridge
    @enforce_parameter_types
    def page_height_for_cad_export(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PageHeightForCADExport",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def page_orientation_for_cad_export(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CadPageOrientation":
        """EnumWithSelectedValue[mastapy.utility.report.CadPageOrientation]"""
        temp = pythonnet_property_get(self.wrapped, "PageOrientationForCADExport")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CadPageOrientation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @page_orientation_for_cad_export.setter
    @exception_bridge
    @enforce_parameter_types
    def page_orientation_for_cad_export(
        self: "Self", value: "_1940.CadPageOrientation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CadPageOrientation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "PageOrientationForCADExport", value)

    @property
    @exception_bridge
    def page_size_for_cad_export(self: "Self") -> "_1941.CadPageSize":
        """mastapy.utility.report.CadPageSize"""
        temp = pythonnet_property_get(self.wrapped, "PageSizeForCADExport")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Report.CadPageSize"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.report._1941", "CadPageSize"
        )(value)

    @page_size_for_cad_export.setter
    @exception_bridge
    @enforce_parameter_types
    def page_size_for_cad_export(self: "Self", value: "_1941.CadPageSize") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Report.CadPageSize"
        )
        pythonnet_property_set(self.wrapped, "PageSizeForCADExport", value)

    @property
    @exception_bridge
    def page_width_for_cad_export(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PageWidthForCADExport")

        if temp is None:
            return 0.0

        return temp

    @page_width_for_cad_export.setter
    @exception_bridge
    @enforce_parameter_types
    def page_width_for_cad_export(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PageWidthForCADExport",
            float(value) if value is not None else 0.0,
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
    def text_margin_for_cad_tables(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TextMarginForCADTables")

        if temp is None:
            return 0.0

        return temp

    @text_margin_for_cad_tables.setter
    @exception_bridge
    @enforce_parameter_types
    def text_margin_for_cad_tables(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TextMarginForCADTables",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_default_border(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDefaultBorder")

        if temp is None:
            return False

        return temp

    @use_default_border.setter
    @exception_bridge
    @enforce_parameter_types
    def use_default_border(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDefaultBorder",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReport":
        """Cast to another type.

        Returns:
            _Cast_CustomReport
        """
        return _Cast_CustomReport(self)
