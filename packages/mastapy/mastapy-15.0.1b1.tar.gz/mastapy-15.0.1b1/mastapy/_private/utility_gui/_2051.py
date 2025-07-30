"""DataInputFileOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DATA_INPUT_FILE_OPTIONS = python_net_import(
    "SMT.MastaAPI.UtilityGUI", "DataInputFileOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
        _7868,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2796,
    )

    Self = TypeVar("Self", bound="DataInputFileOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="DataInputFileOptions._Cast_DataInputFileOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DataInputFileOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DataInputFileOptions:
    """Special nested class for casting DataInputFileOptions to subclasses."""

    __parent__: "DataInputFileOptions"

    @property
    def rotor_set_data_input_file_options(
        self: "CastSelf",
    ) -> "_2796.RotorSetDataInputFileOptions":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2796,
        )

        return self.__parent__._cast(_2796.RotorSetDataInputFileOptions)

    @property
    def multi_time_series_data_input_file_options(
        self: "CastSelf",
    ) -> "_7868.MultiTimeSeriesDataInputFileOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7868,
        )

        return self.__parent__._cast(_7868.MultiTimeSeriesDataInputFileOptions)

    @property
    def data_input_file_options(self: "CastSelf") -> "DataInputFileOptions":
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
class DataInputFileOptions(_0.APIBase):
    """DataInputFileOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATA_INPUT_FILE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def column_headers_row(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ColumnHeadersRow")

        if temp is None:
            return 0

        return temp

    @column_headers_row.setter
    @exception_bridge
    @enforce_parameter_types
    def column_headers_row(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ColumnHeadersRow", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def data_end_row(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "DataEndRow")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @data_end_row.setter
    @exception_bridge
    @enforce_parameter_types
    def data_end_row(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DataEndRow", value)

    @property
    @exception_bridge
    def data_start_row(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "DataStartRow")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @data_start_row.setter
    @exception_bridge
    @enforce_parameter_types
    def data_start_row(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DataStartRow", value)

    @property
    @exception_bridge
    def selected_file_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "SelectedFileName")

        if temp is None:
            return ""

        return temp

    @selected_file_name.setter
    @exception_bridge
    @enforce_parameter_types
    def selected_file_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "SelectedFileName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def sheet(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "Sheet")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @sheet.setter
    @exception_bridge
    @enforce_parameter_types
    def sheet(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Sheet", value)

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
    def open_file(self: "Self", filename: "str") -> None:
        """Method does not return.

        Args:
            filename (str)
        """
        filename = str(filename)
        pythonnet_method_call(self.wrapped, "OpenFile", filename if filename else "")

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
    def cast_to(self: "Self") -> "_Cast_DataInputFileOptions":
        """Cast to another type.

        Returns:
            _Cast_DataInputFileOptions
        """
        return _Cast_DataInputFileOptions(self)
