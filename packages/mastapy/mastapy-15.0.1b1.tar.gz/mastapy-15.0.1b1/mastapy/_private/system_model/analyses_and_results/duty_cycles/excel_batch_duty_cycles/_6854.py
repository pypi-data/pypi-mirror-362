"""ExcelBatchDutyCycleSpectraCreatorDetails"""

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

_EXCEL_BATCH_DUTY_CYCLE_SPECTRA_CREATOR_DETAILS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DutyCycles.ExcelBatchDutyCycles",
    "ExcelBatchDutyCycleSpectraCreatorDetails",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles import (
        _6855,
        _6857,
        _6858,
    )
    from mastapy._private.utility import _1790

    Self = TypeVar("Self", bound="ExcelBatchDutyCycleSpectraCreatorDetails")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExcelBatchDutyCycleSpectraCreatorDetails._Cast_ExcelBatchDutyCycleSpectraCreatorDetails",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExcelBatchDutyCycleSpectraCreatorDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExcelBatchDutyCycleSpectraCreatorDetails:
    """Special nested class for casting ExcelBatchDutyCycleSpectraCreatorDetails to subclasses."""

    __parent__: "ExcelBatchDutyCycleSpectraCreatorDetails"

    @property
    def excel_batch_duty_cycle_spectra_creator_details(
        self: "CastSelf",
    ) -> "ExcelBatchDutyCycleSpectraCreatorDetails":
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
class ExcelBatchDutyCycleSpectraCreatorDetails(_0.APIBase):
    """ExcelBatchDutyCycleSpectraCreatorDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXCEL_BATCH_DUTY_CYCLE_SPECTRA_CREATOR_DETAILS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def excel_files_found(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcelFilesFound")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def folder(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Folder")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def excel_file_details(self: "Self") -> "_6855.ExcelFileDetails":
        """mastapy.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles.ExcelFileDetails

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcelFileDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def masta_file_details(self: "Self") -> "_6858.MASTAFileDetails":
        """mastapy.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles.MASTAFileDetails

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MASTAFileDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def working_folder(self: "Self") -> "_1790.SelectableFolder":
        """mastapy.utility.SelectableFolder

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingFolder")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def excel_sheet_design_state_selection(
        self: "Self",
    ) -> "List[_6857.ExcelSheetDesignStateSelector]":
        """List[mastapy.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles.ExcelSheetDesignStateSelector]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcelSheetDesignStateSelection")

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
    def edit_folder_path(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "EditFolderPath")

    @exception_bridge
    def prepare_working_folder(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PrepareWorkingFolder")

    @exception_bridge
    def write_masta_files(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "WriteMASTAFiles")

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
    def cast_to(self: "Self") -> "_Cast_ExcelBatchDutyCycleSpectraCreatorDetails":
        """Cast to another type.

        Returns:
            _Cast_ExcelBatchDutyCycleSpectraCreatorDetails
        """
        return _Cast_ExcelBatchDutyCycleSpectraCreatorDetails(self)
