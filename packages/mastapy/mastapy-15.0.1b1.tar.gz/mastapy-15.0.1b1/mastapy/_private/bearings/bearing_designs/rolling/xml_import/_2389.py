"""RollingBearingImporter"""

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

_ROLLING_BEARING_IMPORTER = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.XmlImport", "RollingBearingImporter"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings.bearing_designs.rolling.xml_import import _2390

    Self = TypeVar("Self", bound="RollingBearingImporter")
    CastSelf = TypeVar(
        "CastSelf", bound="RollingBearingImporter._Cast_RollingBearingImporter"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearingImporter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingBearingImporter:
    """Special nested class for casting RollingBearingImporter to subclasses."""

    __parent__: "RollingBearingImporter"

    @property
    def rolling_bearing_importer(self: "CastSelf") -> "RollingBearingImporter":
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
class RollingBearingImporter(_0.APIBase):
    """RollingBearingImporter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_BEARING_IMPORTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_bearings_ready_to_import(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfBearingsReadyToImport")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def replace_existing_bearings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ReplaceExistingBearings")

        if temp is None:
            return False

        return temp

    @replace_existing_bearings.setter
    @exception_bridge
    @enforce_parameter_types
    def replace_existing_bearings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReplaceExistingBearings",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def mappings(self: "Self") -> "List[_2390.XmlBearingTypeMapping]":
        """List[mastapy.bearings.bearing_designs.rolling.xml_import.XmlBearingTypeMapping]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mappings")

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
    def import_all(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ImportAll")

    @exception_bridge
    def load_setup(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "LoadSetup")

    @exception_bridge
    def open_files_in_directory(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "OpenFilesInDirectory")

    @exception_bridge
    def reset_to_defaults(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ResetToDefaults")

    @exception_bridge
    def save_setup(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SaveSetup")

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
    def cast_to(self: "Self") -> "_Cast_RollingBearingImporter":
        """Cast to another type.

        Returns:
            _Cast_RollingBearingImporter
        """
        return _Cast_RollingBearingImporter(self)
