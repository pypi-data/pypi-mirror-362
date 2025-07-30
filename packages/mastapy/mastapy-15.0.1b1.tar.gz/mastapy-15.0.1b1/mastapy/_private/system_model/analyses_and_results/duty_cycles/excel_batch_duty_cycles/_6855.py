"""ExcelFileDetails"""

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
from mastapy._private.utility.units_and_measurements import _1802

_EXCEL_FILE_DETAILS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DutyCycles.ExcelBatchDutyCycles",
    "ExcelFileDetails",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="ExcelFileDetails")
    CastSelf = TypeVar("CastSelf", bound="ExcelFileDetails._Cast_ExcelFileDetails")


__docformat__ = "restructuredtext en"
__all__ = ("ExcelFileDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExcelFileDetails:
    """Special nested class for casting ExcelFileDetails to subclasses."""

    __parent__: "ExcelFileDetails"

    @property
    def excel_file_details(self: "CastSelf") -> "ExcelFileDetails":
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
class ExcelFileDetails(_0.APIBase):
    """ExcelFileDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXCEL_FILE_DETAILS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def combine_positive_and_negative_speeds(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CombinePositiveAndNegativeSpeeds")

        if temp is None:
            return False

        return temp

    @combine_positive_and_negative_speeds.setter
    @exception_bridge
    @enforce_parameter_types
    def combine_positive_and_negative_speeds(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CombinePositiveAndNegativeSpeeds",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def compress_load_cases(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CompressLoadCases")

        if temp is None:
            return False

        return temp

    @compress_load_cases.setter
    @exception_bridge
    @enforce_parameter_types
    def compress_load_cases(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CompressLoadCases",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def cycles_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "CyclesUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @cycles_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def cycles_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "CyclesUnit", value)

    @property
    @exception_bridge
    def duration_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "DurationUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @duration_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def duration_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DurationUnit", value)

    @property
    @exception_bridge
    def first_data_column(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "FirstDataColumn")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @first_data_column.setter
    @exception_bridge
    @enforce_parameter_types
    def first_data_column(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FirstDataColumn", value)

    @property
    @exception_bridge
    def first_data_row(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "FirstDataRow")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @first_data_row.setter
    @exception_bridge
    @enforce_parameter_types
    def first_data_row(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FirstDataRow", value)

    @property
    @exception_bridge
    def header_column(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "HeaderColumn")

        if temp is None:
            return 0

        return temp

    @header_column.setter
    @exception_bridge
    @enforce_parameter_types
    def header_column(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "HeaderColumn", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def header_row(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "HeaderRow")

        if temp is None:
            return 0

        return temp

    @header_row.setter
    @exception_bridge
    @enforce_parameter_types
    def header_row(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "HeaderRow", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def ignore_sheet_names_containing(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "IgnoreSheetNamesContaining")

        if temp is None:
            return ""

        return temp

    @ignore_sheet_names_containing.setter
    @exception_bridge
    @enforce_parameter_types
    def ignore_sheet_names_containing(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IgnoreSheetNamesContaining",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def negate_speeds_and_torques(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "NegateSpeedsAndTorques")

        if temp is None:
            return False

        return temp

    @negate_speeds_and_torques.setter
    @exception_bridge
    @enforce_parameter_types
    def negate_speeds_and_torques(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NegateSpeedsAndTorques",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def number_of_data_columns(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfDataColumns")

        if temp is None:
            return 0

        return temp

    @number_of_data_columns.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_data_columns(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfDataColumns", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_data_rows(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfDataRows")

        if temp is None:
            return 0

        return temp

    @number_of_data_rows.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_data_rows(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfDataRows", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def show_zero_duration_speeds_and_torques(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowZeroDurationSpeedsAndTorques")

        if temp is None:
            return False

        return temp

    @show_zero_duration_speeds_and_torques.setter
    @exception_bridge
    @enforce_parameter_types
    def show_zero_duration_speeds_and_torques(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowZeroDurationSpeedsAndTorques",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def specify_duration(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyDuration")

        if temp is None:
            return False

        return temp

    @specify_duration.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_duration(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SpecifyDuration", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def specify_number_of_data_rows_and_columns(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyNumberOfDataRowsAndColumns")

        if temp is None:
            return False

        return temp

    @specify_number_of_data_rows_and_columns.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_number_of_data_rows_and_columns(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyNumberOfDataRowsAndColumns",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def speed_unit(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "SpeedUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @speed_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def speed_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "SpeedUnit", value)

    @property
    @exception_bridge
    def torque_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "TorqueUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @torque_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "TorqueUnit", value)

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
    def cast_to(self: "Self") -> "_Cast_ExcelFileDetails":
        """Cast to another type.

        Returns:
            _Cast_ExcelFileDetails
        """
        return _Cast_ExcelFileDetails(self)
