"""FESubstructureVersionComparer"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FE_SUBSTRUCTURE_VERSION_COMPARER = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.VersionComparer", "FESubstructureVersionComparer"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.fe.version_comparer import _2637, _2641

    Self = TypeVar("Self", bound="FESubstructureVersionComparer")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureVersionComparer._Cast_FESubstructureVersionComparer",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureVersionComparer",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureVersionComparer:
    """Special nested class for casting FESubstructureVersionComparer to subclasses."""

    __parent__: "FESubstructureVersionComparer"

    @property
    def fe_substructure_version_comparer(
        self: "CastSelf",
    ) -> "FESubstructureVersionComparer":
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
class FESubstructureVersionComparer(_0.APIBase):
    """FESubstructureVersionComparer

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_VERSION_COMPARER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def check_all_files_in_directory(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CheckAllFilesInDirectory")

        if temp is None:
            return False

        return temp

    @check_all_files_in_directory.setter
    @exception_bridge
    @enforce_parameter_types
    def check_all_files_in_directory(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CheckAllFilesInDirectory",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def file(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "File")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def folder_path_for_saved_files(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FolderPathForSavedFiles")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def load_cases_to_run(self: "Self") -> "_2641.LoadCasesToRun":
        """mastapy.system_model.fe.version_comparer.LoadCasesToRun"""
        temp = pythonnet_property_get(self.wrapped, "LoadCasesToRun")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.FE.VersionComparer.LoadCasesToRun"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.fe.version_comparer._2641", "LoadCasesToRun"
        )(value)

    @load_cases_to_run.setter
    @exception_bridge
    @enforce_parameter_types
    def load_cases_to_run(self: "Self", value: "_2641.LoadCasesToRun") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.FE.VersionComparer.LoadCasesToRun"
        )
        pythonnet_property_set(self.wrapped, "LoadCasesToRun", value)

    @property
    @exception_bridge
    def save_new_design_files(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SaveNewDesignFiles")

        if temp is None:
            return False

        return temp

    @save_new_design_files.setter
    @exception_bridge
    @enforce_parameter_types
    def save_new_design_files(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SaveNewDesignFiles",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def status(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def design_results(self: "Self") -> "List[_2637.DesignResults]":
        """List[mastapy.system_model.fe.version_comparer.DesignResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignResults")

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
    def run(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Run")

    @exception_bridge
    def select_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectFile")

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
    def cast_to(self: "Self") -> "_Cast_FESubstructureVersionComparer":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureVersionComparer
        """
        return _Cast_FESubstructureVersionComparer(self)
