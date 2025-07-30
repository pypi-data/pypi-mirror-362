"""BatchOperations"""

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

_BATCH_OPERATIONS = python_net_import("SMT.MastaAPI.SystemModel.FE", "BatchOperations")

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.fe import _2602

    Self = TypeVar("Self", bound="BatchOperations")
    CastSelf = TypeVar("CastSelf", bound="BatchOperations._Cast_BatchOperations")


__docformat__ = "restructuredtext en"
__all__ = ("BatchOperations",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BatchOperations:
    """Special nested class for casting BatchOperations to subclasses."""

    __parent__: "BatchOperations"

    @property
    def batch_operations(self: "CastSelf") -> "BatchOperations":
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
class BatchOperations(_0.APIBase):
    """BatchOperations

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BATCH_OPERATIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def all_selected(self: "Self") -> "Optional[bool]":
        """Optional[bool]"""
        temp = pythonnet_property_get(self.wrapped, "AllSelected")

        if temp is None:
            return None

        return temp

    @all_selected.setter
    @exception_bridge
    @enforce_parameter_types
    def all_selected(self: "Self", value: "Optional[bool]") -> None:
        pythonnet_property_set(self.wrapped, "AllSelected", value)

    @property
    @exception_bridge
    def select_all_to_be_unloaded(self: "Self") -> "Optional[bool]":
        """Optional[bool]"""
        temp = pythonnet_property_get(self.wrapped, "SelectAllToBeUnloaded")

        if temp is None:
            return None

        return temp

    @select_all_to_be_unloaded.setter
    @exception_bridge
    @enforce_parameter_types
    def select_all_to_be_unloaded(self: "Self", value: "Optional[bool]") -> None:
        pythonnet_property_set(self.wrapped, "SelectAllToBeUnloaded", value)

    @property
    @exception_bridge
    def total_memory_for_all_files_selected_to_unload(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalMemoryForAllFilesSelectedToUnload"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def total_memory_for_all_loaded_external_f_es(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalMemoryForAllLoadedExternalFEs"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def fe_parts(self: "Self") -> "List[_2602.FEPartWithBatchOptions]":
        """List[mastapy.system_model.fe.FEPartWithBatchOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEParts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def fe_parts_with_external_files(
        self: "Self",
    ) -> "List[_2602.FEPartWithBatchOptions]":
        """List[mastapy.system_model.fe.FEPartWithBatchOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEPartsWithExternalFiles")

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
    def load_all_selected_external_files(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "LoadAllSelectedExternalFiles")

    @exception_bridge
    def perform_reduction_for_selected(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformReductionForSelected")

    @exception_bridge
    def remove_all_full_fe_meshes_in_design(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveAllFullFEMeshesInDesign")

    @exception_bridge
    def unload_all_selected_external_files(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "UnloadAllSelectedExternalFiles")

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
    def cast_to(self: "Self") -> "_Cast_BatchOperations":
        """Cast to another type.

        Returns:
            _Cast_BatchOperations
        """
        return _Cast_BatchOperations(self)
