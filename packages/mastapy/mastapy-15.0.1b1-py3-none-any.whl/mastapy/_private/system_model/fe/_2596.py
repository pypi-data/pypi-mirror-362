"""ElectricMachineDynamicLoadData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import (
    list_with_selected_item,
    list_with_selected_item_and_image,
)
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
from mastapy._private.electric_machines import _1431
from mastapy._private.system_model.analyses_and_results.static_loads import _7739

_ELECTRIC_MACHINE_DYNAMIC_LOAD_DATA = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "ElectricMachineDynamicLoadData"
)

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.load_cases_and_analyses import _1531, _1540
    from mastapy._private.system_model.fe import _2595

    Self = TypeVar("Self", bound="ElectricMachineDynamicLoadData")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineDynamicLoadData._Cast_ElectricMachineDynamicLoadData",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineDynamicLoadData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineDynamicLoadData:
    """Special nested class for casting ElectricMachineDynamicLoadData to subclasses."""

    __parent__: "ElectricMachineDynamicLoadData"

    @property
    def electric_machine_dynamic_load_data(
        self: "CastSelf",
    ) -> "ElectricMachineDynamicLoadData":
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
class ElectricMachineDynamicLoadData(_0.APIBase):
    """ElectricMachineDynamicLoadData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_DYNAMIC_LOAD_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def electric_machine_data_import_type(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_ElectricMachineDataImportType":
        """ListWithSelectedItemAndImage[mastapy.system_model.analyses_and_results.static_loads.ElectricMachineDataImportType]"""
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDataImportType")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_ElectricMachineDataImportType.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @electric_machine_data_import_type.setter
    @exception_bridge
    @enforce_parameter_types
    def electric_machine_data_import_type(
        self: "Self", value: "_7739.ElectricMachineDataImportType"
    ) -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_ElectricMachineDataImportType.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ElectricMachineDataImportType", value)

    @property
    @exception_bridge
    def slice(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_RotorSkewSlice":
        """ListWithSelectedItem[mastapy.electric_machines.RotorSkewSlice]"""
        temp = pythonnet_property_get(self.wrapped, "Slice")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_RotorSkewSlice",
        )(temp)

    @slice.setter
    @exception_bridge
    @enforce_parameter_types
    def slice(self: "Self", value: "_1431.RotorSkewSlice") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_RotorSkewSlice.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Slice", value)

    @property
    @exception_bridge
    def electric_machine_data_sets(
        self: "Self",
    ) -> "List[_2595.ElectricMachineDataSet]":
        """List[mastapy.system_model.fe.ElectricMachineDataSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDataSets")

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
    @enforce_parameter_types
    def add_electric_machine_data_set(
        self: "Self", name: "str"
    ) -> "_2595.ElectricMachineDataSet":
        """mastapy.system_model.fe.ElectricMachineDataSet

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddElectricMachineDataSet", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_electric_machine_data_set_from_masta_dynamic_force_analysis(
        self: "Self",
        analysis: "_1531.DynamicForceAnalysis",
        slice_index: "Optional[int]",
    ) -> "_2595.ElectricMachineDataSet":
        """mastapy.system_model.fe.ElectricMachineDataSet

        Args:
            analysis (mastapy.electric_machines.load_cases_and_analyses.DynamicForceAnalysis)
            slice_index (Optional[int])
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddElectricMachineDataSetFromMASTADynamicForceAnalysis",
            analysis.wrapped if analysis else None,
            slice_index,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_electric_machine_data_set_from_masta_electric_machine_fe_analysis(
        self: "Self",
        analysis: "_1540.ElectricMachineFEAnalysis",
        slice_index: "Optional[int]",
    ) -> "_2595.ElectricMachineDataSet":
        """mastapy.system_model.fe.ElectricMachineDataSet

        Args:
            analysis (mastapy.electric_machines.load_cases_and_analyses.ElectricMachineFEAnalysis)
            slice_index (Optional[int])
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddElectricMachineDataSetFromMASTAElectricMachineFEAnalysis",
            analysis.wrapped if analysis else None,
            slice_index,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def delete_all_data_sets(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteAllDataSets")

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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineDynamicLoadData":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineDynamicLoadData
        """
        return _Cast_ElectricMachineDynamicLoadData(self)
